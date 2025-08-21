---
permalink: /publications/
title: "Publications"
excerpt: "List of Publications"
author_profile: true
redirect_from: 
  - /publications.html
layout: default
---

<style>
.paper-item {
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.paper-item:last-child {
  border-bottom: none;
}

.paper-title {
  font-size: 1.1em;
  font-weight: 600;
  color: #333;
  margin-bottom: 5px;
  line-height: 1.3;
}

.paper-authors {
  color: #666;
  margin-bottom: 3px;
  font-size: 0.95em;
}

.paper-venue {
  color: #888;
  font-size: 0.9em;
  margin-bottom: 8px;
}

.paper-links {
  margin: 8px 0 0 0;
}

.paper-links a {
  color: #2c5aa0;
  text-decoration: none;
  margin-right: 15px;
  font-size: 0.9em;
}

.paper-links a:hover {
  text-decoration: underline;
}


</style>

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
      fields: fields,
      raw: match[0]
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
        const year = entry.fields.year || 'Unknown year';
        
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
          <div class="paper-venue">${venue}, ${year}</div>
          
          <div class="paper-links">
            ${entry.fields.url ? `<a href="${entry.fields.url}" target="_blank">📄 Paper</a>` : ''}
            ${entry.fields.doi ? `<a href="https://doi.org/${entry.fields.doi}" target="_blank">🔗 DOI</a>` : ''}
          </div>
        `;
        
        container.appendChild(paperDiv);
      });
      
      // Update total count
      document.getElementById('total-count').textContent = entries.length;
      
      // Trigger animations after content is loaded
      setTimeout(() => {
        if (typeof enhancePublicationsAnimation === 'function') {
          enhancePublicationsAnimation();
        }
      }, 100);
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

# 📝 Publications

**Total Publications**: <span id="total-count">Loading...</span> | *For the most up-to-date list, please visit my [Google Scholar profile](https://scholar.google.com/citations?hl=zh-CN&user=AUpqepUAAAAJ&view_op=list_works&sortby=pubdate).*

<div id="publications-container">
  <p>Loading publications...</p>
</div>
