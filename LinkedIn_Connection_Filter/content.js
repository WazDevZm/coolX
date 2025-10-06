// LinkedIn Connection Filter Content Script
class LinkedInConnectionFilter {
    constructor() {
        this.isEnabled = false;
        this.filterSettings = {
            showVerifiedOnly: false,
            showUnverifiedOnly: false,
            customMessage: ""
        };
        this.init();
    }

    init() {
        // Load settings from storage
        chrome.storage.sync.get(['filterSettings', 'isEnabled'], (result) => {
            this.filterSettings = result.filterSettings || this.filterSettings;
            this.isEnabled = result.isEnabled || false;
            
            if (this.isEnabled) {
                this.startFiltering();
            }
        });

        // Listen for messages from popup
        chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
            if (request.action === 'toggleFilter') {
                this.isEnabled = request.enabled;
                if (this.isEnabled) {
                    this.startFiltering();
                } else {
                    this.stopFiltering();
                }
            } else if (request.action === 'updateSettings') {
                this.filterSettings = request.settings;
                this.applyFilters();
            } else if (request.action === 'sendInvite') {
                this.sendConnectionInvite(request.profileUrl, request.message);
            }
        });

        // Monitor for new connection requests
        this.observeConnectionRequests();
    }

    startFiltering() {
        this.createFilterUI();
        this.applyFilters();
        this.observeConnectionRequests();
    }

    stopFiltering() {
        this.removeFilterUI();
        this.showAllConnections();
    }

    createFilterUI() {
        // Remove existing UI if any
        this.removeFilterUI();

        // Create filter control panel
        const filterPanel = document.createElement('div');
        filterPanel.id = 'linkedin-filter-panel';
        filterPanel.innerHTML = `
            <div class="filter-controls">
                <h3>🔗 Connection Filter</h3>
                <div class="filter-options">
                    <label>
                        <input type="radio" name="filterType" value="verified" ${this.filterSettings.showVerifiedOnly ? 'checked' : ''}>
                        Show Verified Only
                    </label>
                    <label>
                        <input type="radio" name="filterType" value="unverified" ${this.filterSettings.showUnverifiedOnly ? 'checked' : ''}>
                        Show Unverified Only
                    </label>
                    <label>
                        <input type="radio" name="filterType" value="all" ${!this.filterSettings.showVerifiedOnly && !this.filterSettings.showUnverifiedOnly ? 'checked' : ''}>
                        Show All
                    </label>
                </div>
                <div class="filter-actions">
                    <button id="apply-filter">Apply Filter</button>
                    <button id="clear-filter">Clear Filter</button>
                </div>
            </div>
        `;

        // Insert at the top of the page
        const targetElement = document.querySelector('.scaffold-layout__content') || document.body;
        targetElement.insertBefore(filterPanel, targetElement.firstChild);

        // Add event listeners
        this.addFilterEventListeners();
    }

    addFilterEventListeners() {
        const applyBtn = document.getElementById('apply-filter');
        const clearBtn = document.getElementById('clear-filter');
        const filterRadios = document.querySelectorAll('input[name="filterType"]');

        if (applyBtn) {
            applyBtn.addEventListener('click', () => {
                const selectedFilter = document.querySelector('input[name="filterType"]:checked').value;
                this.updateFilterSettings(selectedFilter);
                this.applyFilters();
            });
        }

        if (clearBtn) {
            clearBtn.addEventListener('click', () => {
                this.showAllConnections();
            });
        }

        filterRadios.forEach(radio => {
            radio.addEventListener('change', () => {
                this.updateFilterSettings(radio.value);
            });
        });
    }

    updateFilterSettings(filterType) {
        this.filterSettings.showVerifiedOnly = filterType === 'verified';
        this.filterSettings.showUnverifiedOnly = filterType === 'unverified';
        
        // Save to storage
        chrome.storage.sync.set({ filterSettings: this.filterSettings });
    }

    applyFilters() {
        console.log('LinkedIn Filter: Applying filters...');
        const connectionElements = this.getConnectionElements();
        console.log(`LinkedIn Filter: Found ${connectionElements.length} connection elements`);
        
        let verifiedCount = 0;
        let unverifiedCount = 0;
        
        connectionElements.forEach((element, index) => {
            const isVerified = this.isUserVerified(element);
            const shouldShow = this.shouldShowConnection(isVerified);
            
            console.log(`LinkedIn Filter: Element ${index} - Verified: ${isVerified}, Should Show: ${shouldShow}`);
            
            if (shouldShow) {
                element.style.display = '';
                element.style.opacity = '1';
                element.classList.remove('filtered-out');
                element.classList.add('linkedin-filter-visible');
                if (isVerified) verifiedCount++;
                else unverifiedCount++;
            } else {
                element.style.display = 'none';
                element.style.opacity = '0.3';
                element.classList.add('filtered-out');
                element.classList.remove('linkedin-filter-visible');
            }
        });
        
        console.log(`LinkedIn Filter: Showing ${verifiedCount} verified, ${unverifiedCount} unverified connections`);
        this.updateStatistics(verifiedCount, unverifiedCount);
    }

    getConnectionElements() {
        // LinkedIn connection request selectors (may need updates based on current LinkedIn UI)
        const selectors = [
            '.invitation-card',
            '.connection-request',
            '[data-test-id="invitation-card"]',
            '.artdeco-entity-lockup',
            '.invitation-card__content'
        ];

        let elements = [];
        selectors.forEach(selector => {
            elements = elements.concat(Array.from(document.querySelectorAll(selector)));
        });

        return elements;
    }

    isUserVerified(element) {
        // Look for verification indicators
        const verificationIndicators = [
            '.verified-badge',
            '.premium-badge',
            '[data-test-id="verified-badge"]',
            '.premium-indicator',
            '.verified-icon'
        ];

        for (const indicator of verificationIndicators) {
            if (element.querySelector(indicator)) {
                return true;
            }
        }

        // Check for verification text
        const text = element.textContent.toLowerCase();
        const verificationKeywords = ['verified', 'premium', 'pro'];
        
        return verificationKeywords.some(keyword => text.includes(keyword));
    }

    shouldShowConnection(isVerified) {
        if (this.filterSettings.showVerifiedOnly) {
            return isVerified;
        } else if (this.filterSettings.showUnverifiedOnly) {
            return !isVerified;
        }
        return true;
    }

    showAllConnections() {
        const connectionElements = this.getConnectionElements();
        connectionElements.forEach(element => {
            element.style.display = '';
            element.classList.remove('filtered-out');
        });
    }

    observeConnectionRequests() {
        // Use MutationObserver to detect new connection requests
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.addedNodes.length > 0) {
                    // Check if new connection requests were added
                    const hasNewConnections = Array.from(mutation.addedNodes).some(node => {
                        if (node.nodeType === Node.ELEMENT_NODE) {
                            return this.getConnectionElements().some(el => el.contains(node));
                        }
                        return false;
                    });

                    if (hasNewConnections && this.isEnabled) {
                        setTimeout(() => this.applyFilters(), 100);
                    }
                }
            });
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }

    sendConnectionInvite(profileUrl, message) {
        // Navigate to the profile and send connection request
        if (profileUrl) {
            window.open(profileUrl, '_blank');
            
            // Wait for page to load and then send invite
            setTimeout(() => {
                this.triggerConnectionRequest(message);
            }, 2000);
        }
    }

    triggerConnectionRequest(message) {
        // Look for connect button and click it
        const connectButton = document.querySelector('[data-test-id="connect-button"], .artdeco-button--primary, [aria-label*="Connect"]');
        
        if (connectButton) {
            connectButton.click();
            
            // Wait for modal to appear and add message
            setTimeout(() => {
                this.addMessageToInvite(message);
            }, 1000);
        }
    }

    addMessageToInvite(message) {
        // Look for message textarea in connection modal
        const messageTextarea = document.querySelector('textarea[placeholder*="message"], textarea[aria-label*="message"], .send-invite__custom-message textarea');
        
        if (messageTextarea && message) {
            messageTextarea.value = message;
            messageTextarea.dispatchEvent(new Event('input', { bubbles: true }));
        }

        // Look for send button and click it
        const sendButton = document.querySelector('[data-test-id="send-invite"], .artdeco-button--primary, button[aria-label*="Send"]');
        if (sendButton) {
            sendButton.click();
        }
    }

    removeFilterUI() {
        const existingPanel = document.getElementById('linkedin-filter-panel');
        if (existingPanel) {
            existingPanel.remove();
        }
    }
}

// Initialize the filter when the page loads
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new LinkedInConnectionFilter();
    });
} else {
    new LinkedInConnectionFilter();
}
