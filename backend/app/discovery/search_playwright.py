
from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright
from urllib.parse import urlparse, urlencode, quote_plus
import os, re, time, hashlib, json

DEFAULT_TIMEOUT = 10000  # Reduced from 15s to 10s for even faster discovery


async def handle_overlays(page):
    """Handle cookie consent dialogs and other overlays that might block interactions"""
    overlay_selectors = [
        # Cookie consent
        '#ccc-overlay',
        '.cookie-consent',
        '.cookie-banner',
        '[data-testid="cookie-banner"]',
        '.gdpr-banner',
        '.privacy-banner',
        
        # Accept/Decline buttons
        'button:has-text("Accept")',
        'button:has-text("Accept All")',
        'button:has-text("I Accept")',
        'button:has-text("Agree")',
        'button:has-text("OK")',
        'button:has-text("Continue")',
        'button[id*="accept"]',
        'button[class*="accept"]',
        
        # Generic overlays
        '.modal-overlay',
        '.overlay',
        '.popup',
        '[data-dismiss="modal"]'
    ]
    
    for selector in overlay_selectors:
        try:
            # Try to dismiss overlays by clicking them
            elements = await page.query_selector_all(selector)
            for element in elements:
                if await element.is_visible():
                    try:
                        await element.click(timeout=2000, force=True)
                        print(f"    🍪 Dismissed overlay: {selector}")
                        await page.wait_for_timeout(1000)
                        break
                    except:
                        continue
        except:
            continue
    
    # Also try pressing Escape to dismiss modals
    try:
        await page.keyboard.press('Escape')
        await page.wait_for_timeout(500)
    except:
        pass


def handle_overlays_sync(page):
    """Sync version of overlay handler"""
    overlay_selectors = [
        # Cookie consent
        '#ccc-overlay',
        '.cookie-consent',
        '.cookie-banner',
        '[data-testid="cookie-banner"]',
        '.gdpr-banner',
        '.privacy-banner',
        
        # Accept/Decline buttons
        'button:has-text("Accept")',
        'button:has-text("Accept All")',
        'button:has-text("I Accept")',
        'button:has-text("Agree")',
        'button:has-text("OK")',
        'button:has-text("Continue")',
        'button[id*="accept"]',
        'button[class*="accept"]',
        
        # Generic overlays
        '.modal-overlay',
        '.overlay',
        '.popup',
        '[data-dismiss="modal"]'
    ]
    
    for selector in overlay_selectors:
        try:
            # Try to dismiss overlays by clicking them
            elements = page.query_selector_all(selector)
            for element in elements:
                if element.is_visible():
                    try:
                        element.click(timeout=2000, force=True)
                        print(f"    🍪 Dismissed overlay: {selector}")
                        page.wait_for_timeout(1000)
                        break
                    except:
                        continue
        except:
            continue
    
    # Also try pressing Escape to dismiss modals
    try:
        page.keyboard.press('Escape')
        page.wait_for_timeout(500)
    except:
        pass

def token_hits(html: str, pii: dict) -> int:
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
    
    # Name matching - more sophisticated but not overly restrictive
    for n in pii.get("names", []):
        if n and len(n.strip()) > 2:
            name_parts = n.lower().split()
            if len(name_parts) >= 2:  # Full name required
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
            elif len(name_parts) == 1 and len(n.strip()) > 4:  # Single names if long enough
                # For single names, be more careful - only count if in meaningful context
                if n.lower() in html_low:
                    # Only count if not in navigation elements and appears with other identifying info
                    name_contexts = re.findall(rf'.{{0,100}}{re.escape(n.lower())}.{{0,100}}', html_low)
                    for context in name_contexts:
                        # Check if context contains other PII indicators
                        if any(email.lower() in context for email in pii.get("emails", []) if email):
                            hits += 1
                            break
                        elif any(phone in context for phone in pii.get("phones", []) if phone):
                            hits += 1
                            break
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
    Build more targeted but comprehensive search queries
    """
    names = pii.get("names", []) or []
    emails = pii.get("emails", []) or []
    phones = pii.get("phones", []) or []
    
    queries = []
    
    # Prioritize full names but also include variations
    for n in names:
        if n and len(n.strip().split()) >= 2:  # Full names
            queries.append(f'"{n}"')  # Exact phrase search
            # Also try first and last name separately if helpful
            parts = n.split()
            if len(parts) == 2:
                queries.append(f"{parts[0]} {parts[1]}")  # Without quotes for broader match
        elif n and len(n.strip()) > 4:  # Single names if long enough
            queries.append(n.strip())
    
    # Add emails (highest value searches)
    for e in emails:
        if e and '@' in e:
            queries.append(f'"{e}"')  # Exact email search
            # Also try without quotes for partial matches
            queries.append(e)
    
    # Add phone variations
    for p in phones:
        if p:
            # Clean phone and try multiple formats
            clean_phone = re.sub(r'[^\d]', '', p)
            if len(clean_phone) >= 10:
                queries.append(p)  # Original format
                queries.append(clean_phone)  # Digits only
                if len(clean_phone) == 10:
                    # Add formatted versions
                    queries.append(f"({clean_phone[:3]}) {clean_phone[3:6]}-{clean_phone[6:]}")
                    queries.append(f"{clean_phone[:3]}-{clean_phone[3:6]}-{clean_phone[6:]}")
    
    # Limit queries to prevent too many searches
    return queries[:8] or [""]  # Increased from 3 to 8 for better coverage

def is_meaningful_result_page(html: str, url: str) -> bool:
    """
    Check if the page appears to be showing search results rather than just a homepage
    Made more permissive to reduce false negatives
    """
    html_low = html.lower()
    
    # Look for result indicators (expanded list)
    result_indicators = [
        'result', 'search result', 'found', 'record', 'profile', 'listing',
        'directory', 'people', 'person', 'individual', 'contact', 'address',
        'data', 'information', 'details', 'search', 'find', 'lookup'
    ]
    
    # Look for "no results" indicators  
    no_result_indicators = [
        'no results found', 'not found', 'no matches', 'no records found', 
        'try again', 'refine your search', 'no people found', 'no listings found', 
        'no entries found', 'search returned 0', 'zero results'
    ]
    
    # Count positive indicators
    positive_score = sum(1 for indicator in result_indicators if indicator in html_low)
    
    # Count negative indicators (be more specific to avoid false positives)
    negative_score = sum(1 for indicator in no_result_indicators if indicator in html_low)
    
    # If there are strong "no results" messages, it's not meaningful
    if negative_score >= 2:  # Require multiple negative indicators
        return False
        
    # Be more permissive - allow pages with any positive indicators or if it's clearly a search results page
    if positive_score >= 1:  # Reduced from 2 to 1
        return True
    
    # Also check URL patterns for search results pages
    url_indicators = ['search', 'result', 'find', 'lookup', 'directory']
    if any(indicator in url.lower() for indicator in url_indicators):
        return True
    
    # If we can't determine, assume it's meaningful (be permissive)
    return True

def search_broker(broker: dict, pii: dict, evidence_dir: str = "/tmp") -> dict:
    """
    Enhanced search with better balance between precision and recall
    """
    print(f"🔍 Searching {broker.get('domain', 'unknown')} for PII...")
    
    search_url = broker.get("search_url") or f"https://{broker.get('domain', '')}"
    if not search_url:
        return {"found": False, "confidence": 0.0, "error": "No search URL"}
    
    queries = build_queries(pii)
    print(f"📝 Generated {len(queries)} search queries: {queries[:3]}...")  # Show first 3 queries
    
    if not queries:
        return {"found": False, "confidence": 0.0, "error": "No valid search queries generated"}
    
    found = False
    max_hits = 0
    confidence = 0.0
    evidence_url = ""
    best_url = ""
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.set_default_timeout(DEFAULT_TIMEOUT)
            
            for i, q in enumerate(queries):
                print(f"  🔎 Trying query {i+1}/{len(queries)}: '{q[:50]}...'")
                try:
                    page.goto(search_url, wait_until="networkidle")
                    
                    # Handle overlays and cookie consents
                    handle_overlays_sync(page)
                    
                    # Fill search form
                    search_filled = False
                    search_selectors = [
                        "input[name='search']", "input[name='q']", "input[name='query']",
                        "input[type='search']", "input[placeholder*='search']", "input[placeholder*='name']",
                        "input[placeholder*='find']", "input[id*='search']", "input[class*='search']",
                        "input[name*='name']", "input[name*='first']", "input[name*='last']"
                    ]
                    
                    for selector in search_selectors:
                        try:
                            if page.locator(selector).count() > 0:
                                page.fill(selector, q)
                                search_filled = True
                                print(f"    📝 Filled search field with selector: {selector}")
                                break
                        except Exception as e:
                            print(f"    ⚠️ Failed to fill {selector}: {e}")
                            continue
                    
                    if not search_filled:
                        print(f"    ❌ No search field found on page")
                        # Still continue to check the page for existing content
                    
                    if search_filled:
                        # Submit search - try Enter key first as it's most reliable
                        try:
                            page.keyboard.press('Enter')
                            page.wait_for_load_state("networkidle", timeout=10000)
                            submitted = True
                            print(f"    🚀 Submitted search with Enter key")
                        except Exception as e:
                            print(f"    ⚠️ Failed to submit with Enter: {e}")
                            submitted = False
                            
                            # Fall back to button clicking
                            submit_selectors = [
                                "button[type='submit']", "input[type='submit']", 
                                "button:has-text('Search')", "button:has-text('Find')",
                                "button[id*='search']", "button[class*='search']",
                                "input[value*='Search']", "input[value*='Find']"
                            ]
                            
                            for selector in submit_selectors:
                                try:
                                    if page.locator(selector).count() > 0:
                                        page.click(selector, force=True, timeout=10000)
                                        page.wait_for_load_state("networkidle", timeout=10000)
                                        submitted = True
                                        print(f"    🚀 Submitted search with: {selector}")
                                        break
                                except Exception as e:
                                    print(f"    ⚠️ Failed to submit with {selector}: {e}")
                                    continue
                        
                        if not submitted:
                            print(f"    ❌ No submit method worked")
                    
                    html = page.content()
                    
                    # Check if this looks like a meaningful results page
                    page_is_meaningful = is_meaningful_result_page(html, page.url)
                    print(f"    📄 Page analysis: meaningful={page_is_meaningful}, URL={page.url[:100]}...")
                    
                    if not page_is_meaningful:
                        print(f"    ❌ Page doesn't appear to show search results")
                        continue
                    
                    hits = token_hits(html, pii)
                    print(f"    📊 Found {hits} hits on this page")
                    
                    if hits > max_hits:
                        max_hits = hits
                        best_url = page.url
                        
                        # More permissive thresholds to get some results
                        if hits >= 2:  # Lowered from 4 to 2 for primary threshold
                            found = True
                            confidence = min(1.0, 0.4 + 0.1 * hits)
                            evidence_url = page.url
                            
                            # Take screenshot of the best result
                            os.makedirs(evidence_dir, exist_ok=True)
                            shot_path = os.path.join(evidence_dir, f"{broker.get('domain', 'unknown')}.png")
                            page.screenshot(path=shot_path, full_page=True)
                            print(f"    ✅ MATCH FOUND! Hits: {hits}, Confidence: {confidence:.2f}")
                            break  # Found a good match, no need to continue
                        elif hits >= 1:  # Even lower threshold for potential matches
                            # For 1+ hits, mark as potential but keep searching
                            found = True
                            confidence = min(0.5, 0.2 + 0.1 * hits)  # Lower confidence
                            evidence_url = page.url
                            
                            # Take screenshot but continue searching for better matches
                            os.makedirs(evidence_dir, exist_ok=True)
                            shot_path = os.path.join(evidence_dir, f"{broker.get('domain', 'unknown')}.png")
                            page.screenshot(path=shot_path, full_page=True)
                            print(f"    ⚠️ POTENTIAL MATCH: Hits: {hits}, Confidence: {confidence:.2f} (continuing search...)")
                        else:
                            print(f"    📉 Hits below threshold: {hits} < 1")
                            
                except Exception as e:
                    # Log error but continue with next query
                    print(f"    ❌ Error with query '{q}': {e}")
                    continue
                    
    except Exception as e:
        print(f"❌ Browser error for {broker.get('domain', 'unknown')}: {e}")
    finally:
        try:
            browser.close()
        except:
            pass

    # Final result summary
    print(f"🏁 Search complete for {broker.get('domain', 'unknown')}: Found={found}, Max hits={max_hits}")
    
    # Add notes about the search quality
    notes = f"max_hits: {max_hits}, queries_tried: {len(queries)}"
    if found:
        if max_hits >= 4:
            notes += f", confidence_reason: strong_match_found"
        else:
            notes += f", confidence_reason: potential_match_found"
    else:
        notes += f", reason: threshold_not_met (need ≥2 hits, got {max_hits})"
    
    return {
        "found": found,
        "confidence": confidence,
        "evidence_url": evidence_url,
        "best_url": best_url,
        "screenshot": os.path.join(evidence_dir, f"{broker.get('domain', 'unknown')}.png") if found else None,
        "notes": notes,
        "debug_hits": max_hits
    }
