/**
 * Life OS Docs - Service Worker
 * Provides offline caching, installability, and app-like experience
 */

const CACHE_NAME = 'lifeos-docs-v1';
const OFFLINE_URL = 'offline.html';

// Resources to cache immediately on install
const PRECACHE_RESOURCES = [
    '/docs-viewer/',
    '/docs-viewer/index.html',
    '/docs-viewer/styles.css',
    '/docs-viewer/app.js',
    '/docs-viewer/manifest.json',
    '/docs-viewer/offline.html',
    '/docs-viewer/search-index.json'
];

// CDN resources to cache with longer TTL
const CDN_RESOURCES = [
    'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap',
    'https://cdn.jsdelivr.net/npm/prismjs@1.29.0/themes/prism-tomorrow.min.css',
    'https://cdn.jsdelivr.net/npm/marked/marked.min.js',
    'https://cdn.jsdelivr.net/npm/prismjs@1.29.0/prism.min.js',
    'https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-python.min.js',
    'https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-javascript.min.js',
    'https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-bash.min.js',
    'https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-json.min.js',
    'https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-yaml.min.js',
    'https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-markdown.min.js'
];

// File types to cache when viewed
const CACHEABLE_EXTENSIONS = ['.md', '.txt', '.json', '.py', '.js', '.html'];

// Install event - precache essential resources
self.addEventListener('install', (event) => {
    console.log('[ServiceWorker] Installing...');
    
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('[ServiceWorker] Precaching app resources');
                return cache.addAll(PRECACHE_RESOURCES.map(url => {
                    return new Request(url, { cache: 'reload' });
                })).catch(err => {
                    console.warn('[ServiceWorker] Precache failed (acceptable if offline):', err.message);
                });
            })
            .then(() => {
                console.log('[ServiceWorker] Skip waiting');
                return self.skipWaiting();
            })
    );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
    console.log('[ServiceWorker] Activating...');
    
    event.waitUntil(
        caches.keys()
            .then((cacheNames) => {
                return Promise.all(
                    cacheNames
                        .filter((cacheName) => cacheName !== CACHE_NAME)
                        .map((cacheName) => {
                            console.log('[ServiceWorker] Deleting old cache:', cacheName);
                            return caches.delete(cacheName);
                        })
                );
            })
            .then(() => {
                console.log('[ServiceWorker] Claiming clients');
                return self.clients.claim();
            })
    );
});

// Fetch event - implement caching strategy
self.addEventListener('fetch', (event) => {
    const { request } = event;
    const url = new URL(request.url);
    
    // Skip cross-origin requests except CDN resources
    if (url.origin !== location.origin && !CDN_RESOURCES.some(r => url.href.startsWith(r))) {
        return;
    }
    
    // Handle API requests (search-index.json) - network first, fallback to cache
    if (url.pathname.includes('search-index.json')) {
        event.respondWith(networkFirst(request));
        return;
    }
    
    // Handle markdown and other docs - cache first, network as fallback
    const isDocFile = CACHEABLE_EXTENSIONS.some(ext => url.pathname.endsWith(ext));
    if (isDocFile) {
        event.respondWith(cacheFirst(request));
        return;
    }
    
    // Handle CDN resources - stale while revalidate with longer cache
    if (CDN_RESOURCES.some(r => url.href.startsWith(r))) {
        event.respondWith(staleWhileRevalidate(request));
        return;
    }
    
    // Default - cache first for static assets
    event.respondWith(cacheFirst(request));
});

// Cache-first strategy: try cache, fall back to network
async function cacheFirst(request) {
    try {
        const cachedResponse = await caches.match(request);
        if (cachedResponse) {
            // Return cached version and update cache in background
            updateCache(request);
            return cachedResponse;
        }
        
        // Not in cache, try network
        const networkResponse = await fetch(request);
        
        // Cache successful responses
        if (networkResponse.ok) {
            const cache = await caches.open(CACHE_NAME);
            cache.put(request, networkResponse.clone());
        }
        
        return networkResponse;
    } catch (error) {
        console.error('[ServiceWorker] Cache-first failed:', error);
        
        // Return offline page for navigation requests
        if (request.mode === 'navigate') {
            return caches.match(OFFLINE_URL);
        }
        
        throw error;
    }
}

// Network-first strategy: try network, fall back to cache
async function networkFirst(request) {
    try {
        const networkResponse = await fetch(request);
        
        // Cache successful responses
        if (networkResponse.ok) {
            const cache = await caches.open(CACHE_NAME);
            cache.put(request, networkResponse.clone());
        }
        
        return networkResponse;
    } catch (error) {
        console.log('[ServiceWorker] Network failed, trying cache:', request.url);
        const cachedResponse = await caches.match(request);
        
        if (cachedResponse) {
            return cachedResponse;
        }
        
        // Return offline page for navigation requests
        if (request.mode === 'navigate') {
            return caches.match(OFFLINE_URL);
        }
        
        throw error;
    }
}

// Stale-while-revalidate: return cache immediately, update in background
async function staleWhileRevalidate(request) {
    const cache = await caches.open(CACHE_NAME);
    const cachedResponse = await cache.match(request);
    
    const fetchPromise = fetch(request)
        .then((networkResponse) => {
            if (networkResponse.ok) {
                cache.put(request, networkResponse.clone());
            }
            return networkResponse;
        })
        .catch(() => cachedResponse);
    
    return cachedResponse || fetchPromise;
}

// Update cache in background without blocking
async function updateCache(request) {
    try {
        const networkResponse = await fetch(request);
        if (networkResponse.ok) {
            const cache = await caches.open(CACHE_NAME);
            cache.put(request, networkResponse);
        }
    } catch (error) {
        // Silently fail - we have cached version
    }
}

// Listen for messages from the main app
self.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'CACHE_DOC') {
        // Cache a specific document
        const { url } = event.data;
        cacheUrl(url);
    } else if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    } else if (event.data && event.data.type === 'GET_CACHE_STATUS') {
        // Return cache status
        getCacheStatus().then(status => {
            event.ports[0].postMessage(status);
        });
    } else if (event.data && event.data.type === 'CLEAR_CACHE') {
        // Clear all caches
        clearAllCaches().then(() => {
            event.ports[0].postMessage({ success: true });
        });
    }
});

// Cache a specific URL
async function cacheUrl(url) {
    try {
        const response = await fetch(url);
        if (response.ok) {
            const cache = await caches.open(CACHE_NAME);
            await cache.put(url, response);
            console.log('[ServiceWorker] Cached:', url);
        }
    } catch (error) {
        console.error('[ServiceWorker] Failed to cache:', url, error);
    }
}

// Get cache status
async function getCacheStatus() {
    const cache = await caches.open(CACHE_NAME);
    const keys = await cache.keys();
    
    return {
        totalSize: keys.length,
        urls: keys.map(r => r.url)
    };
}

// Clear all caches
async function clearAllCaches() {
    const cacheNames = await caches.keys();
    await Promise.all(cacheNames.map(name => caches.delete(name)));
    console.log('[ServiceWorker] All caches cleared');
}

// Background sync for when coming back online
self.addEventListener('sync', (event) => {
    if (event.tag === 'sync-documents') {
        event.waitUntil(syncDocuments());
    }
});

// Sync pending document updates
async function syncDocuments() {
    // Get pending updates from IndexedDB and sync them
    console.log('[ServiceWorker] Syncing documents...');
}

// Push notifications (for future use)
self.addEventListener('push', (event) => {
    if (event.data) {
        const data = event.data.json();
        
        event.waitUntil(
            self.registration.showNotification(data.title, {
                body: data.body,
                icon: '/docs-viewer/icon-192.png',
                badge: '/docs-viewer/icon-192.png',
                data: data.url
            })
        );
    }
});

self.addEventListener('notificationclick', (event) => {
    event.notification.close();
    
    if (event.notification.data) {
        event.waitUntil(
            clients.openWindow(event.notification.data)
        );
    }
});

console.log('[ServiceWorker] Service Worker loaded');
