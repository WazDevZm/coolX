# Mining Computer Vision System

A comprehensive computer vision system designed specifically for mining operations, providing real-time monitoring, safety compliance, and operational analytics.

## Features

### 🔍 Ore Detection & Classification
- Real-time ore detection using color-based classification
- Support for multiple ore types (Iron, Copper, Gold, Silver)
- Value estimation for detected ores
- Historical detection tracking

### 🛡️ Safety Monitoring
- Helmet detection for PPE compliance
- Face detection and safety violation alerts
- Real-time safety status monitoring
- Violation logging and reporting

### 🔧 Equipment Monitoring
- Mining equipment health assessment
- Rust detection and corrosion monitoring
- Oil leak detection
- Equipment status alerts

### 🌍 Environmental Monitoring
- Dust level detection and monitoring
- Gas detection (simplified visual analysis)
- Environmental condition tracking
- Alert system for hazardous conditions

### 📊 Analytics Dashboard
- Real-time detection statistics
- System alerts and notifications
- Historical data visualization
- Comprehensive reporting system

## Installation

1. **Clone or download the project**
2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

## Usage

### Starting the System
1. Launch the application
2. Select your desired monitoring module:
   - **Ore Detection**: Identifies and classifies different ore types
   - **Safety Monitoring**: Ensures PPE compliance
   - **Equipment Monitoring**: Tracks equipment health
   - **Environmental Monitoring**: Monitors environmental conditions

3. Click "Start System" to begin real-time monitoring
4. Use "Capture Image" to save current frames
5. Generate reports using "Generate Report"

### Modules

#### Ore Detection Module
- Automatically detects ore based on color characteristics
- Classifies ores by type and estimates value
- Tracks detection history and statistics

#### Safety Monitoring Module
- Detects faces and checks for helmet compliance
- Issues safety violation alerts
- Maintains safety compliance records

#### Equipment Monitoring Module
- Monitors large equipment objects
- Detects rust, oil leaks, and other issues
- Provides equipment health assessments

#### Environmental Monitoring Module
- Monitors dust levels in the environment
- Detects potential gas presence
- Tracks environmental conditions

## Configuration

### Ore Types
The system supports configurable ore types in the `ore_types` dictionary:
```python
ore_types = {
    'iron': {'color_range': [(0, 50, 50), (20, 255, 255)], 'value': 100},
    'copper': {'color_range': [(10, 100, 100), (30, 255, 255)], 'value': 150},
    'gold': {'color_range': [(20, 100, 100), (40, 255, 255)], 'value': 500},
    'silver': {'color_range': [(0, 0, 100), (180, 30, 255)], 'value': 200}
}
```

### Detection Parameters
- Minimum area threshold for ore detection: 500 pixels
- Face detection scale factor: 1.1
- Equipment health assessment thresholds

## Data Output

### Detection Logs
All detections are logged with timestamps, positions, and metadata:
```json
{
    "timestamp": "2024-01-01T12:00:00",
    "ore_type": "gold",
    "value": 500,
    "area": 1200,
    "position": [100, 150, 50, 60]
}
```

### Reports
Comprehensive JSON reports include:
- Total detection counts
- Safety violations
- Equipment alerts
- Environmental data
- Estimated ore values

## Safety Features

- **Real-time Alerts**: Immediate notification of safety violations
- **PPE Compliance**: Automatic helmet detection
- **Environmental Monitoring**: Gas and dust level tracking
- **Equipment Health**: Proactive maintenance alerts

## Technical Requirements

- Python 3.8+
- OpenCV 4.12+
- Webcam or video input
- Minimum 4GB RAM recommended
- Windows/Linux/macOS compatible

## Troubleshooting

### Camera Issues
- Ensure camera is connected and not used by other applications
- Try different camera indices (0, 1, 2) in the code
- Check camera permissions

### Performance Issues
- Reduce video resolution for better performance
- Close other applications using the camera
- Ensure adequate lighting for better detection

### Detection Accuracy
- Ensure good lighting conditions
- Adjust color ranges for your specific ore types
- Calibrate detection parameters for your environment

## Contributing

This system is designed to be modular and extensible. Key areas for enhancement:
- Machine learning model integration
- Advanced safety equipment detection
- Integration with mining databases
- Real-time data streaming
- Mobile app integration

## License

This project is open source and available under the MIT License.

## Support

For technical support or feature requests, please refer to the project documentation or contact the development team.
