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
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 30px;
  background: #fafafa;
}

.paper-title {
  font-size: 1.2em;
  font-weight: bold;
  color: #2c5aa0;
  margin-bottom: 10px;
}

.paper-authors {
  font-style: italic;
  margin-bottom: 8px;
}

.paper-venue {
  font-weight: bold;
  color: #666;
  margin-bottom: 10px;
}

.paper-links {
  margin: 15px 0;
}

.paper-links a {
  display: inline-block;
  margin-right: 15px;
  padding: 5px 12px;
  background: #2c5aa0;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  font-size: 0.9em;
}

.paper-links a:hover {
  background: #1e3d6f;
  color: white;
}

.bibtex-container {
  margin-top: 15px;
}

.bibtex-toggle {
  background: #666;
  color: white;
  border: none;
  padding: 5px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9em;
}

.bibtex-content {
  display: none;
  background: #f5f5f5;
  border: 1px solid #ddd;
  padding: 15px;
  margin-top: 10px;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  font-size: 0.85em;
  white-space: pre-wrap;
  overflow-x: auto;
}
</style>

<script>
function toggleBibtex(id) {
  var content = document.getElementById('bibtex-' + id);
  var button = document.getElementById('btn-' + id);
  if (content.style.display === 'none' || content.style.display === '') {
    content.style.display = 'block';
    button.textContent = 'Hide BibTeX';
  } else {
    content.style.display = 'none';
    button.textContent = 'Show BibTeX';
  }
}

function copyBibtex(id) {
  var content = document.getElementById('bibtex-' + id);
  navigator.clipboard.writeText(content.textContent).then(function() {
    alert('BibTeX copied to clipboard!');
  });
}

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
          
          <div class="bibtex-container">
            <button class="bibtex-toggle" id="btn-${index}" onclick="toggleBibtex(${index})">Show BibTeX</button>
            <button class="bibtex-toggle" onclick="copyBibtex(${index})" style="margin-left: 5px;">Copy BibTeX</button>
            <div class="bibtex-content" id="bibtex-${index}">${entry.raw}</div>
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

# 📝 Publications

<div id="publications-container">
  <p>Loading publications...</p>
</div>

---

**Total Publications**: <span id="total-count">Loading...</span>

*For the most up-to-date list, please visit my [Google Scholar profile](https://scholar.google.com/citations?hl=zh-CN&user=AUpqepUAAAAJ&view_op=list_works&sortby=pubdate).*
