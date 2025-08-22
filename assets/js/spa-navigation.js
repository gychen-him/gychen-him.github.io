/**
 * Single Page Application Navigation
 * Handles dynamic content loading without full page refresh
 */

class SPANavigation {
  constructor() {
    this.contentContainer = document.getElementById('dynamic-content');
    this.pages = {
      '/': '/pages/about-content.html',
      '/publications/': '/pages/publications-content.html',
      '/group/': '/pages/group-content.html'
    };
    
    this.init();
  }

  init() {
    // Bind navigation links
    this.bindNavigationLinks();
    
    // Handle browser back/forward buttons
    window.addEventListener('popstate', (e) => {
      const path = e.state ? e.state.path : window.location.pathname;
      this.loadContent(path, false);
    });
    
    // Load initial content based on current URL
    this.loadInitialContent();
  }

  bindNavigationLinks() {
    const navLinks = document.querySelectorAll('.masthead__menu-item a, .greedy-nav a');
    
    navLinks.forEach(link => {
      // Only bind internal navigation links
      if (link.href && link.href.includes(window.location.origin)) {
        link.addEventListener('click', (e) => {
          e.preventDefault();
          const href = link.getAttribute('href');
          
          // Skip if it's an anchor link on the same page
          if (href.startsWith('#')) {
            return;
          }
          
          this.navigate(href);
        });
      }
    });
  }

  navigate(path) {
    // Update URL without page refresh
    history.pushState({ path: path }, '', path);
    
    // Load content
    this.loadContent(path, true);
    
    // Update active nav state
    this.updateActiveNavigation(path);
  }

  async loadContent(path, animate = true) {
    if (!this.contentContainer) return;
    
    // Add loading state
    if (animate) {
      this.contentContainer.classList.add('content-loading');
    }
    
    try {
      // For now, we'll fetch the actual page content
      const response = await fetch(path);
      
      if (!response.ok) {
        throw new Error(`Failed to load content: ${response.status}`);
      }
      
      const html = await response.text();
      
      // Extract content from the response
      const parser = new DOMParser();
      const doc = parser.parseFromString(html, 'text/html');
      const pageContent = doc.querySelector('.page__content');
      
      if (pageContent) {
        // Small delay for smooth transition
        setTimeout(() => {
          this.contentContainer.innerHTML = pageContent.innerHTML;
          this.contentContainer.classList.remove('content-loading');
          this.contentContainer.classList.add('content-loaded');
          
          // Scroll to top of content
          this.contentContainer.scrollTop = 0;
        }, animate ? 150 : 0);
      }
      
    } catch (error) {
      console.error('Error loading content:', error);
      this.contentContainer.innerHTML = '<p>Error loading content. Please try again.</p>';
      this.contentContainer.classList.remove('content-loading');
    }
  }

  loadInitialContent() {
    const currentPath = window.location.pathname;
    this.loadContent(currentPath, false);
    this.updateActiveNavigation(currentPath);
  }

  updateActiveNavigation(path) {
    // Remove active class from all nav links
    const allNavLinks = document.querySelectorAll('.masthead__menu-item a');
    allNavLinks.forEach(link => link.classList.remove('active'));
    
    // Add active class to current page link
    const activeLink = document.querySelector(`a[href="${path}"]`);
    if (activeLink) {
      activeLink.classList.add('active');
    }
  }
}

// Initialize SPA navigation when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  new SPANavigation();
});