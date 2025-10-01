# Smart Security Monitor 🔒

A comprehensive computer vision application for real-time security monitoring using your webcam.

## Features

- **Real-time Motion Detection**: Advanced background subtraction algorithm to detect movement
- **Object Tracking**: Visual bounding boxes around detected objects with area measurements
- **Configurable Sensitivity**: Adjustable detection parameters for different environments
- **Audio Alerts**: System beeps when motion is detected (configurable)
- **Event Logging**: Complete log of all security events with timestamps
- **Statistics Dashboard**: Live session statistics and detection counts
- **Report Generation**: Export security reports to JSON format
- **Modern GUI**: Clean, intuitive interface built with Tkinter

## Installation

1. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   python main.py
   ```

## Usage

1. **Start Monitoring**: Click the "Start Monitoring" button to begin
2. **Adjust Settings**: Use the sensitivity and minimum area sliders to fine-tune detection
3. **View Live Feed**: Watch the real-time video feed with motion detection overlays
4. **Monitor Statistics**: Check the status panel for detection counts and session time
5. **Review Events**: Use "View Log" to see all detected events
6. **Save Reports**: Export security reports for analysis

## Technical Details

### Computer Vision Techniques
- **Background Subtraction**: MOG2 algorithm for robust motion detection
- **Morphological Operations**: Noise reduction and contour refinement
- **Contour Analysis**: Object detection and area calculation
- **Real-time Processing**: Multi-threaded video processing for smooth performance

### Architecture
- **GUI Framework**: Tkinter for cross-platform compatibility
- **Video Processing**: OpenCV for computer vision operations
- **Threading**: Separate threads for video processing and UI updates
- **Event System**: Comprehensive logging and reporting system

## Use Cases

- **Home Security**: Monitor entryways and sensitive areas
- **Office Monitoring**: Track activity in restricted zones
- **Pet Monitoring**: Watch for pet movement and activity
- **Research**: Study motion patterns and behavior analysis
- **Accessibility**: Assist users with visual impairments

## Configuration

- **Sensitivity**: 10-100 (higher = more sensitive)
- **Minimum Area**: 500-5000 pixels (larger = fewer false positives)
- **Audio Alerts**: Enable/disable system beeps
- **Detection Zones**: Future feature for area-specific monitoring

## Requirements

- Python 3.7+
- Webcam/Camera access
- Windows/macOS/Linux compatible
- OpenCV, NumPy, Pillow libraries

## Troubleshooting

- **Camera Access**: Ensure your webcam is not being used by other applications
- **Performance**: Adjust sensitivity and minimum area for optimal performance
- **Audio**: Audio alerts work on Windows; other systems use console beeps

## Future Enhancements

- Face detection and recognition
- Multiple camera support
- Cloud storage integration
- Mobile app companion
- Advanced analytics dashboard
