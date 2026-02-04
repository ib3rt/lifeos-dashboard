/**
 * Life OS Docs Viewer - Application Logic
 */

(function() {
    'use strict';

    // ============================================
    // Configuration
    // ============================================
    // Base path for markdown files relative to docs-viewer location
    const MARKDOWN_BASE_PATH = '../';

    // ============================================
    // Error Handling
    // ============================================
    const ERROR_TYPES = {
        NETWORK: 'network',
        NOT_FOUND: 'not_found',
        PARSE: 'parse',
        STORAGE: 'storage',
        RENDER: 'render',
        CORS: 'cors',
        UNKNOWN: 'unknown'
    };

    // Error messages mapping
    const ERROR_MESSAGES = {
        [ERROR_TYPES.NETWORK]: 'Unable to connect. Please check your internet connection.',
        [ERROR_TYPES.NOT_FOUND]: 'File not found. It may have been moved or deleted.',
        [ERROR_TYPES.PARSE]: 'Unable to load content. Please try again.',
        [ERROR_TYPES.STORAGE]: 'Storage full. Please clear some data.',
        [ERROR_TYPES.RENDER]: 'Unable to display content. The file format may be invalid.',
        [ERROR_TYPES.CORS]: 'Cross-origin access denied. Please check server permissions.',
        [ERROR_TYPES.UNKNOWN]: 'An unexpected error occurred. Please try again.'
    };

    // Track last action for retry
    let lastAction = null;
    let lastActionArgs = null;
    let lastActionContext = null;

    // Set the last action for retry functionality
    function setLastAction(action, args, context) {
        lastAction = action;
        lastActionArgs = args || [];
        lastActionContext = context || null;
    }

    // Retry the last failed action
    function retryLastAction() {
        if (lastAction && typeof lastAction === 'function') {
            console.log('Retrying last action...');
            try {
                if (lastActionContext) {
                    lastAction.apply(lastActionContext, lastActionArgs);
                } else {
                    lastAction(...lastActionArgs);
                }
            } catch (error) {
                console.error('Retry failed:', error);
                handleError(error, ERROR_TYPES.UNKNOWN);
            }
        }
    }

    // Report error to console for logging
    function reportError(type) {
        const errorReport = {
            type: type,
            timestamp: new Date().toISOString(),
            userAgent: navigator.userAgent,
            url: window.location.href
        };
        console.group('Error Report');
        console.log('Type:', type);
        console.log('Report:', errorReport);
        console.groupEnd();
        
        // Could be extended to send to error tracking service
        alert(`Error reported: ${type}\nThank you for your feedback!`);
    }

    // Main error handler
    function handleError(error, type = ERROR_TYPES.UNKNOWN) {
        console.error(`Error [${type}]:`, error);
        
        const errorMessage = ERROR_MESSAGES[type] || ERROR_MESSAGES[ERROR_TYPES.UNKNOWN];
        
        const html = `
            <div class="error-state fade-in">
                <div class="error-icon">
                    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10"></circle>
                        <line x1="12" y1="8" x2="12" y2="12"></line>
                        <line x1="12" y1="16" x2="12.01" y2="16"></line>
                    </svg>
                </div>
                <div class="error-message">${errorMessage}</div>
                <div class="error-actions">
                    <button class="retry-btn" onclick="retryLastAction()">Retry</button>
                    <button class="report-btn" onclick="reportError('${type}')">Report Issue</button>
                </div>
            </div>
        `;
        
        if (elements.document) {
            elements.document.innerHTML = html;
        }
        
        return { type, message: errorMessage, originalError: error };
    }

    // Detect error type from error object
    function detectErrorType(error) {
        if (!error) return ERROR_TYPES.UNKNOWN;
        
        const message = (error.message || '').toLowerCase();
        const name = error.name || '';
        
        if (name === 'QuotaExceededError' || message.includes('quota') || message.includes('storage')) {
            return ERROR_TYPES.STORAGE;
        }
        
        if (message.includes('network') || message.includes('fetch') || message.includes('Failed to fetch')) {
            return ERROR_TYPES.NETWORK;
        }
        
        if (error.status === 404 || message.includes('404') || message.includes('not found')) {
            return ERROR_TYPES.NOT_FOUND;
        }
        
        if (message.includes('cors') || message.includes('cross-origin') || message.includes('access-control')) {
            return ERROR_TYPES.CORS;
        }
        
        if (message.includes('json') || message.includes('parse') || message.includes('syntaxerror')) {
            return ERROR_TYPES.PARSE;
        }
        
        if (message.includes('render') || message.includes('markdown') || message.includes('parse')) {
            return ERROR_TYPES.RENDER;
        }
        
        return ERROR_TYPES.UNKNOWN;
    }

    // Safe fetch wrapper with error handling
    async function safeFetch(url, options = {}) {
        try {
            const response = await fetch(url, options);
            
            if (!response.ok) {
                if (response.status === 404) {
                    throw new Error(`File not found: ${url}`);
                } else if (response.status === 403) {
                    throw new Error(`Access denied: ${url}`);
                } else {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
            }
            
            return response;
        } catch (error) {
            const type = detectErrorType(error);
            handleError(error, type);
            throw error;
        }
    }

    // Safe JSON parse wrapper
    function safeParse(jsonString, fallback = null) {
        try {
            return JSON.parse(jsonString);
        } catch (error) {
            handleError(error, ERROR_TYPES.PARSE);
            return fallback;
        }
    }

    // Safe markdown render wrapper
    function safeRenderMarkdown(content) {
        try {
            marked.use({
                gfm: true,
                breaks: true,
                headerIds: true,
                mangle: false
            });

            const renderer = new marked.Renderer();
            const originalCode = renderer.code.bind(renderer);

            renderer.code = function(code, language) {
                const validLanguage = language && Prism.languages[language] ? language : 'plaintext';
                const highlighted = Prism.highlight(code, Prism.languages[validLanguage], validLanguage);
                return `<pre><code class="language-${validLanguage}">${highlighted}</code></pre>`;
            };

            marked.setOptions({ renderer });

            return marked.parse(content);
        } catch (error) {
            handleError(error, ERROR_TYPES.RENDER);
            throw error;
        }
    }

    // ============================================
    // localStorage Helper Functions
    // ============================================
    const storage = {
        get: function(key, defaultValue = null) {
            try {
                const value = localStorage.getItem(key);
                if (value === null) return defaultValue;
                return safeParse(value, defaultValue);
            } catch (e) {
                console.warn(`localStorage get failed for "${key}":`, e);
                handleError(e, detectErrorType(e));
                return defaultValue;
            }
        },
        
        set: function(key, value) {
            try {
                localStorage.setItem(key, JSON.stringify(value));
                return true;
            } catch (e) {
                console.warn(`localStorage set failed for "${key}":`, e);
                const type = detectErrorType(e);
                handleError(e, type);
                if (type === ERROR_TYPES.STORAGE) {
                    // Try to clear old data and retry
                    this.clearExpired();
                    try {
                        localStorage.setItem(key, JSON.stringify(value));
                        return true;
                    } catch (e2) {
                        console.error('localStorage quota exceeded, cannot save:', key);
                        handleError(e2, ERROR_TYPES.STORAGE);
                    }
                }
                return false;
            }
        },
        
        remove: function(key) {
            try {
                localStorage.removeItem(key);
                return true;
            } catch (e) {
                console.warn(`localStorage remove failed for "${key}":`, e);
                return false;
            }
        },
        
        clearExpired: function() {
            // Clear recent files if too many (keep last 10)
            try {
                const recentFiles = this.get('docs-recent-files', []);
                if (recentFiles.length > 10) {
                    this.set('docs-recent-files', recentFiles.slice(-10));
                }
            } catch (e) {
                // Ignore errors during cleanup
            }
        }
    };

    // ============================================
    // Default State for New Users
    // ============================================
    const defaultState = {
        theme: 'dark',
        expandedFolders: [],
        recentFiles: [],
        sidebarCollapsed: false,
        searchHistory: [],
        lastFile: null,
        scrollPosition: { x: 0, y: 0 }
    };

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
        isSidebarCollapsed: storage.get('docs-sidebar-collapsed', defaultState.sidebarCollapsed),
        theme: storage.get('docs-theme', defaultState.theme),
        recentFiles: storage.get('docs-recent-files', defaultState.recentFiles),
        searchHistory: storage.get('docs-search-history', defaultState.searchHistory),
        lastFile: storage.get('docs-last-file', defaultState.lastFile)
    };

    // ============================================
    // DOM Elements
    // ============================================
    const elements = {
        sidebar: document.getElementById('sidebar'),
        toggleSidebar: document.getElementById('toggleSidebar'),
        mobileMenuBtn: document.getElementById('mobileMenuBtn'),
        searchInput: document.getElementById('searchInput'),
        searchResults: document.getElementById('searchResults'),
        fileTree: document.getElementById('fileTree'),
        document: document.getElementById('document'),
        breadcrumbs: document.getElementById('breadcrumbs'),
        themeToggle: document.getElementById('themeToggle'),
        mobileOverlay: document.getElementById('mobileOverlay'),
        recentFilesSection: document.getElementById('recentFilesSection'),
        recentFilesList: document.getElementById('recentFilesList'),
        clearRecentBtn: document.getElementById('clearRecentBtn')
    };

    // ============================================
    // Initialization
    // ============================================
    async function init() {
        // Apply theme
        document.documentElement.setAttribute('data-theme', state.theme);
        
        // Load sidebar state
        if (state.isSidebarCollapsed) {
            elements.sidebar.classList.add('collapsed');
        }
        
        // Load index
        await loadIndex();
        
        // Render file tree
        renderFileTree();
        
        // Setup event listeners
        setupEventListeners();
        
        // Setup hash routing and browser history
        setupHashRouting();
        
        // Render recent files
        renderRecentFiles();
    }

    async function loadIndex() {
        // Set up retry for index loading
        setLastAction(loadIndex, [], null);
        
        try {
            const response = await safeFetch('search-index.json');
            if (!response.ok) {
                throw new Error('Failed to load index');
            }
            
            const indexData = await response.json();
            state.index = indexData;
            
            // Convert flat files array to tree structure
            state.fileTree = buildFileTree(state.index.files || []);
            
            // Load expanded folders from localStorage using storage helper
            const savedFolders = storage.get('docs-expanded', []);
            savedFolders.forEach(f => state.expandedFolders.add(f));
            
        } catch (error) {
            console.error('Failed to load search index:', error);
            elements.fileTree.innerHTML = '<div class="tree-loading">Failed to load files</div>';
            handleError(error, detectErrorType(error));
        }
    }

    // Convert flat file list to tree structure
    function buildFileTree(files) {
        const root = [];

        files.forEach(file => {
            const parts = file.path.split('/');
            let currentPath = '';
            let currentLevel = root;

            parts.forEach((part, index) => {
                currentPath = currentPath ? `${currentPath}/${part}` : part;
                const isFile = index === parts.length - 1;

                let existing = currentLevel.find(n => n.name === part && n.type === (isFile ? 'file' : 'folder'));
                if (!existing) {
                    existing = {
                        name: part,
                        path: currentPath,
                        type: isFile ? 'file' : 'folder',
                        children: isFile ? undefined : []
                    };
                    currentLevel.push(existing);
                }

                if (!isFile) {
                    currentLevel = existing.children;
                }
            });
        });

        return root;
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
        nodeEl.dataset.name = node.name;
        
        const content = document.createElement('div');
        content.className = 'tree-node-content';
        content.setAttribute('role', 'button');
        content.setAttribute('tabindex', '0');
        
        if (node.type === 'folder') {
            const isExpanded = state.expandedFolders.has(node.path);
            if (isExpanded) {
                nodeEl.classList.add('expanded');
            }
            
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
            const childrenInner = document.createElement('div');
            childrenInner.className = 'tree-children-inner';
            
            if (node.children && node.children.length > 0) {
                node.children.forEach(child => {
                    childrenInner.appendChild(createTreeNode(child, node.path));
                });
            }
            
            children.appendChild(childrenInner);
            nodeEl.appendChild(content);
            nodeEl.appendChild(children);
            
            // Folder click handler
            const toggleHandler = (e) => {
                e.stopPropagation();
                toggleFolder(node.path, children, content.querySelector('.tree-toggle'), nodeEl);
            };
            
            content.addEventListener('click', toggleHandler);
            
            // Keyboard navigation
            content.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    toggleHandler(e);
                }
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
            
            // Keyboard navigation for files
            content.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    loadDocument(node.path);
                }
            });
        }
        
        return nodeEl;
    }

    function toggleFolder(path, childrenEl, toggleEl, nodeEl) {
        const isExpanded = childrenEl.classList.contains('expanded');
        
        if (isExpanded) {
            childrenEl.classList.remove('expanded');
            toggleEl.classList.remove('expanded');
            if (nodeEl) nodeEl.classList.remove('expanded');
            state.expandedFolders.delete(path);
        } else {
            childrenEl.classList.add('expanded');
            toggleEl.classList.add('expanded');
            if (nodeEl) nodeEl.classList.add('expanded');
            state.expandedFolders.add(path);
        }
        
        // Save to localStorage
        saveExpandedState();
    }
    
    function saveExpandedState() {
        storage.set('docs-expanded', [...state.expandedFolders]);
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
        
        // Save to recent files (limit to 10, most recent first)
        addToRecentFiles(path);
        
        // Show loading
        elements.document.innerHTML = '<div class="loading-spinner"></div>';
        
        // Resolve path using configured base path
        const fetchPath = MARKDOWN_BASE_PATH + path;
        
        // Set up retry for document loading
        setLastAction(loadDocument, [path], null);
        
        try {
            const response = await safeFetch(fetchPath);
            if (!response.ok) {
                throw new Error(`Document not found: ${path}`);
            }
            
            const content = await response.text();
            await renderDocument(path, content);
            updateBreadcrumbs(path);
            
            // Update URL hash
            history.pushState({ path }, '', `#${encodeURIComponent(path)}`);
            
        } catch (error) {
            elements.document.innerHTML = '';
            handleError(error, detectErrorType(error));
        }
    }

    function addToRecentFiles(path) {
        // Get file title from path
        const title = path.split('/').pop();
        
        // Load existing recent files with full info
        let recentFiles = storage.get('docs-recent-files', []);
        
        // Remove if already exists
        recentFiles = recentFiles.filter(f => f.path !== path);
        
        // Add to beginning with title and timestamp
        recentFiles.unshift({
            path: path,
            title: title,
            accessed: Date.now()
        });
        
        // Keep only last 10
        if (recentFiles.length > 10) {
            recentFiles = recentFiles.slice(0, 10);
        }
        
        // Save to localStorage
        storage.set('docs-recent-files', recentFiles);
        state.recentFiles = recentFiles;
        
        // Update UI
        renderRecentFiles();
    }

    async function renderDocument(path, content) {
        try {
            // Get file extension
            const ext = path.split('.').pop().toLowerCase();
            
            // Get appropriate handler based on extension
            const handler = getFileTypeHandler(ext);
            
            // Render content using handler
            const html = await handler(path, content);
            
            // Determine wrapper class based on file type
            let wrapperClass = 'markdown-body';
            if (ext === 'json') wrapperClass = 'json-body';
            else if (ext === 'txt') wrapperClass = 'text-body';
            else if (['yml', 'yaml', 'py', 'js', 'ts', 'jsx', 'tsx', 'css', 'html', 'sh', 'bash', 'sql', 'java', 'c', 'cpp', 'cs', 'go', 'rs', 'rb', 'php', 'swift', 'kt', 'lua', 'r', 'rust', 'dockerfile', 'ini', 'cfg', 'conf', 'env', 'gitignore', 'gitattributes']) {
                wrapperClass = 'code-body';
            } else if (ext === 'mdx') wrapperClass = 'markdown-body';

            elements.document.innerHTML = `
                <div class="${wrapperClass} fade-in">
                    ${html}
                </div>
            `;
            
            // Handle internal links for markdown files
            if (ext === 'md' || ext === 'mdx') {
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
                
                // Handle TOC links
                elements.document.querySelectorAll('.toc a').forEach(link => {
                    link.addEventListener('click', (e) => {
                        e.preventDefault();
                        const targetId = link.getAttribute('href').replace('#', '');
                        const targetEl = document.getElementById(targetId);
                        if (targetEl) {
                            targetEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
                        }
                    });
                });
            }
            
            // Apply syntax highlighting
            Prism.highlightAll();
            
            state.activeFile = path;
        } catch (error) {
            handleError(error, ERROR_TYPES.RENDER);
        }
    }

    function updateBreadcrumbs(path) {
        // Handle root/home case - show single Home breadcrumb
        if (!path || path === '') {
            elements.breadcrumbs.innerHTML = `<span class="breadcrumb-item current">🏠 Home</span>`;
            return;
        }
        
        const parts = path.split('/');
        let html = `<a href="#" class="breadcrumb-item" data-path="">🏠 Home</a>`;
        
        let currentPath = '';
        parts.forEach((part, i) => {
            currentPath = currentPath ? `${currentPath}/${part}` : part;
            const isLast = i === parts.length - 1;
            
            if (isLast) {
                // Last segment - show as current (non-clickable)
                html += `<span class="breadcrumb-separator">/</span><span class="breadcrumb-item current">${part}</span>`;
            } else {
                // Intermediate segment - clickable folder link
                html += `<span class="breadcrumb-separator">/</span><a href="#" class="breadcrumb-item" data-path="${currentPath}">${part}</a>`;
            }
        });
        
        elements.breadcrumbs.innerHTML = html;
        
        // Add click handlers for breadcrumb navigation
        elements.breadcrumbs.querySelectorAll('.breadcrumb-item[data-path]').forEach(el => {
            el.addEventListener('click', (e) => {
                e.preventDefault();
                const targetPath = el.dataset.path;
                if (targetPath === '') {
                    // Home clicked - reset to root view
                    resetToRoot();
                } else {
                    // Folder clicked - expand and scroll to it
                    scrollToFolder(targetPath);
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
            
            // Save expanded state
            saveExpandedState();
            
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
            const filePath = file.path;
            const excerpt = file.excerpt || '';
            const highlightedExcerpt = excerpt ? highlightMatch(excerpt, query) : '';
            
            return `
                <div class="search-result-item ${i === 0 ? 'highlighted' : ''}" data-path="${filePath}">
                    <div class="search-result-title">${highlightedTitle}</div>
                    <div class="search-result-path">${filePath}</div>
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
        const query = state.searchQuery.trim();
        
        // Add to search history if not empty and not already in history
        if (query && !state.searchHistory.includes(query)) {
            state.searchHistory.unshift(query);
            // Keep only last 10 searches
            if (state.searchHistory.length > 10) {
                state.searchHistory = state.searchHistory.slice(0, 10);
            }
            storage.set('docs-search-history', state.searchHistory);
        }
        
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
        storage.set('docs-theme', state.theme);
    }

    // ============================================
    // Sidebar Toggle
    // ============================================
    function toggleSidebar() {
        state.isSidebarCollapsed = !state.isSidebarCollapsed;
        elements.sidebar.classList.toggle('collapsed', state.isSidebarCollapsed);
        storage.set('docs-sidebar-collapsed', state.isSidebarCollapsed);
    }

    // ============================================
    // Hash Routing & Deep Linking
    // ============================================
    function setupHashRouting() {
        // Listen for hash changes (when user clicks links or manually changes hash)
        window.addEventListener('hashchange', handleHashChange);
        
        // Listen for browser back/forward navigation
        window.addEventListener('popstate', handlePopState);
        
        // Check for hash in URL and load document if present
        // This handles direct links and page reloads with hash
        if (window.location.hash) {
            handleHashChange();
        }
    }
    
    function handleHashChange() {
        const hash = window.location.hash.slice(1);
        if (hash) {
            try {
                const path = decodeURIComponent(hash);
                loadDocument(path);
            } catch (e) {
                console.error('Invalid hash:', hash);
                showFileTree();
            }
        } else {
            // No hash - show file tree (home view)
            showFileTree();
        }
    }
    
    function handlePopState(event) {
        // Handle browser back/forward button navigation
        if (event.state && event.state.path) {
            loadDocument(event.state.path);
        } else {
            // No state - check for hash or show home
            if (window.location.hash) {
                handleHashChange();
            } else {
                showFileTree();
            }
        }
    }
    
    function showFileTree() {
        // Reset to file tree view without loading a document
        state.activeFile = null;
        
        // Clear active state in tree
        document.querySelectorAll('.tree-node-content').forEach(el => {
            el.classList.remove('active');
        });
        
        // Update breadcrumbs to show only Home
        elements.breadcrumbs.innerHTML = `<span class="breadcrumb-item current">🏠 Home</span>`;
        
        // Show placeholder
        elements.document.innerHTML = `
            <div class="document-placeholder">
                <div class="empty-state">
                    <div class="icon">
                        <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                            <polyline points="14 2 14 8 20 8"></polyline>
                            <line x1="16" y1="13" x2="8" y2="13"></line>
                            <line x1="16" y1="17" x2="8" y2="17"></line>
                            <polyline points="10 9 9 9 8 9"></polyline>
                        </svg>
                    </div>
                    <div class="title">Select a document to view</div>
                    <div class="description">Choose a markdown file from the sidebar to read</div>
                </div>
            </div>
        `;
    }

    // ============================================
    // Recent File
    // ============================================
    function loadRecentFile() {
        // Use the new array format, get most recent
        const recentFile = state.recentFiles.length > 0 ? state.recentFiles[0] : null;
        if (recentFile && !window.location.hash) {
            loadDocument(recentFile.path);
        }
    }

    // ============================================
    // Recent Files UI
    // ============================================
    function renderRecentFiles() {
        const recentFiles = state.recentFiles || [];
        const section = elements.recentFilesSection;
        const list = elements.recentFilesList;
        
        if (recentFiles.length === 0) {
            section.style.display = 'none';
            return;
        }
        
        section.style.display = 'block';
        
        list.innerHTML = recentFiles.map((file, index) => {
            const isActive = file.path === state.activeFile;
            return `
                <div class="recent-file-item ${isActive ? 'active' : ''}" data-path="${file.path}">
                    <svg class="recent-file-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                        <polyline points="14 2 14 8 20 8"></polyline>
                    </svg>
                    <span class="recent-file-title">${escapeHtml(file.title)}</span>
                </div>
            `;
        }).join('');
        
        // Add click handlers
        list.querySelectorAll('.recent-file-item').forEach(item => {
            item.addEventListener('click', () => {
                loadDocument(item.dataset.path);
            });
        });
    }

    function clearRecentFiles() {
        state.recentFiles = [];
        storage.set('docs-recent-files', []);
        renderRecentFiles();
    }

    function resetToRoot() {
        // Collapse all expanded folders
        state.expandedFolders.clear();
        saveExpandedState();
        
        // Re-render file tree to show collapsed state
        renderFileTree();
        
        // Reset URL hash
        history.pushState({}, '', window.location.pathname);
        
        // Clear active file
        state.activeFile = null;
        
        // Show placeholder
        elements.document.innerHTML = `
            <div class="document-placeholder">
                <div class="placeholder-icon">
                    <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                        <polyline points="14 2 14 8 20 8"></polyline>
                        <line x1="16" y1="13" x2="8" y2="13"></line>
                        <line x1="16" y1="17" x2="8" y2="17"></line>
                        <polyline points="10 9 9 9 8 9"></polyline>
                    </svg>
                </div>
                <h2>Select a document to view</h2>
                <p>Choose a markdown file from the sidebar to read</p>
            </div>
        `;
        
        // Update breadcrumbs to show only Home
        elements.breadcrumbs.innerHTML = `<span class="breadcrumb-item current">🏠 Home</span>`;
        
        // Clear active state in tree
        document.querySelectorAll('.tree-node-content').forEach(el => {
            el.classList.remove('active');
        });
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

    // Escape HTML for safe rendering
    function escapeHtml(str) {
        if (!str) return '';
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    // ============================================
    // Tree Keyboard Navigation
    // ============================================
    let focusedNodeIndex = -1;
    let allTreeNodes = [];

    function updateTreeNodes() {
        allTreeNodes = Array.from(elements.fileTree.querySelectorAll('.tree-node-content'));
    }

    function navigateTree(direction) {
        updateTreeNodes();
        
        if (allTreeNodes.length === 0) return;
        
        // Find currently focused element
        const focused = document.activeElement;
        const isInTree = focused && focused.classList.contains('tree-node-content');
        const currentIndex = isInTree ? allTreeNodes.indexOf(focused) : -1;
        
        let nextIndex;
        
        if (direction === 'ArrowDown') {
            nextIndex = currentIndex < allTreeNodes.length - 1 ? currentIndex + 1 : 0;
        } else if (direction === 'ArrowUp') {
            nextIndex = currentIndex > 0 ? currentIndex - 1 : allTreeNodes.length - 1;
        } else if (direction === 'ArrowRight') {
            if (isInTree) {
                const nodeEl = focused.parentElement;
                if (nodeEl.classList.contains('folder')) {
                    const isExpanded = nodeEl.querySelector('.tree-children')?.classList.contains('expanded');
                    if (!isExpanded) {
                        const path = nodeEl.dataset.path;
                        const children = nodeEl.querySelector('.tree-children');
                        const toggle = nodeEl.querySelector('.tree-toggle');
                        if (children && toggle) {
                            children.classList.add('expanded');
                            toggle.classList.add('expanded');
                            state.expandedFolders.add(path);
                            saveExpandedState();
                        }
                    }
                    // Focus first child after expanding
                    setTimeout(() => {
                        updateTreeNodes();
                        const firstChild = nodeEl.querySelector('.tree-children .tree-node-content');
                        if (firstChild) firstChild.focus();
                    }, 50);
                    return;
                }
            }
            return;
        } else if (direction === 'ArrowLeft') {
            if (isInTree) {
                const nodeEl = focused.parentElement;
                if (nodeEl.classList.contains('folder')) {
                    const isExpanded = nodeEl.querySelector('.tree-children')?.classList.contains('expanded');
                    if (isExpanded) {
                        const path = nodeEl.dataset.path;
                        const children = nodeEl.querySelector('.tree-children');
                        const toggle = nodeEl.querySelector('.tree-toggle');
                        if (children && toggle) {
                            children.classList.remove('expanded');
                            toggle.classList.remove('expanded');
                            state.expandedFolders.delete(path);
                            saveExpandedState();
                        }
                    } else {
                        // Focus parent
                        const parentContent = nodeEl.closest('.tree-children')?.previousElementSibling;
                        if (parentContent) parentContent.focus();
                    }
                    return;
                }
            }
            return;
        }
        
        if (nextIndex !== undefined && allTreeNodes[nextIndex]) {
            allTreeNodes[nextIndex].focus();
        }
    }

    function openSelectedFile() {
        const focused = document.activeElement;
        if (focused && focused.classList.contains('tree-node-content')) {
            const nodeEl = focused.parentElement;
            const path = nodeEl.dataset.path;
            if (nodeEl.classList.contains('file')) {
                loadDocument(path);
            } else if (nodeEl.classList.contains('folder')) {
                const isExpanded = nodeEl.querySelector('.tree-children')?.classList.contains('expanded');
                const children = nodeEl.querySelector('.tree-children');
                const toggle = nodeEl.querySelector('.tree-toggle');
                if (!isExpanded && children && toggle) {
                    children.classList.add('expanded');
                    toggle.classList.add('expanded');
                    state.expandedFolders.add(path);
                    saveExpandedState();
                    // Focus first child
                    setTimeout(() => {
                        const firstChild = nodeEl.querySelector('.tree-children .tree-node-content');
                        if (firstChild) firstChild.focus();
                    }, 50);
                }
            }
        }
    }

    // ============================================
    // Event Listeners
    // ============================================
    function setupEventListeners() {
        // Sidebar toggle
        elements.toggleSidebar.addEventListener('click', toggleSidebar);
        
        // Mobile menu button
        if (elements.mobileMenuBtn) {
            elements.mobileMenuBtn.addEventListener('click', () => {
                elements.sidebar.classList.add('mobile-open');
                elements.mobileOverlay.classList.add('active');
            });
        }
        
