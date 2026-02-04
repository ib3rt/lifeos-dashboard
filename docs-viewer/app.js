/**
 * Life OS Docs Viewer - Application Logic
 */

(function() {
    'use strict';

    // ============================================
    // State Management
    // ============================================
    const state = {
        index: null,
        fileTree: [],
        expandedFolders: new Set(),
        activeFile: null,
        searchQuery: '',
        searchResults: [],
        isSidebarCollapsed: false,
        theme: localStorage.getItem('docs-theme') || 'light'
    };

    // ============================================
    // DOM Elements
    // ============================================
    const elements = {
        sidebar: document.getElementById('sidebar'),
        toggleSidebar: document.getElementById('toggleSidebar'),
        searchInput: document.getElementById('searchInput'),
        searchResults: document.getElementById('searchResults'),
        fileTree: document.getElementById('fileTree'),
        document: document.getElementById('document'),
        breadcrumbs: document.getElementById('breadcrumbs'),
        themeToggle: document.getElementById('themeToggle'),
        mobileOverlay: document.getElementById('mobileOverlay')
    };

    // ============================================
    // Initialization
    // ============================================
    async function init() {
        // Apply theme
        document.documentElement.setAttribute('data-theme', state.theme);
        
        // Load index
        await loadIndex();
        
        // Render file tree
        renderFileTree();
        
        // Setup event listeners
        setupEventListeners();
        
        // Check for hash in URL
        handleHashChange();
        
        // Load recent file if available
        loadRecentFile();
    }

    async function loadIndex() {
        try {
            const response = await fetch('search-index.json');
            if (!response.ok) throw new Error('Failed to load index');
            state.index = await response.json();
            state.fileTree = state.index.fileTree || [];
            
            // Load expanded folders from localStorage
            const saved = localStorage.getItem('docs-expanded-folders');
            if (saved) {
                try {
                    JSON.parse(saved).forEach(f => state.expandedFolders.add(f));
                } catch(e) {}
            }
        } catch (error) {
            console.error('Failed to load search index:', error);
            elements.fileTree.innerHTML = '<div class="tree-loading">Failed to load files</div>';
        }
    }

    // ============================================
    // File Tree Rendering
    // ============================================
    function renderFileTree() {
        if (!state.fileTree.length) {
            elements.fileTree.innerHTML = '<div class="tree-loading">No documents found</div>';
            return;
        }
        
        const container = document.createElement('div');
        container.className = 'tree-root';
        
        state.fileTree.forEach(node => {
            container.appendChild(createTreeNode(node, ''));
        });
        
        elements.fileTree.innerHTML = '';
        elements.fileTree.appendChild(container);
    }

    function createTreeNode(node, path) {
        const nodeEl = document.createElement('div');
        nodeEl.className = `tree-node ${node.type}`;
        nodeEl.dataset.path = path + (path ? '/' : '') + node.name;
        
        const content = document.createElement('div');
        content.className = 'tree-node-content';
        
        if (node.type === 'folder') {
            const isExpanded = state.expandedFolders.has(node.path);
            
            content.innerHTML = `
                <span class="tree-toggle ${isExpanded ? 'expanded' : ''}">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="9 18 15 12 9 6"></polyline>
                    </svg>
                </span>
                <span class="tree-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path>
                    </svg>
                </span>
                <span class="tree-label">${node.name}</span>
            `;
            
            const children = document.createElement('div');
            children.className = `tree-children ${isExpanded ? 'expanded' : ''}`;
            
            if (node.children) {
                node.children.forEach(child => {
                    children.appendChild(createTreeNode(child, node.path));
                });
            }
            
            nodeEl.appendChild(content);
            nodeEl.appendChild(children);
            
            // Folder click handler
            content.addEventListener('click', (e) => {
                e.stopPropagation();
                toggleFolder(node.path, children, content.querySelector('.tree-toggle'));
            });
        } else {
            content.innerHTML = `
                <span class="tree-toggle" style="visibility: hidden;">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="9 18 15 12 9 6"></polyline>
                    </svg>
                </span>
                <span class="tree-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                        <polyline points="14 2 14 8 20 8"></polyline>
                    </svg>
                </span>
                <span class="tree-label">${node.name}</span>
            `;
            
            nodeEl.appendChild(content);
            
            // File click handler
            content.addEventListener('click', () => {
                loadDocument(node.path);
            });
        }
        
        return nodeEl;
    }

    function toggleFolder(path, childrenEl, toggleEl) {
        const isExpanded = childrenEl.classList.contains('expanded');
        
        if (isExpanded) {
            childrenEl.classList.remove('expanded');
            toggleEl.classList.remove('expanded');
            state.expandedFolders.delete(path);
        } else {
            childrenEl.classList.add('expanded');
            toggleEl.classList.add('expanded');
            state.expandedFolders.add(path);
        }
        
        // Save to localStorage
        localStorage.setItem('docs-expanded-folders', JSON.stringify([...state.expandedFolders]));
    }

    // ============================================
    // Document Loading
    // ============================================
    async function loadDocument(path) {
        // Update active state in tree
        document.querySelectorAll('.tree-node-content').forEach(el => {
            el.classList.remove('active');
            if (el.parentElement.dataset.path === path) {
                el.classList.add('active');
            }
        });
        
        // Save as recent
        localStorage.setItem('docs-recent-file', path);
        
        // Show loading
        elements.document.innerHTML = '<div class="loading-spinner"></div>';
        
        try {
            const response = await fetch(path);
            if (!response.ok) throw new Error('Document not found');
            
            const content = await response.text();
            renderDocument(path, content);
            updateBreadcrumbs(path);
            
            // Update URL hash
            history.pushState({ path }, '', `#${encodeURIComponent(path)}`);
            
        } catch (error) {
            elements.document.innerHTML = `
                <div class="document-placeholder">
                    <div class="placeholder-icon">
                        <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                            <circle cx="12" cy="12" r="10"></circle>
                            <line x1="12" y1="8" x2="12" y2="12"></line>
                            <line x1="12" y1="16" x2="12.01" y2="16"></line>
                        </svg>
                    </div>
                    <h2>Document not found</h2>
                    <p>${error.message}</p>
                </div>
            `;
        }
    }

    function renderDocument(path, content) {
        // Configure marked
        marked.setOptions({
            highlight: function(code, lang) {
                if (Prism.languages[lang]) {
                    return Prism.highlight(code, Prism.languages[lang], lang);
                }
                return code;
            },
            breaks: true,
            gfm: true
        });
        
        // Render markdown
        const html = marked.parse(content);
        
        elements.document.innerHTML = `
            <div class="markdown-body fade-in">
                ${html}
            </div>
        `;
        
        // Re-highlight code blocks
        elements.document.querySelectorAll('pre code').forEach(block => {
            Prism.highlightElement(block);
        });
        
        // Handle internal links
        elements.document.querySelectorAll('a').forEach(link => {
            const href = link.getAttribute('href');
            if (href && href.endsWith('.md')) {
                link.addEventListener('click', (e) => {
                    e.preventDefault();
                    const relPath = resolvePath(path, href);
                    loadDocument(relPath);
                });
            }
        });
        
        state.activeFile = path;
    }

    function updateBreadcrumbs(path) {
        const parts = path.split('/');
        let html = `<a href="#" class="breadcrumb-item" data-path="">Home</a>`;
        
        let currentPath = '';
        parts.forEach((part, i) => {
            currentPath = currentPath ? `${currentPath}/${part}` : part;
            const isLast = i === parts.length - 1;
            
            if (isLast) {
                html += `<span class="breadcrumb-separator">/</span><span class="breadcrumb-item">${part}</span>`;
            } else {
                html += `<span class="breadcrumb-separator">/</span><a href="#" class="breadcrumb-item" data-path="${currentPath}">${part}</a>`;
            }
        });
        
        elements.breadcrumbs.innerHTML = html;
        
        // Add click handlers
        elements.breadcrumbs.querySelectorAll('.breadcrumb-item[data-path]').forEach(el => {
            el.addEventListener('click', (e) => {
                e.preventDefault();
                const path = el.dataset.path;
                if (path) {
                    scrollToFolder(path);
                }
            });
        });
    }

    function scrollToFolder(path) {
        const node = document.querySelector(`.tree-node[data-path="${path}"]`);
        if (node) {
            // Expand all parent folders
            let parent = node.parentElement;
            while (parent) {
                if (parent.classList.contains('tree-children')) {
                    parent.classList.add('expanded');
                    const toggle = parent.previousElementSibling?.querySelector('.tree-toggle');
                    if (toggle) toggle.classList.add('expanded');
                    
                    const folderPath = parent.previousElementSibling?.parentElement?.dataset.path;
                    if (folderPath) state.expandedFolders.add(folderPath);
                }
                parent = parent.parentElement;
            }
            
            // Scroll to node
            const content = node.querySelector('.tree-node-content');
            if (content) {
                content.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
        }
    }

    // ============================================
    // Search
    // ============================================
    function setupSearch() {
        const query = state.searchQuery.toLowerCase();
        
        if (!query || !state.index) {
            elements.searchResults.classList.remove('active');
            return;
        }
        
        // Search in file metadata and content
        const results = state.index.files.filter(file => {
            return file.title.toLowerCase().includes(query) ||
                   file.path.toLowerCase().includes(query) ||
                   (file.excerpt && file.excerpt.toLowerCase().includes(query));
        }).slice(0, 20); // Limit results
        
        if (results.length === 0) {
            elements.searchResults.innerHTML = `
                <div class="search-result-item">
                    <div class="search-result-title">No results found</div>
                </div>
            `;
            elements.searchResults.classList.add('active');
            return;
        }
        
        // Render results
        elements.searchResults.innerHTML = results.map((file, i) => {
            const highlightedTitle = highlightMatch(file.title, query);
            const path = file.path;
            const excerpt = file.excerpt || '';
            const highlightedExcerpt = excerpt ? highlightMatch(excerpt, query) : '';
            
            return `
                <div class="search-result-item ${i === 0 ? 'highlighted' : ''}" data-path="${file.path}">
                    <div class="search-result-title">${highlightedTitle}</div>
                    <div class="search-result-path">${path}</div>
                    ${highlightedExcerpt ? `<div class="search-result-excerpt">${highlightedExcerpt}</div>` : ''}
                </div>
            `;
        }).join('');
        
        elements.searchResults.classList.add('active');
        
        // Add click handlers
        elements.searchResults.querySelectorAll('.search-result-item').forEach(item => {
            item.addEventListener('click', () => {
                loadDocument(item.dataset.path);
                clearSearch();
            });
        });
    }

    function highlightMatch(text, query) {
        const regex = new RegExp(`(${escapeRegex(query)})`, 'gi');
        return text.replace(regex, '<mark>$1</mark>');
    }

    function escapeRegex(str) {
        return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    function clearSearch() {
        elements.searchInput.value = '';
        state.searchQuery = '';
        elements.searchResults.classList.remove('active');
    }

    // ============================================
    // Theme Toggle
    // ============================================
    function toggleTheme() {
        state.theme = state.theme === 'light' ? 'dark' : 'light';
        document.documentElement.setAttribute('data-theme', state.theme);
        localStorage.setItem('docs-theme', state.theme);
    }

    // ============================================
    // Sidebar Toggle
    // ============================================
    function toggleSidebar() {
        state.isSidebarCollapsed = !state.isSidebarCollapsed;
        elements.sidebar.classList.toggle('collapsed', state.isSidebarCollapsed);
        localStorage.setItem('docs-sidebar-collapsed', state.isSidebarCollapsed);
    }

    // ============================================
    // URL Hash Handling
    // ============================================
    function handleHashChange() {
        const hash = window.location.hash.slice(1);
        if (hash) {
            try {
                const path = decodeURIComponent(hash);
                loadDocument(path);
            } catch (e) {
                console.error('Invalid hash:', hash);
            }
        }
    }

    // ============================================
    // Recent File
    // ============================================
    function loadRecentFile() {
        const recent = localStorage.getItem('docs-recent-file');
        if (recent && !window.location.hash) {
            loadDocument(recent);
        }
    }

    // ============================================
    // Utility Functions
    // ============================================
    function resolvePath(currentPath, relativePath) {
        const parts = currentPath.split('/');
        parts.pop();
        
        const relativeParts = relativePath.split('/');
        
        relativeParts.forEach(part => {
            if (part === '..') {
                parts.pop();
            } else if (part !== '.') {
                parts.push(part);
            }
        });
        
        return parts.join('/');
    }

    // ============================================
    // Event Listeners
    // ============================================
    function setupEventListeners() {
        // Sidebar toggle
        elements.toggleSidebar.addEventListener('click', toggleSidebar);
        
        // Theme toggle
        elements.themeToggle.addEventListener('click', toggleTheme);
        
        // Search
        let searchTimeout;
        elements.searchInput.addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                state.searchQuery = e.target.value;
                setupSearch();
            }, 200);
        });
        
        // Close search on escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                clearSearch();
                elements.searchInput.blur();
            }
            // Cmd/Ctrl + K for search
            if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
                e.preventDefault();
                elements.searchInput.focus();
            }
        });
        
        // Click outside search to close
        document.addEventListener('click', (e) => {
            if (!elements.searchInput.contains(e.target) && 
                !elements.searchResults.contains(e.target)) {
                clearSearch();
            }
        });
        
        // Keyboard navigation in search
        elements.searchInput.addEventListener('keydown', (e) => {
            const results = elements.searchResults.querySelectorAll('.search-result-item');
            const current = elements.searchResults.querySelector('.highlighted');
            const currentIndex = current ? [...results].indexOf(current) : -1;
            
            if (e.key === 'ArrowDown') {
                e.preventDefault();
                const next = results[currentIndex + 1] || results[0];
                if (current) current.classList.remove('highlighted');
                next.classList.add('highlighted');
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                const prev = results[currentIndex - 1] || results[results.length - 1];
                if (current) current.classList.remove('highlighted');
                prev.classList.add('highlighted');
            } else if (e.key === 'Enter' && current) {
                e.preventDefault();
                loadDocument(current.dataset.path);
                clearSearch();
            }
        });
        
        // Hash change
        window.addEventListener('hashchange', handleHashChange);
        
        // Popstate
        window.addEventListener('popstate', handleHashChange);
        
        // Mobile overlay click
        elements.mobileOverlay.addEventListener('click', () => {
            elements.sidebar.classList.remove('mobile-open');
            elements.mobileOverlay.classList.remove('active');
        });
    }

    // ============================================
    // Start Application
    // ============================================
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
