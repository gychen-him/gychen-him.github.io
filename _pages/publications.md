---
permalink: /publications/
title: "Publications"
excerpt: "Selected Publications and Research Overview"
author_profile: true
redirect_from:
  - /publications.html
layout: spa
---

# 📝 Publications

## 🔬 Research Overview

My research focuses on developing next-generation computational tools for medical AI and drug discovery. The work follows a comprehensive pipeline from clinical data processing to therapeutic design:

<div class="research-pipeline">
  <div class="pipeline-step">
    <div class="step-icon">🏥</div>
    <div class="step-content">
      <h4>Clinical Data Processing</h4>
      <p>Multimodal clinical information analysis</p>
    </div>
  </div>
  
  <div class="pipeline-arrow">→</div>
  
  <div class="pipeline-step">
    <div class="step-icon">🔍</div>
    <div class="step-content">
      <h4>Disease Mechanism Discovery</h4>
      <p>AI-driven biomarker identification</p>
    </div>
  </div>
  
  <div class="pipeline-arrow">→</div>
  
  <div class="pipeline-step">
    <div class="step-icon">🧬</div>
    <div class="step-content">
      <h4>Therapeutic Design</h4>
      <p>Targeted drug development & optimization</p>
    </div>
  </div>
</div>

---

## 📚 Publications

<div id="publications-loading" style="text-align: center; padding: 2em;">
  <p>Loading publications...</p>
</div>

<div id="publications-container"></div>

### Key Research Areas

<div class="research-areas">
  <div class="research-area">
    <h4>🧠 Large Language Models for Drug Discovery</h4>
    <p>Applying LLMs to accelerate pharmaceutical research and development processes</p>
  </div>
  
  <div class="research-area">
    <h4>🔬 Protein Representation Learning</h4>
    <p>Advanced neural architectures for protein structure and function prediction</p>
  </div>
  
  <div class="research-area">
    <h4>💊 Molecular Generation & Optimization</h4>
    <p>AI-driven design of novel therapeutic compounds with desired properties</p>
  </div>
  
  <div class="research-area">
    <h4>🎯 Drug-Target Interaction Prediction</h4>
    <p>Computational methods for predicting and optimizing drug-protein interactions</p>
  </div>
</div>

---

## 📚 Complete Publication List

**Total Publications**: <span id="total-count">Loading...</span> published papers

<div class="scholar-stats">
  <div class="stat-item">
    <div class="stat-number">2600+</div>
    <div class="stat-label">Citations</div>
  </div>
  <div class="stat-item">
    <div class="stat-number" id="paper-count">Loading...</div>
    <div class="stat-label">Papers</div>
  </div>
  <div class="stat-item">
    <div class="stat-number">High</div>
    <div class="stat-label">Impact</div>
  </div>
</div>

For a complete and up-to-date list including preprints, please visit my [**Google Scholar profile**](https://scholar.google.com/citations?hl=zh-CN&user=AUpqepUAAAAJ&view_op=list_works&sortby=pubdate).

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

// Get venue badge class based on venue name
function getVenueBadge(venue) {
  const venueUpper = venue.toUpperCase();
  
  if (venueUpper.includes('NATURE')) {
    return 'nature';
  } else if (venueUpper.includes('NEURIPS') || venueUpper.includes('NIPS')) {
    return 'neurips';
  } else if (venueUpper.includes('ICML')) {
    return 'icml';
  } else if (venueUpper.includes('ICLR')) {
    return 'iclr';
  } else if (venueUpper.includes('AAAI') || venueUpper.includes('IJCAI')) {
    return 'ai-conference';
  } else if (venueUpper.includes('BIOINFORMATICS') || venueUpper.includes('BMC') || venueUpper.includes('PLOS')) {
    return 'bio-journal';
  } else if (venueUpper.includes('IEEE') || venueUpper.includes('ACM')) {
    return 'cs-journal';
  }
  return 'other';
}

// Check if entry is arXiv preprint
function isArxivPreprint(entry) {
  const venue = entry.fields.journal || entry.fields.booktitle || entry.fields.publisher || '';
  return venue.toLowerCase().includes('arxiv') || 
         (entry.fields.eprint && entry.fields.eprint.includes('arxiv'));
}

// Get venue display name
function getVenueDisplay(entry) {
  if (entry.fields.journal) {
    return entry.fields.journal;
  } else if (entry.fields.booktitle) {
    return entry.fields.booktitle;
  } else if (entry.fields.publisher) {
    return entry.fields.publisher;
  }
  return '';
}

// Render publications from BibTeX
function renderPublications() {
  fetch('/pub.bib')
    .then(response => response.text())
    .then(bibtexText => {
      const entries = parseBibtex(bibtexText);
      
      // Filter out arXiv preprints
      const publishedEntries = entries.filter(entry => !isArxivPreprint(entry));
      
      // Group by year
      const groupedByYear = {};
      publishedEntries.forEach(entry => {
        const year = parseInt(entry.fields.year) || 'Unknown';
        if (!groupedByYear[year]) {
          groupedByYear[year] = [];
        }
        groupedByYear[year].push(entry);
      });
      
      // Sort years (newest first)
      const sortedYears = Object.keys(groupedByYear).sort((a, b) => {
        if (a === 'Unknown') return 1;
        if (b === 'Unknown') return -1;
        return parseInt(b) - parseInt(a);
      });
      
      const container = document.getElementById('publications-container');
      const loadingDiv = document.getElementById('publications-loading');
      loadingDiv.style.display = 'none';
      container.innerHTML = '';
      
      sortedYears.forEach(year => {
        // Create year section
        const yearSection = document.createElement('div');
        yearSection.className = 'year-section';
        
        const yearHeader = document.createElement('h3');
        yearHeader.className = 'year-header';
        yearHeader.innerHTML = `📅 ${year} <span class="year-count">(${groupedByYear[year].length} papers)</span>`;
        yearSection.appendChild(yearHeader);
        
        const yearPapers = document.createElement('div');
        yearPapers.className = 'year-papers';
        
        groupedByYear[year].forEach((entry, index) => {
          const paperDiv = document.createElement('div');
          paperDiv.className = 'publication-item';
          
          const title = entry.fields.title || 'Untitled';
          const authors = entry.fields.author || 'Unknown authors';
          const venue = getVenueDisplay(entry);
          const venueClass = getVenueBadge(venue);
          
          paperDiv.innerHTML = `
            <div class="paper-number">${groupedByYear[year].length - index}</div>
            <div class="paper-content">
              ${venue ? `<div class="paper-badge ${venueClass}">${venue}</div>` : ''}
              <div class="paper-title">${title}</div>
              <div class="paper-authors">${authors}</div>
              
              <div class="paper-links">
                ${entry.fields.url ? `<a href="${entry.fields.url}" target="_blank">📄 Paper</a>` : ''}
                ${entry.fields.doi ? `<a href="https://doi.org/${entry.fields.doi}" target="_blank">🔗 DOI</a>` : ''}
                ${entry.fields.code ? `<a href="${entry.fields.code}" target="_blank">💻 Code</a>` : ''}
              </div>
            </div>
          `;
          
          yearPapers.appendChild(paperDiv);
        });
        
        yearSection.appendChild(yearPapers);
        container.appendChild(yearSection);
      });
      
      // Update counts
      document.getElementById('total-count').textContent = publishedEntries.length;
      document.getElementById('paper-count').textContent = publishedEntries.length;
    })
    .catch(error => {
      console.error('Error loading BibTeX file:', error);
      const loadingDiv = document.getElementById('publications-loading');
      loadingDiv.innerHTML = '<p>Error loading publications. Please check if pub.bib file is accessible.</p>';
    });
}

// Load publications when page loads
document.addEventListener('DOMContentLoaded', renderPublications);
</script>