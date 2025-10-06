# LinkedIn Connection Filter & Manager

A Chrome extension that helps you filter LinkedIn connection invites by verification status and send connection requests with custom messages.

## 🚀 Features

### Connection Filtering
- **Verified Users Only**: Show only verified LinkedIn users in your connection requests
- **Unverified Users Only**: Show only unverified users
- **Show All**: Display all connection requests (default)

### Connection Management
- **Send Custom Messages**: Send connection invites with personalized messages
- **Quick Actions**: Toggle filters, clear filters, and refresh pages
- **Real-time Statistics**: Track total, verified, and unverified connections

### Smart Detection
- Automatically detects verification status using LinkedIn's verification badges
- Works with LinkedIn's current UI structure
- Real-time filtering as new connection requests arrive

## 📦 Installation

### From Source
1. Download or clone this repository
2. Open Chrome and navigate to `chrome://extensions/`
3. Enable "Developer mode" in the top right
4. Click "Load unpacked" and select the extension folder
5. The extension will appear in your Chrome toolbar

### Files Structure
```
LinkedIn_Connection_Filter/
├── manifest.json          # Extension configuration
├── content.js             # Main content script
├── popup.html             # Extension popup UI
├── popup.js               # Popup functionality
├── popup.css              # Popup styling
├── styles.css             # Content script styling
├── background.js          # Background service worker
└── README.md              # This file
```

## 🛠️ Usage

### Filtering Connections
1. Navigate to LinkedIn's "My Network" or "Connections" page
2. Click the extension icon in your Chrome toolbar
3. Select your preferred filter option:
   - **Verified Users Only**: Shows only verified LinkedIn users
   - **Unverified Users Only**: Shows only unverified users
   - **Show All**: Shows all connection requests
4. Click "Apply Filter" to activate the filter

### Sending Connection Invites
1. Open the extension popup
2. Enter a LinkedIn profile URL in the "Profile URL" field
3. Add a custom message in the "Message" field
4. Click "Send Invite" to send the connection request

### Quick Actions
- **Toggle Filter**: Enable/disable the current filter
- **Clear Filter**: Remove all active filters
- **Refresh Page**: Reload the current LinkedIn page

## 🔧 Technical Details

### Permissions
- `activeTab`: Access to the current LinkedIn tab
- `storage`: Save user preferences and settings
- `scripting`: Inject content scripts into LinkedIn pages
- `host_permissions`: Access to linkedin.com domain

### How It Works
1. **Content Script Injection**: Automatically injects into LinkedIn pages
2. **DOM Monitoring**: Uses MutationObserver to detect new connection requests
3. **Verification Detection**: Scans for LinkedIn verification badges and indicators
4. **Real-time Filtering**: Applies filters as new content loads
5. **Message Integration**: Automates the connection request process

### Verification Detection
The extension looks for these indicators:
- `.verified-badge` elements
- `.premium-badge` elements
- `[data-test-id="verified-badge"]` attributes
- Text content containing "verified", "premium", or "pro"

## 🎨 UI Features

### Modern Design
- Clean, professional interface
- LinkedIn-inspired color scheme
- Responsive design for different screen sizes
- Smooth animations and transitions

### Status Indicators
- Real-time filter status
- Connection statistics
- Visual feedback for actions

## 🔒 Privacy & Security

- **No Data Collection**: The extension doesn't collect or store personal data
- **Local Storage Only**: All settings are stored locally in your browser
- **LinkedIn Integration**: Works entirely within LinkedIn's existing interface
- **No External Requests**: No data is sent to external servers

## 🐛 Troubleshooting

### Common Issues

**Extension not working on LinkedIn:**
- Make sure you're on a LinkedIn page (linkedin.com)
- Refresh the page after installing the extension
- Check that the extension is enabled in Chrome

**Filter not applying:**
- Click "Apply Filter" after selecting your filter option
- Try refreshing the LinkedIn page
- Check the extension popup for any error messages

**Connection invites not sending:**
- Ensure you're on a LinkedIn profile page
- Check that the profile URL is correct
- Make sure you have permission to send connection requests

### Debug Mode
1. Open Chrome DevTools (F12)
2. Go to the Console tab
3. Look for messages starting with "LinkedIn Filter:"
4. Check for any error messages

## 🔄 Updates

The extension automatically updates when new versions are available. You can also manually check for updates in Chrome's extension management page.

## 📝 Changelog

### Version 1.0.0
- Initial release
- Basic connection filtering by verification status
- Custom message sending for connection invites
- Modern UI with LinkedIn-inspired design
- Real-time statistics and monitoring

## 🤝 Contributing

This extension is open source. Feel free to:
- Report bugs and issues
- Suggest new features
- Submit pull requests
- Improve the documentation

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

## 🙏 Acknowledgments

- LinkedIn for providing the platform
- Chrome Extensions API for the development framework
- Open source community for inspiration and tools

---

**Note**: This extension is not affiliated with LinkedIn. It's a third-party tool designed to enhance your LinkedIn experience.
