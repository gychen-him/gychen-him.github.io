---
permalink: /publications/
title: "Publications"
excerpt: "Publications List"
author_profile: true
redirect_from:
  - /publications.html
layout: spa
---

# Publications

**Total Publications**: <span id="total-count">Loading...</span> published papers

<div id="publications-loading" style="text-align: center; padding: 2em;">
  <p>Loading publications...</p>
</div>

<div id="publications-container"></div>

---

For a complete and up-to-date list including preprints, please visit my [**Google Scholar profile**](https://scholar.google.com/citations?hl=zh-CN&user=AUpqepUAAAAJ&view_op=list_works&sortby=pubdate).

<script>
// Normalize author name from various formats to "First Last"
function normalizeAuthorName(authorName) {
  authorName = authorName.trim();
  
  if (authorName.includes(',')) {
    // Handle "Last, First" format
    const parts = authorName.split(',');
    if (parts.length === 2) {
      const lastName = parts[0].trim();
      const firstName = parts[1].trim();
      
      // Normalize case
      const normalizedLast = normalizeCase(lastName);
      const normalizedFirst = normalizeCase(firstName);
      
      return `${normalizedFirst} ${normalizedLast}`;
    }
  }
  
  // Already in "First Last" format, just normalize case
  return normalizeCase(authorName);
}

// Normalize case of names (handle ALL CAPS -> Proper Case)
function normalizeCase(name) {
  if (name === name.toUpperCase()) {
    // Handle ALL CAPS case
    return name.split('-').map(part => 
      part.charAt(0) + part.slice(1).toLowerCase()
    ).join('-');
  }
  return name; // Keep existing case
}

// Normalize author field string
function normalizeAuthors(authorString) {
  if (!authorString) return authorString;
  
  // Split by 'and' (case insensitive)
  const authors = authorString.split(/\s+and\s+/i);
  
  // Normalize each author
  const normalizedAuthors = authors.map(author => normalizeAuthorName(author));
  
  // Join back with ' and '
  return normalizedAuthors.join(' and ');
}

// Parse BibTeX content with automatic author normalization
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
      let fieldValue = fieldMatch[2] || fieldMatch[4];
      
      if (fieldName && fieldValue) {
        fieldValue = fieldValue.trim();
        
        // Auto-normalize author field
        if (fieldName.toLowerCase() === 'author') {
          fieldValue = normalizeAuthors(fieldValue);
        }
        
        fields[fieldName.toLowerCase()] = fieldValue;
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

// Get research category badge from BibTeX field
function getCategoryBadge(entry) {
  const category = entry.fields.category;
  if (!category) return null;
  
  const categoryLower = category.toLowerCase();
  if (categoryLower.includes('ai') || categoryLower.includes('artificial intelligence') || categoryLower.includes('machine learning')) {
    return { class: 'ai-category', text: 'AI' };
  } else if (categoryLower.includes('science') || categoryLower.includes('biology') || categoryLower.includes('medicine') || categoryLower.includes('chemistry')) {
    return { class: 'science-category', text: 'Science' };
  }
  return null;
}

// Check if entry is preprint (arXiv or bioRxiv)
function isPreprint(entry) {
  const venue = entry.fields.journal || entry.fields.booktitle || entry.fields.publisher || '';
  const venueLower = venue.toLowerCase();
  
  return venueLower.includes('arxiv') || 
         venueLower.includes('biorxiv') ||
         venueLower.includes('bioarxiv') ||
         (entry.fields.eprint && (entry.fields.eprint.includes('arxiv') || entry.fields.eprint.includes('biorxiv')));
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

// Parse author names from "Last, First" format
function parseAuthorName(authorString) {
  const trimmed = authorString.trim();
  if (trimmed.includes(',')) {
    const [last, first] = trimmed.split(',').map(p => p.trim());
    return { last, first, full: `${first} ${last}`, original: trimmed };
  } else {
    // If no comma, assume "First Last" format
    const parts = trimmed.split(' ');
    const last = parts[parts.length - 1];
    const first = parts.slice(0, -1).join(' ');
    return { last, first, full: trimmed, original: trimmed };
  }
}

// Check if two authors match (compare both last and first names)
function authorsMatch(author1, author2) {
  const parsed1 = parseAuthorName(author1);
  const parsed2 = parseAuthorName(author2);
  
  return parsed1.last.toLowerCase() === parsed2.last.toLowerCase() && 
         parsed1.first.toLowerCase() === parsed2.first.toLowerCase();
}

// Format authors in Chicago style with special markings
function formatAuthors(authorsString, entry) {
  if (!authorsString) return 'Unknown authors';
  
  // Parse cofirst and corresponding fields
  // These contain authors in same format as main author field: "Last1, First1 and Last2, First2"
  const cofirstAuthors = entry.fields.cofirst ? 
    entry.fields.cofirst.split(' and ').map(author => author.trim()) : [];
  const correspondingAuthors = entry.fields.corresponding ? 
    entry.fields.corresponding.split(' and ').map(author => author.trim()) : [];
  
  // Split authors by 'and'
  const authors = authorsString.split(' and ').map(author => author.trim());
  
  console.log('Debug - Authors:', authors);
  console.log('Debug - Cofirst:', cofirstAuthors);
  console.log('Debug - Corresponding:', correspondingAuthors);
  
  // Format each author
  const formattedAuthors = authors.map((author, index) => {
    const parsed = parseAuthorName(author);
    let displayName = parsed.full; // Display as "First Last"
    
    // Check if this author is co-first
    const isCoFirst = cofirstAuthors.some(cofirstAuthor => authorsMatch(author, cofirstAuthor));
    
    // Check if this author is corresponding
    const isCorresponding = correspondingAuthors.some(corrAuthor => authorsMatch(author, corrAuthor));
    
    console.log(`Debug - Author "${author}": coFirst=${isCoFirst}, corresponding=${isCorresponding}`);
    
    // Bold my name
    if (parsed.last.toLowerCase() === 'chen' && parsed.first.toLowerCase().includes('guangyong')) {
      displayName = `<strong>${displayName}</strong>`;
    }
    
    // Add markers
    let markers = '';
    if (isCoFirst) {
      markers += '<sup class="author-marker cofirst">†</sup>';
    }
    if (isCorresponding) {
      markers += '<sup class="author-marker corresponding">*</sup>';
    }
    
    return displayName + markers;
  });
  
  // Join with Chicago style formatting
  let result;
  if (formattedAuthors.length === 1) {
    result = formattedAuthors[0];
  } else if (formattedAuthors.length === 2) {
    result = `${formattedAuthors[0]}, and ${formattedAuthors[1]}`;
  } else {
    const lastAuthor = formattedAuthors[formattedAuthors.length - 1];
    const otherAuthors = formattedAuthors.slice(0, -1);
    result = `${otherAuthors.join(', ')}, and ${lastAuthor}`;
  }
  
  // Add legend if there are special authors
  let legend = '';
  if (cofirstAuthors.length > 0 || correspondingAuthors.length > 0) {
    const legendParts = [];
    if (cofirstAuthors.length > 0) {
      legendParts.push('<sup class="author-marker cofirst">†</sup> Co-first author');
    }
    if (correspondingAuthors.length > 0) {
      legendParts.push('<sup class="author-marker corresponding">*</sup> Corresponding author');
    }
    legend = `<div class="author-legend">${legendParts.join(', ')}</div>`;
  }
  
  return result + legend;
}

// Format citation in Chicago style with proper formatting
function formatChicagoCitation(entry) {
  const title = entry.fields.title || 'Untitled';
  const authors = formatAuthors(entry.fields.author, entry);
  const year = entry.fields.year || 'n.d.';
  
  // Start with authors (without period here since legend might be included)
  let citation = `<div class="citation-authors">${authors}</div>`;
  
  // Add title on new line
  citation += `<div class="citation-title">"${title}."</div>`;
  
  // Add venue information
  citation += '<div class="citation-venue">';
  
  if (entry.fields.journal) {
    // Journal article
    const journal = entry.fields.journal;
    const volume = entry.fields.volume;
    const number = entry.fields.number;
    const pages = entry.fields.pages;
    
    citation += `<em><strong>${journal}</strong></em>`;
    if (volume) {
      citation += ` ${volume}`;
      if (number) {
        citation += `, no. ${number}`;
      }
    }
    citation += ` (${year})`;
    if (pages) {
      citation += `: ${pages}`;
    }
    citation += '.';
    
  } else if (entry.fields.booktitle) {
    // Conference paper
    const booktitle = entry.fields.booktitle;
    const pages = entry.fields.pages;
    
    citation += `In <em><strong>${booktitle}</strong></em>`;
    if (pages) {
      citation += `, ${pages}`;
    }
    citation += `. ${year}.`;
    
  } else if (entry.fields.publisher) {
    // Book or other publication
    const publisher = entry.fields.publisher;
    citation += `<strong>${publisher}</strong>, ${year}.`;
  } else {
    citation += `${year}.`;
  }
  
  citation += '</div>';
  
  return citation;
}

// Render publications from BibTeX
function renderPublications() {
  fetch('/pub.bib')
    .then(response => response.text())
    .then(bibtexText => {
      const entries = parseBibtex(bibtexText);
      
      // Filter out preprints (arXiv and bioRxiv)
      const publishedEntries = entries.filter(entry => !isPreprint(entry));
      
      // Group by year (skip entries without valid year)
      const groupedByYear = {};
      publishedEntries.forEach(entry => {
        const year = parseInt(entry.fields.year);
        if (year && year > 1900) { // Only include valid years
          if (!groupedByYear[year]) {
            groupedByYear[year] = [];
          }
          groupedByYear[year].push(entry);
        }
      });
      
      // Sort years (newest first)
      const sortedYears = Object.keys(groupedByYear).sort((a, b) => parseInt(b) - parseInt(a));
      
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
        yearHeader.innerHTML = `${year} <span class="year-count">(${groupedByYear[year].length} papers)</span>`;
        yearSection.appendChild(yearHeader);
        
        const yearPapers = document.createElement('div');
        yearPapers.className = 'year-papers';
        
        groupedByYear[year].forEach((entry, index) => {
          const paperDiv = document.createElement('div');
          paperDiv.className = 'publication-item';
          
          const categoryBadge = getCategoryBadge(entry);
          const chicagoCitation = formatChicagoCitation(entry);
          
          paperDiv.innerHTML = `
            ${categoryBadge ? `<div class="category-badge ${categoryBadge.class}">${categoryBadge.text}</div>` : ''}
            <div class="paper-number">${groupedByYear[year].length - index}</div>
            <div class="paper-content">
              <div class="chicago-citation">${chicagoCitation}</div>
              
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