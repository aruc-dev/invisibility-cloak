
from playwright.sync_api import sync_playwright
from urllib.parse import urlparse, urlencode, quote_plus
import os, re, time, hashlib, json

DEFAULT_TIMEOUT = 30000

def token_hits(html: str, pii: dict, strict_mode: bool = True) -> int:
    """
    Calculate hits with improved logic to reduce false positives
    """
    html_low = html.lower()
    hits = 0
    
    # Email matching - high value, exact match required
    for e in pii.get("emails", []):
        if e and e.lower() in html_low:
            # Check if email appears in a meaningful context (not just in page source/scripts)
            if re.search(rf'\b{re.escape(e.lower())}\b', html_low):
                hits += 4
    
    # Phone matching - exact format required
    for p in pii.get("phones", []):
        if p:
            # Clean phone number for matching
            clean_phone = re.sub(r'[^\d]', '', p)
            if len(clean_phone) >= 10:
                # Look for phone in various formats
                phone_patterns = [
                    p,  # Original format
                    clean_phone,  # Digits only
                    f"({clean_phone[:3]}) {clean_phone[3:6]}-{clean_phone[6:]}" if len(clean_phone) == 10 else None,
                    f"{clean_phone[:3]}-{clean_phone[3:6]}-{clean_phone[6:]}" if len(clean_phone) == 10 else None
                ]
                for pattern in phone_patterns:
                    if pattern and pattern in html:
                        hits += 3
                        break
    
    # Name matching - more sophisticated
    for n in pii.get("names", []):
        if n and len(n.strip()) > 2:
            name_parts = n.lower().split()
            if len(name_parts) >= 2:  # Only count full names, not single words
                # Check for full name match
                if n.lower() in html_low:
                    # Verify it's not just in navigation/footer by checking context
                    name_contexts = re.findall(rf'.{{0,50}}{re.escape(n.lower())}.{{0,50}}', html_low)
                    meaningful_contexts = 0
                    for context in name_contexts:
                        # Skip if appears in common page elements
                        if not any(skip_word in context for skip_word in 
                                 ['nav', 'menu', 'footer', 'header', 'sidebar', 'copyright', 'terms', 'privacy']):
                            meaningful_contexts += 1
                    
                    if meaningful_contexts > 0:
                        hits += 2
    
    # Address matching - only count if multiple address components match
    address_hits = 0
    for adr in pii.get("addresses", []):
        if not adr:
            continue
            
        city = adr.get("city")
        state = adr.get("state") 
        zip_code = adr.get("zip") or adr.get("postal")
        
        temp_address_hits = 0
        if city and len(city) > 3 and city.lower() in html_low:
            temp_address_hits += 1
        if state and state.lower() in html_low:
            temp_address_hits += 1
        if zip_code and zip_code in html:
            temp_address_hits += 1
            
        # Only count address hits if multiple components match
        if temp_address_hits >= 2:
            address_hits += temp_address_hits
    
    hits += address_hits
    return hits

def build_queries(pii: dict):
    """
    Build more targeted search queries
    """
    names = pii.get("names", []) or []
    emails = pii.get("emails", []) or []
    phones = pii.get("phones", []) or []
    
    queries = []
    
    # Prioritize full names (skip single words)
    for n in names:
        if n and len(n.strip().split()) >= 2:  # Only full names
            queries.append(f'"{n}"')  # Exact phrase search
    
    # Add emails (highest value searches)
    for e in emails:
        if e and '@' in e:
            queries.append(e)
    
    # Add formatted phone numbers
    for p in phones:
        if p:
            # Clean and format phone
            clean = re.sub(r'[^\d]', '', p)
            if len(clean) >= 10:
                queries.append(p)  # Original format
                
    return queries[:3] or [""]  # Limit to top 3 queries to avoid timeout

def is_meaningful_result_page(html: str, url: str) -> bool:
    """
    Check if the page appears to be showing search results rather than just a homepage
    """
    html_low = html.lower()
    
    # Look for result indicators
    result_indicators = [
        'result', 'search result', 'found', 'record', 'profile', 'listing',
        'directory', 'people', 'person', 'individual', 'contact', 'address'
    ]
    
    # Look for "no results" indicators  
    no_result_indicators = [
        'no results', 'not found', 'no matches', 'no records', 'try again',
        'refine your search', 'no people found', 'no listings', 'no entries'
    ]
    
    # Count positive indicators
    positive_score = sum(1 for indicator in result_indicators if indicator in html_low)
    
    # Count negative indicators  
    negative_score = sum(1 for indicator in no_result_indicators if indicator in html_low)
    
    # If there are clear "no results" messages, it's not a meaningful result
    if negative_score > 0:
        return False
        
    # Need some positive indicators to consider it meaningful
    return positive_score >= 2

def search_broker(broker: dict, pii: dict, evidence_dir: str) -> dict:
    found, confidence, evidence_url, shot_path = False, 0.0, None, None
    search_url = broker.get("search_url") or (f"https://{broker.get('domain')}" if broker.get("domain") else None)
    
    if not search_url:
        return {"found": False, "confidence": 0.0, "evidence_url": None, "screenshot": None, "notes": "no search url"}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_default_timeout(DEFAULT_TIMEOUT)
        
        # Set realistic user agent
        page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })
        
        try:
            queries = build_queries(pii)
            max_hits = 0
            best_url = None
            
            for q in queries:
                try:
                    url = search_url
                    if "{query}" in url:
                        url = url.replace("{query}", quote_plus(q))
                    elif "?" not in url:
                        # Try appending as query parameter
                        url = f"{url}?q={quote_plus(q)}"
                    
                    page.goto(url, wait_until="networkidle")
                    
                    # Try to find and use search form
                    search_selectors = [
                        "input[name='q']", "input[name='query']", "input[name='search']",
                        "input[type='search']", "input[placeholder*='earch' i]",
                        "input[placeholder*='name' i]", "#search", ".search-input"
                    ]
                    
                    search_attempted = False
                    for selector in search_selectors:
                        try:
                            if page.locator(selector).count() > 0:
                                page.fill(selector, q)
                                # Try Enter key first
                                page.keyboard.press("Enter")
                                page.wait_for_load_state("networkidle", timeout=10000)
                                search_attempted = True
                                break
                        except Exception:
                            continue
                    
                    # If no search form found, try submit button
                    if not search_attempted:
                        submit_selectors = [
                            "button[type='submit']", "input[type='submit']", 
                            "button:has-text('Search')", "button:has-text('Find')"
                        ]
                        for selector in submit_selectors:
                            try:
                                if page.locator(selector).count() > 0:
                                    page.click(selector)
                                    page.wait_for_load_state("networkidle", timeout=10000)
                                    break
                            except Exception:
                                continue
                    
                    html = page.content()
                    
                    # Check if this looks like a meaningful results page
                    if not is_meaningful_result_page(html, page.url):
                        continue
                    
                    hits = token_hits(html, pii, strict_mode=True)
                    
                    if hits > max_hits:
                        max_hits = hits
                        best_url = page.url
                        
                        # Require higher threshold for "found"
                        if hits >= 6:  # Increased from 3 to 6
                            found = True
                            confidence = min(1.0, 0.3 + 0.08 * hits)  # More conservative confidence
                            evidence_url = page.url
                            
                            # Take screenshot of the best result
                            os.makedirs(evidence_dir, exist_ok=True)
                            shot_path = os.path.join(evidence_dir, f"{broker.get('domain', 'unknown')}.png")
                            page.screenshot(path=shot_path, full_page=True)
                            
                except Exception as e:
                    # Log error but continue with next query
                    print(f"Error searching {broker.get('domain', 'unknown')} with query '{q}': {e}")
                    continue
                    
        except Exception as e:
            print(f"Browser error for {broker.get('domain', 'unknown')}: {e}")
        finally:
            browser.close()

    # Add notes about the search quality
    notes = f"max_hits: {max_hits}, queries_tried: {len(queries)}"
    if found:
        notes += f", confidence_reason: meaningful_context_found"
    else:
        notes += f", confidence_reason: insufficient_context_or_hits"

    return {
        "found": found, 
        "confidence": confidence, 
        "evidence_url": evidence_url, 
        "screenshot": shot_path,
        "notes": notes
    }
