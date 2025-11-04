
from playwright.sync_api import sync_playwright
from urllib.parse import urlparse, urlencode
import os, re, time, hashlib, json

DEFAULT_TIMEOUT = 30000

def token_hits(html: str, pii: dict) -> int:
    html_low = html.lower()
    hits = 0
    for e in pii.get("emails", []):
        if e and e.lower() in html_low: hits += 3
    for p in pii.get("phones", []):
        if p and p in html: hits += 2
    for n in pii.get("names", []):
        if n and n.lower() in html_low: hits += 1
    # Address city/zip light checks
    for adr in pii.get("addresses", []):
        city = (adr or {}).get("city")
        if city and city.lower() in html_low: hits += 1
        zipc = (adr or {}).get("zip") or (adr or {}).get("postal")
        if zipc and zipc in html: hits += 1
    return hits

def build_queries(pii: dict):
    names = pii.get("names", []) or []
    emails = pii.get("emails", []) or []
    phones = pii.get("phones", []) or []
    cities = [(a or {}).get("city") for a in (pii.get("addresses", []) or []) if (a or {}).get("city")]
    queries = []
    for n in names:
        for c in (cities or [""]):
            q = f"\"{n}\" {c}".strip()
            if q not in queries: queries.append(q)
    for e in emails:
        if e not in queries: queries.append(e)
    for p in phones:
        if p not in queries: queries.append(p)
    return queries or [""]

def search_broker(broker: dict, pii: dict, evidence_dir: str) -> dict:
    found, confidence, evidence_url, shot_path = False, 0.0, None, None
    search_url = broker.get("search_url") or (f"https://{broker.get('domain')}" if broker.get("domain") else None)
    if not search_url:
        return {"found": False, "confidence": 0.0, "evidence_url": None, "screenshot": None, "notes":"no search url"}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_default_timeout(DEFAULT_TIMEOUT)
        try:
            queries = build_queries(pii)
            for q in queries:
                url = search_url
                if "{query}" in url:
                    # replace with encoded query param (keep it simple for now)
                    url = url.replace("{query}", urlencode({"q": q}))
                page.goto(url)
                # try inline search boxes
                try:
                    sel = None
                    for s in ["input[name=q]", "input[type=search]", "input[placeholder*=Search i]"]:
                        if page.locator(s).count():
                            sel = s
                            break
                    if sel:
                        page.fill(sel, q)
                        page.keyboard.press("Enter")
                except Exception:
                    pass
                page.wait_for_load_state("networkidle")
                html = page.content()
                hits = token_hits(html, pii)
                if hits >= 3:
                    found = True
                    confidence = min(1.0, 0.5 + 0.1*hits)
                    evidence_url = page.url
                    os.makedirs(evidence_dir, exist_ok=True)
                    shot_path = os.path.join(evidence_dir, f"{broker.get('domain','unknown')}.png")
                    page.screenshot(path=shot_path, full_page=True)
                    break
        finally:
            browser.close()

    return {"found": found, "confidence": confidence, "evidence_url": evidence_url, "screenshot": shot_path}
