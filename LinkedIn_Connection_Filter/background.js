// LinkedIn Connection Filter Background Script
class LinkedInFilterBackground {
    constructor() {
        this.init();
    }

    init() {
        // Listen for extension installation
        chrome.runtime.onInstalled.addListener((details) => {
            if (details.reason === 'install') {
                this.handleInstall();
            } else if (details.reason === 'update') {
                this.handleUpdate(details.previousVersion);
            }
        });

        // Listen for messages from content scripts and popup
        chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
            this.handleMessage(request, sender, sendResponse);
            return true; // Keep message channel open for async responses
        });

        // Listen for tab updates
        chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
            if (changeInfo.status === 'complete' && tab.url && tab.url.includes('linkedin.com')) {
                this.handleLinkedInPageLoad(tabId, tab);
            }
        });
    }

    handleInstall() {
        console.log('LinkedIn Connection Filter installed');
        
        // Set default settings
        chrome.storage.sync.set({
            filterSettings: {
                showVerifiedOnly: false,
                showUnverifiedOnly: false,
                customMessage: ""
            },
            isEnabled: false,
            statistics: {
                totalConnections: 0,
                verifiedConnections: 0,
                unverifiedConnections: 0
            }
        });

        // Open welcome page
        chrome.tabs.create({
            url: chrome.runtime.getURL('welcome.html')
        });
    }

    handleUpdate(previousVersion) {
        console.log(`LinkedIn Connection Filter updated from ${previousVersion}`);
        
        // Handle any migration logic here
        this.migrateSettings(previousVersion);
    }

    async migrateSettings(previousVersion) {
        // Add any settings migration logic here
        // For now, just log the update
        console.log('Settings migration completed');
    }

    handleMessage(request, sender, sendResponse) {
        switch (request.action) {
            case 'getStatistics':
                this.getStatistics(sendResponse);
                break;
            case 'updateStatistics':
                this.updateStatistics(request.data);
                break;
            case 'logActivity':
                this.logActivity(request.data);
                break;
            case 'getSettings':
                this.getSettings(sendResponse);
                break;
            case 'saveSettings':
                this.saveSettings(request.data, sendResponse);
                break;
            default:
                console.log('Unknown message action:', request.action);
        }
    }

    async getStatistics(sendResponse) {
        try {
            const result = await chrome.storage.sync.get(['statistics']);
            sendResponse(result.statistics || {
                totalConnections: 0,
                verifiedConnections: 0,
                unverifiedConnections: 0
            });
        } catch (error) {
            console.error('Error getting statistics:', error);
            sendResponse({
                totalConnections: 0,
                verifiedConnections: 0,
                unverifiedConnections: 0
            });
        }
    }

    async updateStatistics(data) {
        try {
            await chrome.storage.sync.set({ statistics: data });
        } catch (error) {
            console.error('Error updating statistics:', error);
        }
    }

    async logActivity(data) {
        try {
            const timestamp = new Date().toISOString();
            const activity = {
                ...data,
                timestamp,
                url: data.url || 'unknown'
            };

            // Store activity log (keep last 100 entries)
            const result = await chrome.storage.local.get(['activityLog']);
            const activityLog = result.activityLog || [];
            activityLog.push(activity);
            
            // Keep only last 100 entries
            if (activityLog.length > 100) {
                activityLog.splice(0, activityLog.length - 100);
            }

            await chrome.storage.local.set({ activityLog });
        } catch (error) {
            console.error('Error logging activity:', error);
        }
    }

    async getSettings(sendResponse) {
        try {
            const result = await chrome.storage.sync.get(['filterSettings', 'isEnabled']);
            sendResponse({
                filterSettings: result.filterSettings || {
                    showVerifiedOnly: false,
                    showUnverifiedOnly: false,
                    customMessage: ""
                },
                isEnabled: result.isEnabled || false
            });
        } catch (error) {
            console.error('Error getting settings:', error);
            sendResponse({
                filterSettings: {
                    showVerifiedOnly: false,
                    showUnverifiedOnly: false,
                    customMessage: ""
                },
                isEnabled: false
            });
        }
    }

    async saveSettings(data, sendResponse) {
        try {
            await chrome.storage.sync.set(data);
            sendResponse({ success: true });
        } catch (error) {
            console.error('Error saving settings:', error);
            sendResponse({ success: false, error: error.message });
        }
    }

    handleLinkedInPageLoad(tabId, tab) {
        // Inject content script if not already injected
        chrome.scripting.executeScript({
            target: { tabId: tabId },
            files: ['content.js']
        }).catch(error => {
            // Content script might already be injected
            console.log('Content script injection skipped:', error.message);
        });

        // Inject CSS
        chrome.scripting.insertCSS({
            target: { tabId: tabId },
            files: ['styles.css']
        }).catch(error => {
            console.log('CSS injection skipped:', error.message);
        });
    }

    // Utility methods
    async getCurrentTab() {
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        return tab;
    }

    async isLinkedInPage(tab) {
        return tab && tab.url && tab.url.includes('linkedin.com');
    }

    // Analytics and reporting
    async generateReport() {
        try {
            const [statistics, activityLog] = await Promise.all([
                chrome.storage.sync.get(['statistics']),
                chrome.storage.local.get(['activityLog'])
            ]);

            return {
                statistics: statistics.statistics,
                activityLog: activityLog.activityLog || [],
                generatedAt: new Date().toISOString()
            };
        } catch (error) {
            console.error('Error generating report:', error);
            return null;
        }
    }

    // Cleanup old data
    async cleanupOldData() {
        try {
            const result = await chrome.storage.local.get(['activityLog']);
            const activityLog = result.activityLog || [];
            
            // Keep only last 7 days of activity
            const sevenDaysAgo = new Date();
            sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);
            
            const filteredLog = activityLog.filter(activity => {
                return new Date(activity.timestamp) > sevenDaysAgo;
            });

            await chrome.storage.local.set({ activityLog: filteredLog });
        } catch (error) {
            console.error('Error cleaning up old data:', error);
        }
    }
}

// Initialize background script
new LinkedInFilterBackground();

// Cleanup old data on startup
chrome.runtime.onStartup.addListener(() => {
    const background = new LinkedInFilterBackground();
    background.cleanupOldData();
});

