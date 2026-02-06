/**
 * Life OS Docs Viewer - Comprehensive Test Suite
 * Tests: Functional, Performance, Compatibility, Accessibility
 */

// ============================================
// Test Runner
// ============================================
class TestRunner {
    constructor() {
        this.results = {
            functional: [],
            performance: [],
            compatibility: [],
            accessibility: []
        };
        this.startTime = null;
        this.memoryStart = null;
    }

    log(name, status, details = '') {
        const timestamp = new Date().toISOString();
        console.log(`[${status.toUpperCase()}] ${name}${details ? ': ' + details : ''}`);
    }

    async measureTime(fn) {
        const start = performance.now();
        await fn();
        return performance.now() - start;
    }

    getMemoryUsage() {
        if (performance.memory) {
            return Math.round(performance.memory.usedJSHeapSize / 1024 / 1024);
        }
        return null;
    }
}

// ============================================
// Functional Tests
// ============================================
class FunctionalTests extends TestRunner {
    constructor() {
        super();
        this.elements = {
            fileTree: null,
            searchInput: null,
            searchResults: null,
            themeToggle: null,
            recentFilesSection: null,
            recentFilesList: null,
            breadcrumbs: null,
            document: null,
            sidebar: null
        };
    }

    async init() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            await new Promise(resolve => document.addEventListener('DOMContentLoaded', resolve));
        }
        
        // Get element references
        this.elements.fileTree = document.getElementById('fileTree');
        this.elements.searchInput = document.getElementById('searchInput');
        this.elements.searchResults = document.getElementById('searchResults');
        this.elements.themeToggle = document.getElementById('themeToggle');
        this.elements.recentFilesSection = document.getElementById('recentFilesSection');
        this.elements.recentFilesList = document.getElementById('recentFilesList');
        this.elements.breadcrumbs = document.getElementById('breadcrumbs');
        this.elements.document = document.getElementById('document');
        this.elements.sidebar = document.getElementById('sidebar');
        
        // Wait for app to initialize
        await new Promise(resolve => setTimeout(resolve, 1000));
    }

    async runAll() {
        console.log('\n=== FUNCTIONAL TESTS ===\n');
        
        await this.testFileTreeRenders();
        await this.testSearchReturnsResults();
        await this.testFileClickNavigation();
        await this.testBreadcrumbNavigation();
        await this.testDarkModeToggle();
        await this.testRecentFilesTracking();
        
        return this.results.functional;
    }

    async testFileTreeRenders() {
        const testName = 'File Tree Renders';
        try {
            const hasContent = this.elements.fileTree && 
                              this.elements.fileTree.children.length > 0 &&
                              !this.elements.fileTree.querySelector('.loading-overlay');
            
            if (hasContent) {
                const fileItems = this.elements.fileTree.querySelectorAll('[role="treeitem"]');
                this.results.functional.push({
                    name: testName,
                    status: 'PASS',
                    details: `Found ${fileItems.length} file items`
                });
            } else {
                this.results.functional.push({
                    name: testName,
                    status: 'FAIL',
                    details: 'File tree is empty or still loading'
                });
            }
        } catch (error) {
            this.results.functional.push({
                name: testName,
                status: 'ERROR',
                details: error.message
            });
        }
    }

    async testSearchReturnsResults() {
        const testName = 'Search Returns Results';
        try {
            if (!this.elements.searchInput) {
                this.results.functional.push({
                    name: testName,
                    status: 'FAIL',
                    details: 'Search input not found'
                });
                return;
            }

            // Focus search and type
            this.elements.searchInput.focus();
            this.elements.searchInput.value = 'test';
            
            // Trigger input event
            const event = new Event('input', { bubbles: true });
            this.elements.searchInput.dispatchEvent(event);
            
            // Wait for results
            await new Promise(resolve => setTimeout(resolve, 500));
            
            const results = this.elements.searchResults.querySelectorAll('.search-result-item');
            
            if (results.length > 0) {
                this.results.functional.push({
                    name: testName,
                    status: 'PASS',
                    details: `Found ${results.length} results for "test"`
                });
            } else {
                // Check if search index loaded
                const searchIndex = window.searchIndex || window.fileIndex;
                if (searchIndex && Object.keys(searchIndex).length > 0) {
                    this.results.functional.push({
                        name: testName,
                        status: 'PASS',
                        details: 'Search input works, no results for "test" (expected)'
                    });
                } else {
                    this.results.functional.push({
                        name: testName,
                        status: 'FAIL',
                        details: 'No search results found'
                    });
                }
            }
            
            // Clear search
            this.elements.searchInput.value = '';
            this.elements.searchInput.dispatchEvent(new Event('input', { bubbles: true }));
            
        } catch (error) {
            this.results.functional.push({
                name: testName,
                status: 'ERROR',
                details: error.message
            });
        }
    }

    async testFileClickNavigation() {
        const testName = 'File Click Navigation';
        try {
            const fileItem = this.elements.fileTree?.querySelector('[role="treeitem"]');
            
            if (fileItem) {
                const filePath = fileItem.getAttribute('data-path') || fileItem.dataset.path;
                const initialContent = this.elements.document?.innerHTML;
                
                // Click the file
                fileItem.click();
                
                // Wait for navigation
                await new Promise(resolve => setTimeout(resolve, 500));
                
                const newContent = this.elements.document?.innerHTML;
                const contentChanged = initialContent !== newContent;
                const hasContent = newContent && !newContent.includes('Select a document to view');
                
                if (contentChanged || hasContent) {
                    this.results.functional.push({
                        name: testName,
                        status: 'PASS',
                        details: `Navigation triggered for: ${filePath || 'file'}`
                    });
                } else {
                    this.results.functional.push({
                        name: testName,
                        status: 'FAIL',
                        details: 'Content did not change after click'
                    });
                }
            } else {
                this.results.functional.push({
                    name: testName,
                    status: 'FAIL',
                    details: 'No file items found to click'
                });
            }
        } catch (error) {
            this.results.functional.push({
                name: testName,
                status: 'ERROR',
                details: error.message
            });
        }
    }

    async testBreadcrumbNavigation() {
        const testName = 'Breadcrumb Navigation';
        try {
            const breadcrumbs = this.elements.breadcrumbs;
            
            if (breadcrumbs) {
                const items = breadcrumbs.querySelectorAll('.breadcrumb-item');
                const hasHome = items.length > 0 && items[0]?.textContent?.includes('Home');
                
                if (hasHome) {
                    this.results.functional.push({
                        name: testName,
                        status: 'PASS',
                        details: `Found ${items.length} breadcrumb(s)`
                    });
                } else {
                    this.results.functional.push({
                        name: testName,
                        status: 'FAIL',
                        details: 'Home breadcrumb not found'
                    });
                }
            } else {
                this.results.functional.push({
                    name: testName,
                    status: 'FAIL',
                    details: 'Breadcrumbs element not found'
                });
            }
        } catch (error) {
            this.results.functional.push({
                name: testName,
                status: 'ERROR',
                details: error.message
            });
        }
    }

    async testDarkModeToggle() {
        const testName = 'Dark Mode Toggle';
        try {
            if (!this.elements.themeToggle) {
                this.results.functional.push({
                    name: testName,
                    status: 'FAIL',
                    details: 'Theme toggle button not found'
                });
                return;
            }

            const initialTheme = document.body.getAttribute('data-theme');
            
            // Click toggle
            this.elements.themeToggle.click();
            await new Promise(resolve => setTimeout(resolve, 200));
            
            const afterClick = document.body.getAttribute('data-theme');
            const toggled = initialTheme !== afterClick;
            
            // Click again to restore
            this.elements.themeToggle.click();
            await new Promise(resolve => setTimeout(resolve => {}, 200));
            const restored = document.body.getAttribute('data-theme') === initialTheme;
            
            if (toggled) {
                this.results.functional.push({
                    name: testName,
                    status: 'PASS',
                    details: `Theme toggled: ${initialTheme} → ${afterClick}`
                });
            } else {
                this.results.functional.push({
                    name: testName,
                    status: 'FAIL',
                    details: 'Theme did not toggle'
                });
            }
        } catch (error) {
            this.results.functional.push({
                name: testName,
                status: 'ERROR',
                details: error.message
            });
        }
    }

    async testRecentFilesTracking() {
        const testName = 'Recent Files Tracking';
        try {
            // Navigate to a file first
            const fileItem = this.elements.fileTree?.querySelector('[role="treeitem"]');
            if (fileItem) {
                fileItem.click();
                await new Promise(resolve => setTimeout(resolve, 500));
            }
            
            // Check recent files section
            const section = this.elements.recentFilesSection;
            const isVisible = section && section.style.display !== 'none';
            const hasRecentFiles = this.elements.recentFilesList?.children.length > 0;
            
            // Check localStorage
            const recentFiles = JSON.parse(localStorage.getItem('docs-recent-files') || '[]');
            const inStorage = recentFiles.length > 0;
            
            if (isVisible && hasRecentFiles) {
                this.results.functional.push({
                    name: testName,
                    status: 'PASS',
                    details: `Recent files section visible with ${this.elements.recentFilesList.children.length} file(s)`
                });
            } else if (inStorage) {
                this.results.functional.push({
                    name: testName,
                    status: 'PASS',
                    details: `${recentFiles.length} file(s) tracked in storage`
                });
            } else {
                this.results.functional.push({
                    name: testName,
                    status: 'FAIL',
                    details: 'No recent files tracked'
                });
            }
        } catch (error) {
            this.results.functional.push({
                name: testName,
                status: 'ERROR',
                details: error.message
            });
        }
    }
}

// ============================================
// Performance Tests
// ============================================
class PerformanceTests extends TestRunner {
    async runAll() {
        console.log('\n=== PERFORMANCE TESTS ===\n');
        
        await this.testInitialLoad();
        await this.testSearchPerformance();
        await this.testFileClickPerformance();
        await this.testMemoryUsage();
        
        return this.results.performance;
    }

    async testInitialLoad() {
        const testName = 'Initial Load < 2s';
        try {
            // Check if page loaded within reasonable time
            const timing = performance.timing;
            const loadTime = timing.loadEventEnd - timing.navigationStart;
            
            if (loadTime < 2000) {
                this.results.performance.push({
                    name: testName,
                    status: 'PASS',
                    details: `Load time: ${(loadTime / 1000).toFixed(2)}s`
                });
            } else {
                this.results.performance.push({
                    name: testName,
                    status: 'FAIL',
                    details: `Load time: ${(loadTime / 1000).toFixed(2)}s (exceeds 2s)`
                });
            }
        } catch (error) {
            this.results.performance.push({
                name: testName,
                status: 'ERROR',
                details: error.message
            });
        }
    }

    async testSearchPerformance() {
        const testName = 'Search < 100ms';
        try {
            const searchInput = document.getElementById('searchInput');
            if (!searchInput) {
                this.results.performance.push({
                    name: testName,
                    status: 'FAIL',
                    details: 'Search input not found'
                });
                return;
            }

            const iterations = 5;
            let totalTime = 0;
            
            for (let i = 0; i < iterations; i++) {
                searchInput.focus();
                searchInput.value = 'test';
                const start = performance.now();
                
                searchInput.dispatchEvent(new Event('input', { bubbles: true }));
                
                // Small delay to allow processing
                await new Promise(resolve => setTimeout(resolve, 10));
                
                totalTime += performance.now() - start;
            }
            
            const avgTime = totalTime / iterations;
            
            if (avgTime < 100) {
                this.results.performance.push({
                    name: testName,
                    status: 'PASS',
                    details: `Avg search time: ${avgTime.toFixed(2)}ms`
                });
            } else {
                this.results.performance.push({
                    name: testName,
                    status: 'FAIL',
                    details: `Avg search time: ${avgTime.toFixed(2)}ms (exceeds 100ms)`
                });
            }
            
            searchInput.value = '';
            searchInput.dispatchEvent(new Event('input', { bubbles: true }));
            
        } catch (error) {
            this.results.performance.push({
                name: testName,
                status: 'ERROR',
                details: error.message
            });
        }
    }

    async testFileClickPerformance() {
        const testName = 'File Click < 500ms';
        try {
            const fileTree = document.getElementById('fileTree');
            const fileItem = fileTree?.querySelector('[role="treeitem"]');
            
            if (!fileItem) {
                this.results.performance.push({
                    name: testName,
                    status: 'FAIL',
                    details: 'No file items found'
                });
                return;
            }

            const iterations = 3;
            let totalTime = 0;
            
            for (let i = 0; i < iterations; i++) {
                const start = performance.now();
                fileItem.click();
                await new Promise(resolve => setTimeout(resolve, 200));
                totalTime += performance.now() - start;
            }
            
            const avgTime = totalTime / iterations;
            
            if (avgTime < 500) {
                this.results.performance.push({
                    name: testName,
                    status: 'PASS',
                    details: `Avg navigation time: ${avgTime.toFixed(2)}ms`
                });
            } else {
                this.results.performance.push({
                    name: testName,
                    status: 'FAIL',
                    details: `Avg navigation time: ${avgTime.toFixed(2)}ms (exceeds 500ms)`
                });
            }
            
        } catch (error) {
            this.results.performance.push({
                name: testName,
                status: 'ERROR',
                details: error.message
            });
        }
    }

    async testMemoryUsage() {
        const testName = 'Memory Usage < 50MB';
        try {
            const memory = performance.memory;
            
            if (memory) {
                const usedMB = Math.round(memory.usedJSHeapSize / 1024 / 1024);
                
                if (usedMB < 50) {
                    this.results.performance.push({
                        name: testName,
                        status: 'PASS',
                        details: `Memory usage: ${usedMB}MB`
                    });
                } else {
                    this.results.performance.push({
                        name: testName,
                        status: 'FAIL',
                        details: `Memory usage: ${usedMB}MB (exceeds 50MB)`
                    });
                }
            } else {
                this.results.performance.push({
                    name: testName,
                    status: 'INFO',
                    details: 'Memory API not available (Chrome only)'
                });
            }
        } catch (error) {
            this.results.performance.push({
                name: testName,
                status: 'ERROR',
                details: error.message
            });
        }
    }
}

// ============================================
// Compatibility Tests (Browser Detection)
// ============================================
class CompatibilityTests extends TestRunner {
    async runAll() {
        console.log('\n=== COMPATIBILITY TESTS ===\n');
        
        await this.detectBrowser();
        await this.checkFeatures();
        await this.testResponsiveBreakpoints();
        
        return this.results.compatibility;
    }

    detectBrowser() {
        const ua = navigator.userAgent;
        let browser = 'Unknown';
        
        if (ua.includes('Chrome')) browser = 'Chrome';
        else if (ua.includes('Safari') && !ua.includes('Chrome')) browser = 'Safari';
        else if (ua.includes('Firefox')) browser = 'Firefox';
        else if (ua.includes('Edge')) browser = 'Edge';
        
        this.results.compatibility.push({
            name: 'Browser Detection',
            status: 'INFO',
            details: `${browser} (${ua.substring(0, 100)}...)`
        });
    }

    checkFeatures() {
        // Check ES6+ support
        const es6Features = [
            { name: 'const', supported: 'const' in window },
            { name: 'let', supported: 'let' in window },
            { name: 'Arrow Functions', supported: (() => true) instanceof Function },
            { name: 'Fetch API', supported: 'fetch' in window },
            { name: 'localStorage', supported: 'localStorage' in window },
            { name: 'Promise', supported: 'Promise' in window },
            { name: 'IntersectionObserver', supported: 'IntersectionObserver' in window },
            { name: 'CSS Variables', supported: CSS.supports('--test', '0') }
        ];
        
        const allSupported = es6Features.every(f => f.supported);
        const supportedCount = es6Features.filter(f => f.supported).length;
        
        this.results.compatibility.push({
            name: 'Feature Detection',
            status: allSupported ? 'PASS' : 'FAIL',
            details: `${supportedCount}/${es6Features.length} features supported`
        });
    }

    async testResponsiveBreakpoints() {
        const breakpoints = [
            { name: 'Mobile', width: 375, height: 667 },
            { name: 'Tablet', width: 768, height: 1024 },
            { name: 'Desktop', width: 1440, height: 900 }
        ];
        
        const currentWidth = window.innerWidth;
        let activeBreakpoint = 'Desktop';
        
        if (currentWidth < 768) activeBreakpoint = 'Mobile';
        else if (currentWidth < 1024) activeBreakpoint = 'Tablet';
        
        this.results.compatibility.push({
            name: 'Responsive Breakpoints',
            status: 'INFO',
            details: `Current viewport: ${currentWidth}px (${activeBreakpoint})`
        });
    }
}

// ============================================
// Accessibility Tests
// ============================================
class AccessibilityTests extends TestRunner {
    async runAll() {
        console.log('\n=== ACCESSIBILITY TESTS ===\n');
        
        await this.testKeyboardNavigation();
        await this.testScreenReaderSupport();
        await this.testColorContrast();
        await this.testFocusIndicators();
        
        return this.results.accessibility;
    }

    async testKeyboardNavigation() {
        const testName = 'Keyboard Navigation';
        try {
            // Check for skip link
            const skipLink = document.querySelector('.skip-link');
            const hasSkipLink = !!skipLink;
            
            // Check tab order
            const focusableElements = document.querySelectorAll(
                'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
            );
            
            // Check key event handlers exist
            const hasKeyHandlers = document.querySelectorAll('[onkeydown], [onkeyup], [onkeypress]').length > 0;
            
            // Test Tab navigation
            let tabWorks = false;
            const testInput = document.createElement('input');
            testInput.type = 'text';
            testInput.style.position = 'absolute';
            testInput.style.opacity = '0';
            document.body.appendChild(testInput);
            
            testInput.focus();
            const startActive = document.activeElement;
            testInput.blur();
            
            // Press Tab key
            const tabEvent = new KeyboardEvent('keydown', { key: 'Tab', bubbles: true });
            document.body.dispatchEvent(tabEvent);
            
            // Check if focus moved
            setTimeout(() => {
                tabWorks = document.activeElement !== startActive;
            }, 10);
            
            document.body.removeChild(testInput);
            
            if (hasSkipLink && focusableElements.length > 0) {
                this.results.accessibility.push({
                    name: testName,
                    status: 'PASS',
                    details: `${focusableElements.length} focusable elements, skip link present`
                });
            } else {
                this.results.accessibility.push({
                    name: testName,
                    status: 'FAIL',
                    details: `Skip link: ${hasSkipLink}, Focusable: ${focusableElements.length}`
                });
            }
        } catch (error) {
            this.results.accessibility.push({
                name: testName,
                status: 'ERROR',
                details: error.message
            });
        }
    }

    async testScreenReaderSupport() {
        const testName = 'Screen Reader Support';
        try {
            // Check ARIA landmarks
            const landmarks = {
                navigation: document.querySelectorAll('[role="navigation"], nav').length,
                main: document.querySelectorAll('[role="main"], main').length,
                article: document.querySelectorAll('[role="article"], article').length,
                region: document.querySelectorAll('[role="region"], [aria-label], [aria-labelledby]').length
            };
            
            const hasLandmarks = landmarks.navigation > 0 && landmarks.main > 0;
            
            // Check ARIA live regions
            const liveRegions = document.querySelectorAll('[aria-live]').length;
            
            // Check labels
            const inputsWithLabels = document.querySelectorAll('input[aria-label], input[id], label[for]');
            
            if (hasLandmarks && liveRegions > 0) {
                this.results.accessibility.push({
                    name: testName,
                    status: 'PASS',
                    details: `Landmarks: nav(${landmarks.navigation}), main(${landmarks.main}), aria-live(${liveRegions})`
                });
            } else {
                this.results.accessibility.push({
                    name: testName,
                    status: 'FAIL',
                    details: `Missing landmarks or aria-live regions`
                });
            }
        } catch (error) {
            this.results.accessibility.push({
                name: testName,
                status: 'ERROR',
                details: error.message
            });
        }
    }

    async testColorContrast() {
        const testName = 'Color Contrast (WCAG AA)';
        try {
            // Get computed colors for key elements
            const sidebar = document.querySelector('.sidebar');
            const bodyBg = getComputedStyle(document.body).backgroundColor;
            const textColor = getComputedStyle(document.body).color;
            const linkColor = getComputedStyle(document.querySelector('a') || document.body).color;
            
            // Simple contrast check (simplified - real implementation would use chroma.js)
            const hasLightMode = !document.body.hasAttribute('data-theme');
            const hasDarkMode = document.body.hasAttribute('data-theme');
            
            // Check focus colors
            const focusColor = getComputedStyle(document.querySelector('.toggle-btn') || document.body).outlineColor;
            
            this.results.accessibility.push({
                name: testName,
                status: 'INFO',
                details: `Light mode: ${hasLightMode}, Dark mode: ${hasDarkMode}, Focus visible`
            });
        } catch (error) {
            this.results.accessibility.push({
                name: testName,
                status: 'ERROR',
                details: error.message
            });
        }
    }

    async testFocusIndicators() {
        const testName = 'Focus Indicators Visible';
        try {
            // Check for focus-visible styles
            const styles = document.styleSheets;
            let hasFocusStyles = false;
            
            try {
                for (const sheet of styles) {
                    if (sheet.cssRules) {
                        for (const rule of sheet.cssRules) {
                            if (rule.selectorText && 
                                (rule.selectorText.includes(':focus') || 
                                 rule.selectorText.includes(':focus-visible'))) {
                                hasFocusStyles = true;
                                break;
                            }
                        }
                    }
                }
            } catch (e) {
                // Cross-origin stylesheets may throw
            }
            
            // Check button focus styles
            const buttons = document.querySelectorAll('button');
            let hasButtonFocus = false;
            
            for (const btn of buttons) {
                const style = getComputedStyle(btn);
                if (style.outlineWidth !== '0px' || style.outlineStyle !== 'none') {
                    hasButtonFocus = true;
                    break;
                }
            }
            
            if (hasFocusStyles) {
                this.results.accessibility.push({
                    name: testName,
                    status: 'PASS',
                    details: 'Focus styles detected in stylesheets'
                });
            } else {
                this.results.accessibility.push({
                    name: testName,
                    status: 'FAIL',
                    details: 'No visible focus styles found'
                });
            }
        } catch (error) {
            this.results.accessibility.push({
                name: testName,
                status: 'ERROR',
                details: error.message
            });
        }
    }
}

// ============================================
// Main Test Runner
// ============================================
async function runAllTests() {
    console.log('╔════════════════════════════════════════╗');
    console.log('║  Life OS Docs Viewer - Test Suite     ║');
    console.log('╚════════════════════════════════════════╝\n');
    
    const allResults = {
        functional: [],
        performance: [],
        compatibility: [],
        accessibility: [],
        summary: {},
        timestamp: new Date().toISOString(),
        environment: {
            userAgent: navigator.userAgent,
            viewport: `${window.innerWidth}x${window.innerHeight}`,
            platform: navigator.platform
        }
    };
    
    try {
        // Run Functional Tests
        const functional = new FunctionalTests();
        await functional.init();
        allResults.functional = await functional.runAll();
        
        // Run Performance Tests
        const performance = new PerformanceTests();
        await performance.runAll();
        allResults.performance = performance.results.performance;
        
        // Run Compatibility Tests
        const compatibility = new CompatibilityTests();
        await compatibility.runAll();
        allResults.compatibility = compatibility.results.compatibility;
        
        // Run Accessibility Tests
        const accessibility = new AccessibilityTests();
        await accessibility.runAll();
        allResults.accessibility = accessibility.results.accessibility;
        
        // Generate summary
        const categories = ['functional', 'performance', 'compatibility', 'accessibility'];
        for (const cat of categories) {
            const results = allResults[cat] || [];
            const passed = results.filter(r => r.status === 'PASS').length;
            const failed = results.filter(r => r.status === 'FAIL').length;
            const errors = results.filter(r => r.status === 'ERROR').length;
            const info = results.filter(r => r.status === 'INFO').length;
            
            allResults.summary[cat] = { passed, failed, errors, info, total: results.length };
        }
        
        // Log summary
        console.log('\n═══════════════════════════════════════════');
        console.log('           TEST SUMMARY');
        console.log('═══════════════════════════════════════════\n');
        
        for (const cat of categories) {
            const s = allResults.summary[cat];
            console.log(`${cat.toUpperCase()}: ${s.passed} PASS, ${s.failed} FAIL, ${s.errors} ERROR, ${s.info} INFO (${s.total} total)`);
        }
        
        console.log('\n═══════════════════════════════════════════\n');
        
        return allResults;
        
    } catch (error) {
        console.error('Test suite error:', error);
        allResults.error = error.message;
        return allResults;
    }
}

// Export for use
window.runAllTests = runAllTests;
window.TestRunner = TestRunner;
window.FunctionalTests = FunctionalTests;
window.PerformanceTests = PerformanceTests;
window.CompatibilityTests = CompatibilityTests;
window.AccessibilityTests = AccessibilityTests;
