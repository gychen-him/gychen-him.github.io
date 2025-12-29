#!/usr/bin/env python3
"""
Alternative method: Fetch BibTeX from Google Scholar using Selenium
This method is more reliable but requires more setup.
"""

import os
import sys
import time
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bib_database import BibDatabase

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
except ImportError:
    print("Error: selenium library not installed. Install it with: pip install selenium")
    print("Also install ChromeDriver: https://chromedriver.chromium.org/")
    sys.exit(1)

def fetch_bibtex_selenium(scholar_id):
    """Fetch BibTeX from Google Scholar using Selenium"""
    print(f"Fetching BibTeX for Google Scholar ID: {scholar_id}")
    
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    driver = None
    try:
        # Initialize driver
        driver = webdriver.Chrome(options=chrome_options)
        
        # Navigate to Google Scholar profile
        url = f"https://scholar.google.com/citations?user={scholar_id}&hl=en"
        print(f"Accessing: {url}")
        driver.get(url)
        
        # Wait for page to load
        time.sleep(3)
        
        # Try to find and click "Export" or "BibTeX" button
        # Note: Google Scholar's UI may change, this is a template
        try:
            # Look for export options
            export_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Export') or contains(text(), 'BibTeX')]"))
            )
            export_button.click()
            time.sleep(2)
        except:
            print("Could not find export button, trying alternative method...")
            # Alternative: construct BibTeX export URL directly
            bibtex_url = f"https://scholar.google.com/citations?user={scholar_id}&hl=en&cstart=0&pagesize=100"
            driver.get(bibtex_url)
            time.sleep(3)
        
        # Get page source and extract BibTeX
        page_source = driver.page_source
        
        # This is a simplified version - actual implementation would need
        # to parse the HTML and extract BibTeX entries
        print("Note: This is a template. Full implementation would parse HTML to extract BibTeX.")
        print("For production use, consider using the scholarly library method.")
        
        return None
        
    except Exception as e:
        print(f"Error with Selenium method: {e}")
        return None
    finally:
        if driver:
            driver.quit()

if __name__ == '__main__':
    scholar_id = os.environ.get('GOOGLE_SCHOLAR_ID', 'AUpqepUAAAAJ')
    fetch_bibtex_selenium(scholar_id)

