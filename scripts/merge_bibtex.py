#!/usr/bin/env python3
"""
Merge BibTeX files while preserving custom fields from the existing file.
Useful for manually merging exported BibTeX from Google Scholar.
"""

import sys
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bib_database import BibDatabase

def merge_bibtex_files(new_file, existing_file, output_file=None):
    """Merge new BibTeX entries with existing file, preserving custom fields"""
    if output_file is None:
        output_file = existing_file
    
    # Read existing file
    print(f"Reading existing file: {existing_file}")
    with open(existing_file, 'r', encoding='utf-8') as f:
        parser = BibTexParser()
        parser.ignore_nonstandard_types = False
        existing_db = bibtexparser.load(f, parser=parser)
    
    # Read new file
    print(f"Reading new file: {new_file}")
    with open(new_file, 'r', encoding='utf-8') as f:
        parser = BibTexParser()
        parser.ignore_nonstandard_types = False
        new_db = bibtexparser.load(f, parser=parser)
    
    # Create map of existing entries by normalized title
    existing_map = {}
    for entry in existing_db.entries:
        title = entry.get('title', '').lower().strip()
        if title:
            existing_map[title] = entry
    
    # Merge entries
    merged_entries = []
    new_titles = set()
    
    # Add all existing entries first
    for entry in existing_db.entries:
        merged_entries.append(entry)
        title = entry.get('title', '').lower().strip()
        if title:
            new_titles.add(title)
    
    # Add new entries that don't exist, or update existing ones
    added_count = 0
    updated_count = 0
    
    for new_entry in new_db.entries:
        title = new_entry.get('title', '').lower().strip()
        if title in existing_map:
            # Entry exists, update basic fields but preserve custom fields
            existing_entry = existing_map[title]
            
            # Update basic fields
            for key in ['author', 'title', 'year', 'journal', 'booktitle', 'volume', 'pages', 'url', 'doi']:
                if key in new_entry:
                    existing_entry[key] = new_entry[key]
            
            updated_count += 1
        elif title:
            # New entry, add it
            merged_entries.append(new_entry)
            new_titles.add(title)
            added_count += 1
    
    # Write merged file
    db = BibDatabase()
    db.entries = merged_entries
    
    writer = BibTexWriter()
    writer.indent = '  '
    writer.comma_first = False
    
    print(f"Writing merged file: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        bibtexparser.dump(db, f, writer=writer)
    
    print(f"\nMerge complete!")
    print(f"  Total entries: {len(merged_entries)}")
    print(f"  Added: {added_count}")
    print(f"  Updated: {updated_count}")
    print(f"  Preserved: {len(existing_db.entries) - updated_count}")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python merge_bibtex.py <new_file.bib> <existing_file.bib> [output_file.bib]")
        print("\nExample:")
        print("  python merge_bibtex.py exported.bib pub.bib")
        print("  python merge_bibtex.py exported.bib pub.bib pub_merged.bib")
        sys.exit(1)
    
    new_file = sys.argv[1]
    existing_file = sys.argv[2]
    output_file = sys.argv[3] if len(sys.argv) > 3 else None
    
    merge_bibtex_files(new_file, existing_file, output_file)

