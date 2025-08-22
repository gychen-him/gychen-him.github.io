/**
 * Simple SPA Navigation System
 * Updates only the content area without refreshing the entire page
 */

class SPANavigation {
  constructor() {
    this.contentArea = document.querySelector('.spa-content');
    this.navLinks = document.querySelectorAll('.masthead__menu-item a, .greedy-nav a');
    this.currentPath = window.location.pathname;
    
    // Debug logging
    console.log('SPA Navigation initialized');
    console.log('Content area found:', !!this.contentArea);
    console.log('Navigation links found:', this.navLinks.length);
    
    this.init();
  }

  init() {
    this.bindNavigationLinks();
    this.updateActiveNavigation();
    
    // Handle browser back/forward buttons
    window.addEventListener('popstate', (e) => {
      this.loadContent(window.location.pathname, false);
    });
  }

    bindNavigationLinks() {
    // Get all navigation links including the homepage link
    const allNavLinks = document.querySelectorAll('.masthead__menu-item a, .greedy-nav a');
    
    allNavLinks.forEach(link => {
      const href = link.getAttribute('href');

      // Skip external links, anchor links, and mailto links
      if (!href || href.startsWith('http') || href.startsWith('#') || href.startsWith('mailto:')) {
        return;
      }

      // Only bind to internal page links
      const internalPages = ['/', '/publications/', '/group/'];
      if (internalPages.includes(href)) {
        console.log('Binding SPA navigation to:', href);
        link.addEventListener('click', (e) => {
          e.preventDefault();
          this.navigate(href);
        });
      }
    });
  }

  navigate(path) {
    // Don't navigate if already on the same page
    if (path === this.currentPath) {
      return;
    }
    
    // Update browser URL
    history.pushState({ path: path }, '', path);
    
    // Load new content
    this.loadContent(path, true);
    
    // Update current path
    this.currentPath = path;
  }

  async loadContent(path, animate = true) {
    if (!this.contentArea) {
      // Fallback: if SPA fails, do a normal page load
      window.location.href = path;
      return;
    }

    try {
      // Add loading state
      if (animate) {
        this.contentArea.style.opacity = '0.7';
        this.contentArea.style.transform = 'translateY(10px)';
      }

      // Fetch the new page
      const response = await fetch(path);
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const html = await response.text();
      
      // Parse the response and extract content
      const parser = new DOMParser();
      const newDoc = parser.parseFromString(html, 'text/html');
      const newContent = newDoc.querySelector('.spa-content');
      
      if (newContent) {
        // Small delay for smooth transition
        setTimeout(() => {
          // Update content
          this.contentArea.innerHTML = newContent.innerHTML;
          
          // Update page title
          const newTitle = newDoc.querySelector('title');
          if (newTitle) {
            document.title = newTitle.textContent;
          }
          
          // Update active navigation
          this.updateActiveNavigation();
          
          // Remove loading state
          this.contentArea.style.opacity = '1';
          this.contentArea.style.transform = 'translateY(0)';
          
          // Scroll to top of content
          this.contentArea.scrollTop = 0;
          
          // Re-run any scripts that might be needed (like MathJax)
          this.initializeContentScripts();
          
        }, animate ? 150 : 0);
      } else {
        throw new Error('Content not found');
      }

    } catch (error) {
      console.error('SPA navigation error:', error);
      // Fallback: do a normal page load
      window.location.href = path;
    }
  }

  updateActiveNavigation() {
    // Remove active class from all navigation links
    this.navLinks.forEach(link => {
      link.classList.remove('current');
      link.parentElement.classList.remove('current');
    });
    
    // Add active class to current page link
    const currentLink = document.querySelector(`.greedy-nav a[href="${this.currentPath}"]`) ||
                       document.querySelector(`.greedy-nav a[href="${this.currentPath.replace(/\/$/, '')}"]`);
    
    if (currentLink) {
      currentLink.classList.add('current');
      currentLink.parentElement.classList.add('current');
    }
  }

  initializeContentScripts() {
    // Re-initialize MathJax if present
    if (window.MathJax && window.MathJax.typesetPromise) {
      window.MathJax.typesetPromise([this.contentArea]).catch((err) => {
        console.log('MathJax typeset error:', err);
      });
    }
    
    // Re-initialize any other scripts that might be needed
    // (Google Scholar stats, etc.)
    if (window.initializeGoogleScholarStats) {
      window.initializeGoogleScholarStats();
    }
    
    // Execute page-specific scripts
    const scripts = this.contentArea.querySelectorAll('script');
    scripts.forEach(script => {
      if (script.innerHTML.trim()) {
        try {
          // Create a new script element and execute it
          const newScript = document.createElement('script');
          newScript.innerHTML = script.innerHTML;
          document.head.appendChild(newScript);
          document.head.removeChild(newScript);
        } catch (error) {
          console.error('Error executing script:', error);
        }
      }
    });
  }
}

// Initialize SPA navigation when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  new SPANavigation();
});

// Add smooth transitions
document.addEventListener('DOMContentLoaded', () => {
  const contentArea = document.querySelector('.spa-content');
  if (contentArea) {
    contentArea.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
  }
});
