
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
        broker = self.broker
        pii = self.pii
        url = broker.get("optout_url") or broker.get("search_url") or f"https://{broker.get('domain','')}"
        if not url:
            return {"status":"error","transcript":"No opt-out URL","evidence_path":None}
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)  # headful for CAPTCHA
            page = browser.new_page()
            page.goto(url)
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
                        page.click(btn); break
                except Exception:
                    pass
            page.wait_for_load_state("networkidle")
            evidence = Path("evidence_form.png")
            page.screenshot(path=str(evidence), full_page=True)
            browser.close()
        return {"status":"submitted","transcript":"Generic form submitted (verify if CAPTCHA present)","evidence_path": str(evidence)}
