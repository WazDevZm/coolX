// LinkedIn Connection Filter Popup Script
class LinkedInFilterPopup {
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
        this.loadSettings();
        this.setupEventListeners();
        this.updateUI();
    }

    async loadSettings() {
        try {
            const result = await chrome.storage.sync.get(['filterSettings', 'isEnabled']);
            this.filterSettings = result.filterSettings || this.filterSettings;
            this.isEnabled = result.isEnabled || false;
        } catch (error) {
            console.error('Error loading settings:', error);
        }
    }

    async saveSettings() {
        try {
            await chrome.storage.sync.set({
                filterSettings: this.filterSettings,
                isEnabled: this.isEnabled
            });
        } catch (error) {
            console.error('Error saving settings:', error);
        }
    }

    setupEventListeners() {
        // Filter type radio buttons
        document.querySelectorAll('input[name="filterType"]').forEach(radio => {
            radio.addEventListener('change', (e) => {
                this.updateFilterSettings(e.target.value);
            });
        });

        // Toggle filter button
        document.getElementById('toggleFilter').addEventListener('click', () => {
            this.toggleFilter();
        });

        // Clear filter button
        document.getElementById('clearFilter').addEventListener('click', () => {
            this.clearFilter();
        });

        // Send invite button
        document.getElementById('sendInviteBtn').addEventListener('click', () => {
            this.sendConnectionInvite();
        });

        // Refresh page button
        document.getElementById('refreshPage').addEventListener('click', () => {
            this.refreshPage();
        });

        // Help and settings links
        document.getElementById('helpLink').addEventListener('click', (e) => {
            e.preventDefault();
            this.showHelp();
        });

        document.getElementById('settingsLink').addEventListener('click', (e) => {
            e.preventDefault();
            this.showSettings();
        });
    }

    updateFilterSettings(filterType) {
        this.filterSettings.showVerifiedOnly = filterType === 'verified';
        this.filterSettings.showUnverifiedOnly = filterType === 'unverified';
        this.saveSettings();
        this.sendMessageToContentScript('updateSettings', this.filterSettings);
    }

    async toggleFilter() {
        this.isEnabled = !this.isEnabled;
        await this.saveSettings();
        this.updateUI();
        this.sendMessageToContentScript('toggleFilter', { enabled: this.isEnabled });
    }

    clearFilter() {
        this.sendMessageToContentScript('clearFilter');
        this.updateUI();
    }

    async sendConnectionInvite() {
        const profileUrl = document.getElementById('profileUrl').value;
        const message = document.getElementById('customMessage').value;

        if (!profileUrl) {
            this.showNotification('Please enter a profile URL', 'error');
            return;
        }

        if (!message.trim()) {
            this.showNotification('Please enter a message', 'error');
            return;
        }

        try {
            // Send message to content script
            const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
            await chrome.tabs.sendMessage(tab.id, {
                action: 'sendInvite',
                profileUrl: profileUrl,
                message: message
            });

            this.showNotification('Connection invite sent!', 'success');
            document.getElementById('profileUrl').value = '';
            document.getElementById('customMessage').value = '';
        } catch (error) {
            console.error('Error sending invite:', error);
            this.showNotification('Error sending invite. Make sure you\'re on LinkedIn.', 'error');
        }
    }

    refreshPage() {
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
            chrome.tabs.reload(tabs[0].id);
        });
    }

    sendMessageToContentScript(action, data = {}) {
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
            if (tabs[0]) {
                chrome.tabs.sendMessage(tabs[0].id, {
                    action: action,
                    ...data
                });
            }
        });
    }

    updateUI() {
        // Update status indicator
        const statusIndicator = document.getElementById('statusIndicator');
        const statusText = document.getElementById('statusText');
        
        if (this.isEnabled) {
            statusIndicator.classList.add('active');
            statusText.textContent = 'Active';
        } else {
            statusIndicator.classList.remove('active');
            statusText.textContent = 'Inactive';
        }

        // Update filter radio buttons
        if (this.filterSettings.showVerifiedOnly) {
            document.getElementById('verifiedOnly').checked = true;
        } else if (this.filterSettings.showUnverifiedOnly) {
            document.getElementById('unverifiedOnly').checked = true;
        } else {
            document.getElementById('showAll').checked = true;
        }

        // Update toggle button text
        const toggleBtn = document.getElementById('toggleFilter');
        toggleBtn.textContent = this.isEnabled ? 'Disable Filter' : 'Enable Filter';
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        // Add to page
        document.body.appendChild(notification);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

    showHelp() {
        const helpText = `
LinkedIn Connection Filter Help:

1. Filter Options:
   - Verified Users Only: Shows only verified LinkedIn users
   - Unverified Users Only: Shows only unverified users
   - Show All: Shows all connection requests

2. Send Connection Invite:
   - Enter a LinkedIn profile URL
   - Add a custom message
   - Click "Send Invite" to send the connection request

3. Quick Actions:
   - Toggle Filter: Enable/disable the filter
   - Clear Filter: Remove all filters
   - Refresh Page: Reload the current page

Note: This extension works on LinkedIn.com pages.
        `;
        
        alert(helpText);
    }

    showSettings() {
        // For now, just show a simple settings message
        this.showNotification('Settings panel coming soon!', 'info');
    }

    async updateStatistics() {
        try {
            // Get statistics from content script
            const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
            const response = await chrome.tabs.sendMessage(tab.id, { action: 'getStatistics' });
            
            if (response) {
                document.getElementById('totalConnections').textContent = response.total || 0;
                document.getElementById('verifiedConnections').textContent = response.verified || 0;
                document.getElementById('unverifiedConnections').textContent = response.unverified || 0;
            }
        } catch (error) {
            console.error('Error getting statistics:', error);
        }
    }
}

// Initialize popup when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new LinkedInFilterPopup();
});

