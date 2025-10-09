# Object Detection Backend

Real-time object detection using YOLOv8 and OpenCV for the React Native app.

## Features

- 🎯 **Real Object Detection** - Uses YOLOv8 (YOLO v8) for accurate object recognition
- 🚀 **Fast Processing** - Optimized for mobile app integration
- 📱 **80 Object Classes** - Detects people, vehicles, animals, food, and more
- 🔄 **REST API** - Simple HTTP endpoints for easy integration
- 📊 **Confidence Scores** - Real accuracy percentages for each detection

## Setup

### 1. Install Python Dependencies

```bash
# Navigate to python_backend directory
cd python_backend

# Install dependencies
python setup.py
```

### 2. Start the Backend Server

```bash
python server.py
```

The API will be available at: `http://localhost:5000`

## API Endpoints

### POST /detect
Detect objects in an image

**Request:**
```json
{
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ..."
}
```

**Response:**
```json
{
  "success": true,
  "detections": [
    {
      "class": "person",
      "confidence": 0.95,
      "bbox": [100, 200, 300, 400]
    }
  ],
  "count": 1
}
```

### GET /health
Health check endpoint

### GET /classes
Get list of all possible object classes

## Object Classes Detected

The YOLO model can detect 80 different object classes including:

- **People**: person
- **Vehicles**: car, truck, bus, motorcycle, bicycle, airplane, train, boat
- **Animals**: dog, cat, horse, cow, sheep, bird, elephant, bear, zebra, giraffe
- **Food**: banana, apple, sandwich, pizza, donut, cake, hot dog, orange
- **Furniture**: chair, couch, bed, dining table, toilet
- **Electronics**: laptop, mouse, remote, keyboard, cell phone, tv, microwave, oven
- **Sports**: sports ball, tennis racket, baseball bat, baseball glove, skateboard, surfboard
- **And many more...**

## Technical Details

- **Model**: YOLOv8n (nano version for speed)
- **Framework**: Ultralytics YOLO
- **Backend**: Flask with CORS support
- **Image Processing**: OpenCV and PIL
- **Confidence Threshold**: 0.5 (50% minimum confidence)

## Performance

- **Processing Time**: ~1-3 seconds per image
- **Model Size**: ~6MB (YOLOv8n)
- **Memory Usage**: ~200-300MB
- **Accuracy**: 80 COCO classes with high precision

## Troubleshooting

### Common Issues

1. **Model Download Fails**
   - Check internet connection
   - Run `python setup.py` again

2. **Port 5000 Already in Use**
   - Change port in `server.py`: `app.run(port=5001)`
   - Update React Native app to use new port

3. **CORS Errors**
   - Make sure Flask-CORS is installed
   - Check that CORS is enabled in server.py

### Performance Tips

- Use YOLOv8n for speed (current)
- Use YOLOv8s for better accuracy
- Use YOLOv8m for best accuracy (slower)

## Development

To modify the detection logic, edit `object_detector.py`:

```python
# Change confidence threshold
if confidence > 0.3:  # Lower threshold = more detections

# Change model size
self.model = YOLO('yolov8s.pt')  # Small model for better accuracy
```
