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
        // Filter and sort state
        filters: {
            fileTypes: ['.md'], // Default to markdown
            folder: '',
            dateRange: ''
        },
        sortBy: 'relevance', // relevance, name-asc, name-desc, date-newest, date-oldest, size
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
        searchFilterBtn: document.getElementById('searchFilterBtn'),
        searchFilterPanel: document.getElementById('searchFilterPanel'),
        fileTypeFilters: document.getElementById('fileTypeFilters'),
        folderFilter: document.getElementById('folderFilter'),
        dateFilter: document.getElementById('dateFilter'),
        clearFiltersBtn: document.getElementById('clearFiltersBtn'),
        sortOptions: document.getElementById('sortOptions'),
        activeFilters: document.getElementById('activeFilters'),
        activeFiltersList: document.getElementById('activeFiltersList'),
        fileTree: document.getElementById('fileTree'),
        document: document.getElementById('document'),
        breadcrumbs: document.getElementById('breadcrumbs'),
        themeToggle: document.getElementById('themeToggle'),
        mobileOverlay: document.getElementById('mobileOverlay'),
        recentFilesSection: document.getElementById('recentFilesSection'),
        recentFilesList: document.getElementById('recentFilesList'),
        clearRecentBtn: document.getElementById('clearRecentBtn'),
        favoritesSection: document.getElementById('favoritesSection'),
        favoritesList: document.getElementById('favoritesList'),
        favoritesEmptyState: document.getElementById('favoritesEmptyState'),
        tableOfContents: document.getElementById('tableOfContents')
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
        
        // Hide TOC initially
        elements.tableOfContents.classList.add('hidden');
        
        // Initialize active filters display
        updateActiveFilters();
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
            
            // Generate Table of Contents for markdown files
            if (ext === 'md' || ext === 'mdx') {
                generateTableOfContents();
                setupScrollSpy();
            }
            
            state.activeFile = path;
        } catch (error) {
            handleError(error, ERROR_TYPES.RENDER);
        }
    }

    // ============================================
    // Table of Contents Generation
    // ============================================
    function generateTableOfContents() {
        const headings = [];
        
        // Extract H2 and H3 headings from the rendered document
        elements.document.querySelectorAll('.markdown-body h2, .markdown-body h3').forEach((heading, index) => {
            // Ensure heading has an ID
            if (!heading.id) {
                const text = heading.textContent;
                const id = text.toLowerCase()
                    .replace(/[^\w\s-]/g, '')
                    .replace(/\s+/g, '-');
                heading.id = id || `heading-${index}`;
            }
            
            headings.push({
                level: parseInt(heading.tagName.charAt(1)),
                id: heading.id,
                text: heading.textContent
            });
        });
        
        // Render TOC or hide if no headings
        if (headings.length === 0) {
            elements.tableOfContents.classList.add('hidden');
            return;
        }
        
        let tocHtml = `
            <div class="table-of-contents-title">Contents</div>
            <ul>
        `;
        
        headings.forEach(h => {
            const indentClass = h.level === 3 ? 'toc-h3' : '';
            tocHtml += `
                <li>
                    <a href="#${h.id}" class="${indentClass}" data-target="${h.id}">${h.text}</a>
                </li>
            `;
        });
        
        tocHtml += '</ul>';
        
        elements.tableOfContents.innerHTML = tocHtml;
        elements.tableOfContents.classList.remove('hidden');
        
        // Add click handlers for smooth scroll
        elements.tableOfContents.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const targetId = link.getAttribute('href').slice(1);
                const targetElement = document.getElementById(targetId);
                if (targetElement) {
                    // Offset for fixed header/breadcrumbs
                    const offset = 100;
                    const targetPosition = targetElement.getBoundingClientRect().top + elements.document.scrollTop - offset;
                    elements.document.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });
                }
            });
        });
    }

    // ============================================
    // Scroll Spy for TOC
    // ============================================
    let scrollSpyTimeout = null;
    
    function setupScrollSpy() {
        const headings = elements.document.querySelectorAll('.markdown-body h2, .markdown-body h3');
        if (headings.length === 0) return;
        
        // Remove any existing scroll spy listeners
        elements.document.removeEventListener('scroll', handleScrollSpy);
        
        // Add scroll listener with debouncing
        elements.document.addEventListener('scroll', handleScrollSpy);
        
        // Trigger initial highlight
        handleScrollSpy();
    }

    function handleScrollSpy() {
        // Debounce scroll spy updates
        if (scrollSpyTimeout) return;
        
        scrollSpyTimeout = requestAnimationFrame(() => {
            const headings = Array.from(elements.document.querySelectorAll('.markdown-body h2, .markdown-body h3'));
            if (headings.length === 0) {
                scrollSpyTimeout = null;
                return;
            }
            
            const scrollTop = elements.document.scrollTop;
            
            // Find the currently visible heading
            let activeHeading = headings[0];
            
            headings.forEach((heading) => {
                const rect = heading.getBoundingClientRect();
                const headingTop = rect.top + elements.document.scrollTop;
                
                // Heading is considered active if it's near the top of the viewport
                if (headingTop <= scrollTop + 150) {
                    activeHeading = heading;
                }
            });
            
            // Update active state in TOC
            const tocLinks = elements.tableOfContents.querySelectorAll('a');
            tocLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === `#${activeHeading.id}`) {
                    link.classList.add('active');
                }
            });
            
            scrollSpyTimeout = null;
        });
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
                loadRecentFile();
            }
        } else {
            // No hash - show file tree and optionally load recent file
            showFileTree();
            loadRecentFile();
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
        
        // Hide TOC when no document is loaded
        elements.tableOfContents.classList.add('hidden');
        
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
    // Additional Navigation Functions
    // ============================================
    function navigateUp() {
        // Go up one level in the tree (navigate to parent folder)
        const focused = document.activeElement;
        if (focused && focused.classList.contains('tree-node-content')) {
            const nodeEl = focused.parentElement;
            const parentContent = nodeEl.closest('.tree-children')?.previousElementSibling;
            if (parentContent) {
                parentContent.focus();
            } else if (allTreeNodes.length > 0) {
                // If no parent, focus first node
                allTreeNodes[0]?.focus();
            }
        } else {
            updateTreeNodes();
            if (allTreeNodes.length > 0) {
                allTreeNodes[0].focus();
            }
        }
    }

    function navigateToRoot() {
        // Focus the first tree node (root level)
        updateTreeNodes();
        if (allTreeNodes.length > 0) {
            allTreeNodes[0].focus();
        }
    }

    function navigateToEnd() {
        // Focus the last tree node
        updateTreeNodes();
        if (allTreeNodes.length > 0) {
            allTreeNodes[allTreeNodes.length - 1].focus();
        }
    }

    // ============================================
    // Print Document
    // ============================================
    function printDocument() {
        if (state.activeFile) {
            window.print();
        }
    }

    // ============================================
    // Save Position/Bookmark
    // ============================================
    function savePosition() {
        if (state.activeFile) {
            // Save current file as bookmark in localStorage
            const bookmarks = storage.get('docs-bookmarks', []);
            const existingIndex = bookmarks.findIndex(b => b.path === state.activeFile);
            
            if (existingIndex !== -1) {
                // Update existing bookmark
                bookmarks[existingIndex].name = prompt('Update bookmark name:', bookmarks[existingIndex].name) || bookmarks[existingIndex].name;
                bookmarks[existingIndex].accessed = Date.now();
            } else {
                // Add new bookmark
                const fileName = state.activeFile.split('/').pop();
                bookmarks.unshift({
                    path: state.activeFile,
                    name: fileName,
                    accessed: Date.now()
                });
            }
            
            // Keep only last 20 bookmarks
            if (bookmarks.length > 20) {
                bookmarks.splice(20);
            }
            
            storage.set('docs-bookmarks', bookmarks);
            console.log('Position/bookmark saved:', state.activeFile);
        }
    }

    // ============================================
    // Shortcuts Modal
    // ============================================
    let shortcutsModal = null;

    function showShortcuts() {
        // Close existing modal if any
        closeModal();
        
        const shortcutsHTML = `
            <div class="shortcuts-modal-overlay" id="shortcutsModalOverlay">
                <div class="shortcuts-modal" role="dialog" aria-labelledby="shortcuts-title" aria-modal="true">
                    <div class="shortcuts-modal-header">
                        <h2 id="shortcuts-title">Keyboard Shortcuts</h2>
                        <button class="shortcuts-close" id="shortcutsCloseBtn" aria-label="Close shortcuts">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <line x1="18" y1="6" x2="6" y2="18"></line>
                                <line x1="6" y1="6" x2="18" y2="18"></line>
                            </svg>
                        </button>
                    </div>
                    <div class="shortcuts-content">
                        <div class="shortcuts-section">
                            <h3>Navigation</h3>
                            <table class="shortcuts-table">
                                <tr><td><kbd>↑</kbd> <kbd>↓</kbd></td><td>Navigate tree up/down</td></tr>
                                <tr><td><kbd>←</kbd> <kbd>→</kbd></td><td>Collapse/Expand folder</td></tr>
                                <tr><td><kbd>Enter</kbd></td><td>Open file / Select item</td></tr>
                                <tr><td><kbd>Backspace</kbd></td><td>Go up one level</td></tr>
                                <tr><td><kbd>Home</kbd></td><td>Go to first item</td></tr>
                                <tr><td><kbd>End</kbd></td><td>Go to last item</td></tr>
                            </table>
                        </div>
                        <div class="shortcuts-section">
                            <h3>Actions</h3>
                            <table class="shortcuts-table">
                                <tr><td><kbd>⌘K</kbd> / <kbd>Ctrl+K</kbd></td><td>Focus search</td></tr>
                                <tr><td><kbd>⌘/</kbd> / <kbd>Ctrl+/</kbd></td><td>Show shortcuts</td></tr>
                                <tr><td><kbd>⌘P</kbd> / <kbd>Ctrl+P</kbd></td><td>Print current document</td></tr>
                                <tr><td><kbd>⌘S</kbd> / <kbd>Ctrl+S</kbd></td><td>Save position/bookmark</td></tr>
                                <tr><td><kbd>⌘D</kbd> / <kbd>Ctrl+D</kbd></td><td>Toggle dark mode</td></tr>
                                <tr><td><kbd>Esc</kbd></td><td>Clear search / Close modal</td></tr>
                            </table>
                        </div>
                    </div>
                    <div class="shortcuts-footer">
                        <p>Press <kbd>Esc</kbd> to close this modal</p>
                    </div>
                </div>
            </div>
        `;
        
        // Create modal element
        const modalContainer = document.createElement('div');
        modalContainer.innerHTML = shortcutsHTML;
        document.body.appendChild(modalContainer.firstElementChild);
        
        shortcutsModal = document.getElementById('shortcutsModalOverlay');
        
        // Add event listeners
        document.getElementById('shortcutsCloseBtn').addEventListener('click', closeModal);
        shortcutsModal.addEventListener('click', (e) => {
            if (e.target === shortcutsModal) {
                closeModal();
            }
        });
        
        // Focus close button
        setTimeout(() => {
            document.getElementById('shortcutsCloseBtn')?.focus();
        }, 50);
        
        // Prevent body scroll
        document.body.style.overflow = 'hidden';
    }

    function closeModal() {
        if (shortcutsModal) {
            shortcutsModal.remove();
            shortcutsModal = null;
            document.body.style.overflow = '';
        }
    }

    // ============================================
    // Comprehensive Keyboard Event Listener
    // ============================================
    function setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ignore if typing in input or textarea
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
                return;
            }
            
            const key = e.key.toLowerCase();
            const mod = e.ctrlKey || e.metaKey;
            
            // Navigation keys
            if (key === 'arrowup') {
                e.preventDefault();
                navigateTree('ArrowUp');
            } else if (key === 'arrowdown') {
                e.preventDefault();
                navigateTree('ArrowDown');
            } else if (key === 'arrowleft') {
                e.preventDefault();
                navigateTree('ArrowLeft');
            } else if (key === 'arrowright') {
                e.preventDefault();
                navigateTree('ArrowRight');
            } else if (key === 'enter') {
                e.preventDefault();
                openSelectedFile();
            } else if (key === 'backspace') {
                e.preventDefault();
                navigateUp();
            } else if (key === 'home') {
                e.preventDefault();
                navigateToRoot();
            } else if (key === 'end') {
                e.preventDefault();
                navigateToEnd();
            }
            
            // Modifier keys
            if (mod) {
                if (key === 'k') {
                    e.preventDefault();
                    elements.searchInput.focus();
                } else if (key === '/') {
                    e.preventDefault();
                    showShortcuts();
                } else if (key === 'p') {
                    e.preventDefault();
                    printDocument();
                } else if (key === 's') {
                    e.preventDefault();
                    savePosition();
                } else if (key === 'd') {
                    e.preventDefault();
                    toggleTheme();
                }
            }
            
            // Escape key
            if (key === 'escape') {
                e.preventDefault();
                clearSearch();
                closeModal();
            }
        });
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
        
        // Mobile overlay click to close sidebar
        if (elements.mobileOverlay) {
            elements.mobileOverlay.addEventListener('click', () => {
                elements.sidebar.classList.remove('mobile-open');
                elements.mobileOverlay.classList.remove('active');
            });
        }
        
        // Theme toggle
        elements.themeToggle.addEventListener('click', toggleTheme);
        
        // Search input
        elements.searchInput.addEventListener('input', (e) => {
            state.searchQuery = e.target.value;
            setupSearch();
        });
        
        // Clear recent files button
        if (elements.clearRecentBtn) {
            elements.clearRecentBtn.addEventListener('click', clearRecentFiles);
        }
        
        // Handle URL hash changes
        window.addEventListener('hashchange', handleHashChange);
        
        // Handle window resize
        window.addEventListener('resize', () => {
            // Adjust layout for mobile if needed
        });
        
        // Keyboard shortcuts
        setupKeyboardShortcuts();
    }
        
        // Mobile overlay
        if (elements.mobileOverlay) {
            elements.mobileOverlay.addEventListener('click', () => {
                elements.sidebar.classList.remove('mobile-open');
                elements.mobileOverlay.classList.remove('active');
            });
        }
        
        // Theme toggle
        elements.themeToggle.addEventListener('click', toggleTheme);
        
        // Search input
        elements.searchInput.addEventListener('input', (e) => {
            state.searchQuery = e.target.value;
            setupSearch();
        });
        
        // Clear search on escape
        elements.searchInput.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                clearSearch();
                elements.searchInput.blur();
            }
        });
        
        // Focus search on cmd+k / ctrl+k
        document.addEventListener('keydown', (e) => {
            if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
                e.preventDefault();
                elements.searchInput.focus();
            }
        });
        
        // Clear recent files
        elements.clearRecentBtn.addEventListener('click', clearRecentFiles);
        
        // Handle hash changes
        window.addEventListener('hashchange', handleHashChange);
        
        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            // Don't interfere with input fields
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
                return;
            }
            
            if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
                e.preventDefault();
                navigateTree(e.key);
            } else if (e.key === 'ArrowRight') {
                e.preventDefault();
                navigateTree('ArrowRight');
            } else if (e.key === 'ArrowLeft') {
                e.preventDefault();
                navigateTree('ArrowLeft');
            } else if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                openSelectedFile();
            } else if (e.key === 'Home') {
                e.preventDefault();
                resetToRoot();
            } else if (e.key === 'Escape') {
                if (elements.sidebar.classList.contains('mobile-open')) {
                    elements.sidebar.classList.remove('mobile-open');
                    elements.mobileOverlay.classList.remove('active');
                }
            }
        });
        
        // Handle window resize
        let resizeTimer;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(() => {
                // Update layout on resize if needed
            }, 250);
        });
    }

    // ============================================
    // Initialize Application
    // ============================================
    // Start the app when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
