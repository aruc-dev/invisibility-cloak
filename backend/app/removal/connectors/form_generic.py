
from playwright.sync_api import sync_playwright
from .base import RemovalConnector

DEFAULT_FIELDS = [
  ("input[name='name']", lambda pii: (pii.get('names') or [""])[0]),
  ("input[name='email']", lambda pii: (pii.get('emails') or [""])[0]),
  ("input[name='phone']", lambda pii: (pii.get('phones') or [""])[0]),
]

class GenericForm(RemovalConnector):
    def submit(self):
        from pathlib import Path
        import time, uuid

        broker = self.broker
        pii = self.pii
        url = broker.get("optout_url") or broker.get("search_url") or f"https://{broker.get('domain','')}"

        if not url:
            return {"status":"error","transcript":"No opt-out URL","evidence_path":None}

        # Setup evidence directory
        store_dir = Path(__file__).resolve().parents[4] / "storage"
        evidence_dir = store_dir / "evidence" / "removals"
        evidence_dir.mkdir(parents=True, exist_ok=True)

        evidence_filename = f"{broker.get('domain', 'unknown')}_{uuid.uuid4()}.png"
        evidence_path = evidence_dir / evidence_filename

        with sync_playwright() as p:
            # We use headless=False assuming manual intervention might be needed for CAPTCHA
            # if running locally, otherwise this might fail in headless environments without display
            browser = p.chromium.launch(headless=self.headless)
            page = browser.new_page()
            try:
                page.goto(url, timeout=30000)
                for sel, fn in DEFAULT_FIELDS:
                    try:
                        if page.locator(sel).count():
                            page.fill(sel, fn(pii))
                    except Exception:
                        pass
                # try submit
                for btn in ["button[type=submit]","button:has-text('Submit')","input[type=submit]"]:
                    try:
                        if page.locator(btn).count():
                            page.click(btn, timeout=2000)
                            break
                    except Exception:
                        pass

                page.wait_for_load_state("networkidle", timeout=10000)
                page.screenshot(path=str(evidence_path), full_page=True)
            except Exception as e:
                print(f"Error in form submission for {broker.get('name')}: {e}")
                # Try to take screenshot of error
                try:
                    page.screenshot(path=str(evidence_path), full_page=True)
                except:
                    pass
                return {"status":"error","transcript":f"Error: {str(e)}","evidence_path": str(evidence_path) if evidence_path.exists() else None}
            finally:
                browser.close()

        return {"status":"submitted","transcript":"Generic form submitted (verify if CAPTCHA present)","evidence_path": str(evidence_path)}
