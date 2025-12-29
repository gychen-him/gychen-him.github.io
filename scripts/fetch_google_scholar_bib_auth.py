#!/usr/bin/env python3
"""
Fetch BibTeX entries from Google Scholar with authentication
This script uses Selenium to login to Google Scholar and fetch publications.
"""

import os
import sys
import time
import json
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bib_database import BibDatabase
import re
from urllib.parse import urlparse, parse_qs

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
except ImportError:
    print("Error: selenium library not installed. Install it with: pip install selenium")
    sys.exit(1)

def normalize_bibtex_entry(entry):
    """Normalize BibTeX entry format"""
    if 'author' not in entry:
        entry['author'] = ''
    if 'title' not in entry:
        entry['title'] = 'Untitled'
    if 'year' not in entry:
        entry['year'] = ''
    
    for key, value in entry.items():
        if isinstance(value, str):
            entry[key] = ' '.join(value.split())
    
    return entry

def login_to_google(driver, email, password):
    """Login to Google account"""
    print("Logging in to Google account...")
    
    try:
        # Navigate to Google Scholar login page
        driver.get("https://accounts.google.com/signin/v2/identifier?service=scholar&continue=https%3A%2F%2Fscholar.google.com%2F&flowName=GlifWebSignIn&flowEntry=ServiceLogin")
        
        # Wait for email input
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "identifierId"))
        )
        email_input.send_keys(email)
        email_input.send_keys(Keys.RETURN)
        
        time.sleep(2)
        
        # Wait for password input
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)
        
        # Wait for login to complete
        time.sleep(5)
        
        # Check if login was successful
        if "scholar.google.com" in driver.current_url:
            print("Login successful!")
            return True
        else:
            print("Login may have failed or requires additional verification")
            print(f"Current URL: {driver.current_url}")
            return False
            
    except TimeoutException:
        print("Timeout during login. The page may have changed or requires additional verification.")
        return False
    except Exception as e:
        print(f"Error during login: {e}")
        return False

def extract_bibtex_from_page(driver):
    """Extract BibTeX entries from current page"""
    bibtex_entries = []
    main_window = driver.current_window_handle
    
    try:
        # Find all publication entries on the page
        publications = driver.find_elements(By.CSS_SELECTOR, "tr.gsc_a_tr")
        print(f"Found {len(publications)} publications on this page")
        
        for idx, pub in enumerate(publications):
            try:
                # Get title for logging
                try:
                    title = pub.find_element(By.CSS_SELECTOR, "a.gsc_a_at").text
                    print(f"\n[{idx+1}/{len(publications)}] Processing: {title[:50]}...")
                except:
                    print(f"\n[{idx+1}/{len(publications)}] Processing publication...")
                
                # Find and click the Cite button (not the title!)
                # The Cite button has class "gsc_a_ac" or is a link with "Cited by" nearby
                cite_button = pub.find_element(By.CSS_SELECTOR, "a.gsc_a_ac, a.gsc_a_c")
                
                # Scroll into view
                driver.execute_script("arguments[0].scrollIntoView(true);", cite_button)
                time.sleep(0.3)
                
                cite_button.click()
                time.sleep(1.5)
                
                # Wait for citation popup to appear
                try:
                    # Look for BibTeX link in the popup
                    bibtex_link = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'BibTeX') or contains(@href, 'scholar.bib')]"))
                    )
                    
                    print(f"  → Found BibTeX link, clicking...")
                    bibtex_link.click()
                    time.sleep(1.5)
                    
                    # BibTeX opens in a new window/tab
                    # Switch to the new window
                    all_windows = driver.window_handles
                    for window in all_windows:
                        if window != main_window:
                            driver.switch_to.window(window)
                            break
                    
                    # Extract BibTeX content
                    try:
                        bibtex_content = driver.find_element(By.TAG_NAME, "pre").text
                        print(f"  → Successfully extracted BibTeX")
                        
                        # Parse BibTeX entry
                        parser = BibTexParser()
                        parser.ignore_nonstandard_types = False
                        db = bibtexparser.loads(bibtex_content, parser=parser)
                        
                        if db.entries:
                            bibtex_entries.extend(db.entries)
                            print(f"  → Added {len(db.entries)} entry(ies)")
                        
                    except NoSuchElementException:
                        print(f"  ✗ Could not find BibTeX content")
                    
                    # Close the BibTeX window and switch back
                    driver.close()
                    driver.switch_to.window(main_window)
                    time.sleep(0.5)
                    
                    # Close the citation popup if it's still open
                    try:
                        close_button = driver.find_element(By.CSS_SELECTOR, "#gs_cit-x, button.gs_btnFI")
                        close_button.click()
                        time.sleep(0.3)
                    except:
                        # Try pressing Escape key
                        from selenium.webdriver.common.action_chains import ActionChains
                        ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                        time.sleep(0.3)
                    
                except TimeoutException:
                    print(f"  ✗ Could not find BibTeX link (timeout)")
                    # Make sure we're back to main window
                    driver.switch_to.window(main_window)
                    
                    # Try to close any popup
                    try:
                        close_button = driver.find_element(By.CSS_SELECTOR, "#gs_cit-x, button.gs_btnFI")
                        close_button.click()
                    except:
                        from selenium.webdriver.common.action_chains import ActionChains
                        ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                    
                    continue
                    
            except Exception as e:
                print(f"  ✗ Error processing publication: {e}")
                # Make sure we're back to main window
                try:
                    if driver.current_window_handle != main_window:
                        driver.close()
                        driver.switch_to.window(main_window)
                except:
                    pass
                continue
        
        print(f"\n✓ Total extracted: {len(bibtex_entries)} BibTeX entries")
        return bibtex_entries
        
    except Exception as e:
        print(f"Error extracting BibTeX: {e}")
        import traceback
        traceback.print_exc()
        return []

def construct_bibtex_from_page(driver):
    """Construct BibTeX entry from publication page when export is not available"""
    try:
        entry = {}
        
        # Extract title
        title_elem = driver.find_element(By.CSS_SELECTOR, "a.gsc_oci_title_link, h3.gsc_oci_title")
        entry['title'] = title_elem.text.strip()
        
        # Extract authors
        try:
            authors_elem = driver.find_element(By.CSS_SELECTOR, "div.gsc_oci_value")
            authors_text = authors_elem.text
            # Convert to "Last, First" format
            authors = [a.strip() for a in authors_text.split(',')]
            entry['author'] = ' and '.join(authors)
        except:
            entry['author'] = ''
        
        # Extract year
        try:
            year_elem = driver.find_element(By.XPATH, "//div[contains(text(), 'Publication date')]/following-sibling::div")
            year_text = year_elem.text
            year_match = re.search(r'\d{4}', year_text)
            if year_match:
                entry['year'] = year_match.group()
        except:
            entry['year'] = ''
        
        # Extract journal/venue
        try:
            journal_elem = driver.find_element(By.XPATH, "//div[contains(text(), 'Publication')]/following-sibling::div")
            entry['journal'] = journal_elem.text
        except:
            pass
        
        # Generate entry key
        title = entry.get('title', 'untitled')
        year = entry.get('year', '')
        first_author = entry.get('author', '').split(' and ')[0].split(',')[0] if entry.get('author') else ''
        entry_key = f"{first_author.lower()}{year}{title[:20].lower().replace(' ', '')}"
        entry_key = re.sub(r'[^a-z0-9]', '', entry_key)
        
        entry['ENTRYTYPE'] = 'article'
        entry['ID'] = entry_key
        
        return normalize_bibtex_entry(entry)
        
    except Exception as e:
        print(f"Error constructing BibTeX: {e}")
        return None

def fetch_all_publications(driver, scholar_id):
    """Fetch all publications from Google Scholar profile"""
    print(f"\n{'='*60}")
    print(f"Fetching all publications for Scholar ID: {scholar_id}")
    print(f"{'='*60}\n")
    
    url = f"https://scholar.google.com/citations?user={scholar_id}&hl=en&cstart=0&pagesize=100"
    driver.get(url)
    time.sleep(3)
    
    all_entries = []
    page = 0
    max_pages = 10  # Safety limit
    
    while page < max_pages:
        print(f"\n📄 Page {page + 1}")
        print("-" * 60)
        
        # Extract BibTeX from current page
        entries = extract_bibtex_from_page(driver)
        all_entries.extend(entries)
        
        print(f"\n📊 Page summary: {len(entries)} entries extracted")
        print(f"📊 Running total: {len(all_entries)} entries\n")
        
        # Try to go to next page
        try:
            # Look for "Show more" button or next page button
            next_button = driver.find_element(By.CSS_SELECTOR, "button#gsc_bpf_more, button.gsc_pgn_ppr")
            
            if 'disabled' in next_button.get_attribute('class'):
                print("✓ Reached last page (button disabled)")
                break
                
            if not next_button.is_enabled():
                print("✓ Reached last page (button not enabled)")
                break
            
            print(f"→ Loading next page...")
            next_button.click()
            time.sleep(3)
            page += 1
            
        except NoSuchElementException:
            print("✓ No more pages (button not found)")
            break
        except Exception as e:
            print(f"⚠ Error navigating to next page: {e}")
            break
    
    print(f"\n{'='*60}")
    print(f"✓ Extraction complete: {len(all_entries)} total entries")
    print(f"{'='*60}\n")
    
    return all_entries

def merge_with_existing_bib(existing_file, new_entries):
    """Merge new entries with existing BibTeX file, preserving custom fields"""
    if not os.path.exists(existing_file):
        print(f"Existing file {existing_file} not found, creating new file")
        db = BibDatabase()
        db.entries = new_entries
        return db
    
    with open(existing_file, 'r', encoding='utf-8') as f:
        parser = BibTexParser()
        parser.ignore_nonstandard_types = False
        existing_db = bibtexparser.load(f, parser=parser)
    
    existing_map = {}
    for entry in existing_db.entries:
        title = entry.get('title', '').lower().strip()
        existing_map[title] = entry
    
    merged_entries = []
    new_titles = set()
    
    for entry in existing_db.entries:
        merged_entries.append(entry)
        title = entry.get('title', '').lower().strip()
        if title:
            new_titles.add(title)
    
    for entry in new_entries:
        title = entry.get('title', '').lower().strip()
        if title and title not in new_titles:
            merged_entries.append(entry)
            new_titles.add(title)
    
    db = BibDatabase()
    db.entries = merged_entries
    return db

def main():
    scholar_id = os.environ.get('GOOGLE_SCHOLAR_ID', 'AUpqepUAAAAJ')
    google_email = os.environ.get('GOOGLE_EMAIL')
    google_password = os.environ.get('GOOGLE_PASSWORD')
    output_file = os.environ.get('BIB_OUTPUT_FILE', 'pub.bib')
    
    if not google_email or not google_password:
        print("Error: GOOGLE_EMAIL and GOOGLE_PASSWORD environment variables must be set")
        print("Please set them in GitHub Secrets for automated runs")
        sys.exit(1)
    
    print(f"Starting authenticated BibTeX fetch from Google Scholar...")
    print(f"Scholar ID: {scholar_id}")
    print(f"Output file: {output_file}")
    
    # Setup Chrome options
    chrome_options = Options()
    if os.environ.get('HEADLESS', 'true').lower() == 'true':
        chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    driver = None
    try:
        driver = webdriver.Chrome(options=chrome_options)
        
        # Login
        if not login_to_google(driver, google_email, google_password):
            print("Login failed. Please check credentials or handle 2FA manually.")
            sys.exit(1)
        
        # Fetch publications
        publications = fetch_all_publications(driver, scholar_id)
        
        if not publications:
            print("No publications found")
            sys.exit(1)
        
        print(f"Fetched {len(publications)} publications")
        
        # Merge with existing file
        db = merge_with_existing_bib(output_file, publications)
        
        # Write to file
        writer = BibTexWriter()
        writer.indent = '  '
        writer.comma_first = False
        
        with open(output_file, 'w', encoding='utf-8') as f:
            bibtexparser.dump(db, f, writer=writer)
        
        print(f"Successfully updated {output_file} with {len(db.entries)} entries")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        if driver:
            driver.quit()

if __name__ == '__main__':
    main()

