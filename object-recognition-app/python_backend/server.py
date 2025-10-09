from flask import Flask, request, jsonify
from flask_cors import CORS
from object_detector import detect_objects_in_image
import base64
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for React Native app

@app.route('/detect', methods=['POST'])
def detect_objects():
    """
    API endpoint for object detection
    Expects JSON with 'image' field containing base64 encoded image
    """
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({'error': 'No image data provided'}), 400
        
        image_data = data['image']
        
        # Detect objects using YOLO
        detections = detect_objects_in_image(image_data)
        
        # Format response
        response = {
            'success': True,
            'detections': detections,
            'count': len(detections)
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"Error in API: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'object-detection-api'})

@app.route('/classes', methods=['GET'])
def get_classes():
    """Get list of all possible object classes"""
    try:
        from object_detector import detector
        classes = detector.get_class_names()
        return jsonify({'classes': classes})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting Object Detection API Server...")
    print("YOLO model will be downloaded on first request...")
    app.run(host='0.0.0.0', port=5000, debug=True)
