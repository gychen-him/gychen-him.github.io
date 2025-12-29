#!/usr/bin/env python3
"""
Fetch BibTeX entries from Google Scholar and update pub.bib
This script uses the scholarly library to fetch publications from Google Scholar.
"""

import os
import sys
import json
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bib_database import BibDatabase
import re

try:
    from scholarly import scholarly
except ImportError:
    print("Error: scholarly library not installed. Install it with: pip install scholarly")
    sys.exit(1)

def normalize_bibtex_entry(entry):
    """Normalize BibTeX entry format"""
    # Ensure required fields exist
    if 'author' not in entry:
        entry['author'] = ''
    if 'title' not in entry:
        entry['title'] = 'Untitled'
    if 'year' not in entry:
        entry['year'] = ''
    
    # Clean up fields
    for key, value in entry.items():
        if isinstance(value, str):
            # Remove extra whitespace
            entry[key] = ' '.join(value.split())
    
    return entry

def fetch_publications_from_scholar(scholar_id):
    """Fetch publications from Google Scholar"""
    print(f"Fetching publications for Google Scholar ID: {scholar_id}")
    
    try:
        # Get author profile
        author = scholarly.fill(scholarly.search_author_id(scholar_id))
        
        publications = []
        
        # Fetch all publications
        print(f"Found {len(author.get('publications', []))} publications")
        
        for pub in author.get('publications', []):
            try:
                # Fill publication details
                filled_pub = scholarly.fill(pub)
                
                # Convert to BibTeX format
                bib_entry = convert_to_bibtex(filled_pub)
                if bib_entry:
                    publications.append(bib_entry)
                    
            except Exception as e:
                print(f"Error processing publication: {e}")
                continue
        
        return publications
        
    except Exception as e:
        print(f"Error fetching from Google Scholar: {e}")
        return []

def convert_to_bibtex(pub):
    """Convert Google Scholar publication to BibTeX format"""
    try:
        entry = {}
        
        # Entry type
        entry_type = 'article'  # Default
        if 'conference' in pub.get('pub_url', '').lower():
            entry_type = 'inproceedings'
        elif 'book' in pub.get('pub_url', '').lower():
            entry_type = 'book'
        
        # Generate entry key
        title = pub.get('bib', {}).get('title', 'untitled')
        year = pub.get('bib', {}).get('pub_year', '')
        first_author = ''
        if pub.get('bib', {}).get('author'):
            first_author = pub['bib']['author'][0].split()[0] if pub['bib']['author'] else ''
        
        entry_key = f"{first_author.lower()}{year}{title[:20].lower().replace(' ', '')}"
        entry_key = re.sub(r'[^a-z0-9]', '', entry_key)
        
        # Required fields
        entry['ENTRYTYPE'] = entry_type
        entry['ID'] = entry_key
        
        # Author
        if pub.get('bib', {}).get('author'):
            authors = pub['bib']['author']
            # Convert to "Last, First" format
            formatted_authors = []
            for author in authors:
                parts = author.split()
                if len(parts) >= 2:
                    last = parts[-1]
                    first = ' '.join(parts[:-1])
                    formatted_authors.append(f"{last}, {first}")
                else:
                    formatted_authors.append(author)
            entry['author'] = ' and '.join(formatted_authors)
        
        # Title
        if pub.get('bib', {}).get('title'):
            entry['title'] = pub['bib']['title']
        
        # Year
        if pub.get('bib', {}).get('pub_year'):
            entry['year'] = str(pub['bib']['pub_year'])
        
        # Journal/Conference
        if pub.get('bib', {}).get('venue'):
            if entry_type == 'inproceedings':
                entry['booktitle'] = pub['bib']['venue']
            else:
                entry['journal'] = pub['bib']['venue']
        
        # Volume, Pages
        if pub.get('bib', {}).get('volume'):
            entry['volume'] = pub['bib']['volume']
        if pub.get('bib', {}).get('pages'):
            entry['pages'] = pub['bib']['pages']
        
        # URL
        if pub.get('pub_url'):
            entry['url'] = pub['pub_url']
        
        # DOI
        if pub.get('eprint_url') and 'doi.org' in pub['eprint_url']:
            entry['doi'] = pub['eprint_url'].split('doi.org/')[-1]
        
        # Citations (for reference)
        if pub.get('num_citations'):
            entry['citations'] = str(pub['num_citations'])
        
        return normalize_bibtex_entry(entry)
        
    except Exception as e:
        print(f"Error converting to BibTeX: {e}")
        return None

def merge_with_existing_bib(existing_file, new_entries):
    """Merge new entries with existing BibTeX file, preserving custom fields"""
    if not os.path.exists(existing_file):
        print(f"Existing file {existing_file} not found, creating new file")
        db = BibDatabase()
        db.entries = new_entries
        return db
    
    # Read existing BibTeX
    with open(existing_file, 'r', encoding='utf-8') as f:
        parser = BibTexParser()
        parser.ignore_nonstandard_types = False
        existing_db = bibtexparser.load(f, parser=parser)
    
    # Create a map of existing entries by title (or other unique identifier)
    existing_map = {}
    for entry in existing_db.entries:
        # Use title as key (normalized)
        title = entry.get('title', '').lower().strip()
        existing_map[title] = entry
    
    # Merge: keep existing entries with custom fields, add new ones
    merged_entries = []
    new_titles = set()
    
    # First, add all existing entries
    for entry in existing_db.entries:
        merged_entries.append(entry)
        title = entry.get('title', '').lower().strip()
        new_titles.add(title)
    
    # Then, add new entries that don't exist
    for entry in new_entries:
        title = entry.get('title', '').lower().strip()
        if title and title not in new_titles:
            merged_entries.append(entry)
            new_titles.add(title)
    
    db = BibDatabase()
    db.entries = merged_entries
    return db

def main():
    # Get Google Scholar ID from environment variable or use default
    scholar_id = os.environ.get('GOOGLE_SCHOLAR_ID', 'AUpqepUAAAAJ')
    output_file = os.environ.get('BIB_OUTPUT_FILE', 'pub.bib')
    
    print(f"Starting BibTeX fetch from Google Scholar...")
    print(f"Scholar ID: {scholar_id}")
    print(f"Output file: {output_file}")
    
    # Fetch publications
    publications = fetch_publications_from_scholar(scholar_id)
    
    if not publications:
        print("No publications found or error occurred")
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

if __name__ == '__main__':
    main()

