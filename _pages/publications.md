---
permalink: /publications/
title: "Publications"
excerpt: "List of Publications"
author_profile: true
redirect_from: 
  - /publications.html
layout: spa
---

# 📝 Publications

**Total Publications**: <span id="total-count">Loading...</span> | *For the most up-to-date list, please visit my [Google Scholar profile](https://scholar.google.com/citations?hl=zh-CN&user=AUpqepUAAAAJ&view_op=list_works&sortby=pubdate).*

<div id="publications-container">
  <p>Loading publications...</p>
</div>

<script>
// Parse BibTeX content
function parseBibtex(bibtexText) {
  const entries = [];
  const regex = /@(\w+)\s*\{\s*([^,]+),\s*([\s\S]*?)\n\}/g;
  let match;
  
  while ((match = regex.exec(bibtexText)) !== null) {
    const [, type, key, fieldsStr] = match;
    const fields = {};
    
    // Parse fields
    const fieldRegex = /(\w+)\s*=\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}|(\w+)\s*=\s*"([^"]*)"/g;
    let fieldMatch;
    
    while ((fieldMatch = fieldRegex.exec(fieldsStr)) !== null) {
      const fieldName = fieldMatch[1] || fieldMatch[3];
      const fieldValue = fieldMatch[2] || fieldMatch[4];
      if (fieldName && fieldValue) {
        fields[fieldName.toLowerCase()] = fieldValue.trim();
      }
    }
    
    entries.push({
      type: type.toLowerCase(),
      key: key.trim(),
      fields: fields
    });
  }
  
  return entries;
}

// Render publications
function renderPublications() {
  fetch('/pub.bib')
    .then(response => response.text())
    .then(bibtexText => {
      const entries = parseBibtex(bibtexText);
      
      // Sort by year (newest first)
      entries.sort((a, b) => {
        const yearA = parseInt(a.fields.year) || 0;
        const yearB = parseInt(b.fields.year) || 0;
        return yearB - yearA;
      });
      
      const container = document.getElementById('publications-container');
      container.innerHTML = '';
      
      entries.forEach((entry, index) => {
        const paperDiv = document.createElement('div');
        paperDiv.className = 'paper-item';
        
        const title = entry.fields.title || 'Untitled';
        const authors = entry.fields.author || 'Unknown authors';
        const year = entry.fields.year || '';
        
        let venue = '';
        if (entry.fields.journal) {
          venue = entry.fields.journal;
        } else if (entry.fields.booktitle) {
          venue = entry.fields.booktitle;
        } else if (entry.fields.publisher) {
          venue = entry.fields.publisher;
        }
        
        paperDiv.innerHTML = `
          <div class="paper-title">${title}</div>
          <div class="paper-authors">${authors}</div>
          <div class="paper-venue">${venue}${year ? ', ' + year : ''}</div>
          
          <div class="paper-links">
            ${entry.fields.url ? `<a href="${entry.fields.url}" target="_blank">📄 Paper</a>` : ''}
            ${entry.fields.doi ? `<a href="https://doi.org/${entry.fields.doi}" target="_blank">🔗 DOI</a>` : ''}
          </div>
        `;
        
        container.appendChild(paperDiv);
      });
      
      // Update total count
      document.getElementById('total-count').textContent = entries.length;
    })
    .catch(error => {
      console.error('Error loading BibTeX file:', error);
      document.getElementById('publications-container').innerHTML = 
        '<p>Error loading publications. Please check if pub.bib file is accessible.</p>';
    });
}

// Load publications when page loads
document.addEventListener('DOMContentLoaded', renderPublications);
</script>