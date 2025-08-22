---
permalink: /publications/
title: "Publications"
excerpt: "Publications List"
author_profile: true
redirect_from:
  - /publications.html
layout: spa
---

# 📝 Publications

**Total Publications**: <span id="total-count">Loading...</span> published papers

<div id="publications-loading" style="text-align: center; padding: 2em;">
  <p>Loading publications...</p>
</div>

<div id="publications-container"></div>

---

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

// Format authors in Chicago style and bold my name
function formatAuthors(authorsString) {
  if (!authorsString) return 'Unknown authors';
  
  // Split authors by 'and' and clean up
  const authors = authorsString.split(' and ').map(author => author.trim());
  
  // Format each author (Last, First Middle)
  const formattedAuthors = authors.map(author => {
    // Handle different name formats
    let formatted = author;
    
    // If author contains comma, it's already in "Last, First" format
    if (author.includes(',')) {
      formatted = author;
    } else {
      // Split by spaces and rearrange to "Last, First"
      const parts = author.split(' ');
      if (parts.length >= 2) {
        const lastName = parts[parts.length - 1];
        const firstNames = parts.slice(0, -1).join(' ');
        formatted = `${lastName}, ${firstNames}`;
      }
    }
    
    // Bold my name (check for various formats)
    if (formatted.toLowerCase().includes('guangyong') && formatted.toLowerCase().includes('chen')) {
      formatted = `<strong>${formatted}</strong>`;
    }
    
    return formatted;
  });
  
  // Join with Chicago style formatting
  if (formattedAuthors.length === 1) {
    return formattedAuthors[0];
  } else if (formattedAuthors.length === 2) {
    return `${formattedAuthors[0]}, and ${formattedAuthors[1]}`;
  } else {
    const lastAuthor = formattedAuthors[formattedAuthors.length - 1];
    const otherAuthors = formattedAuthors.slice(0, -1);
    return `${otherAuthors.join(', ')}, and ${lastAuthor}`;
  }
}

// Format citation in Chicago style
function formatChicagoCitation(entry) {
  const title = entry.fields.title || 'Untitled';
  const authors = formatAuthors(entry.fields.author);
  const year = entry.fields.year || 'n.d.';
  
  let citation = `${authors}. "${title}."`;
  
  if (entry.fields.journal) {
    // Journal article
    const journal = entry.fields.journal;
    const volume = entry.fields.volume;
    const number = entry.fields.number;
    const pages = entry.fields.pages;
    
    citation += ` <em>${journal}</em>`;
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
    
    citation += ` In <em>${booktitle}</em>`;
    if (pages) {
      citation += `, ${pages}`;
    }
    citation += `. ${year}.`;
    
  } else if (entry.fields.publisher) {
    // Book or other publication
    const publisher = entry.fields.publisher;
    citation += ` ${publisher}, ${year}.`;
  } else {
    citation += ` ${year}.`;
  }
  
  return citation;
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
          
          const venue = getVenueDisplay(entry);
          const venueClass = getVenueBadge(venue);
          const chicagoCitation = formatChicagoCitation(entry);
          
          paperDiv.innerHTML = `
            <div class="paper-number">${groupedByYear[year].length - index}</div>
            <div class="paper-content">
              ${venue ? `<div class="paper-badge ${venueClass}">${venue}</div>` : ''}
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