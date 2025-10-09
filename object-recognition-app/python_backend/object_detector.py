import cv2
import numpy as np
from ultralytics import YOLO
import base64
from PIL import Image
import io
import json

class ObjectDetector:
    def __init__(self):
        # Load YOLOv8 model (will download automatically on first run)
        self.model = YOLO('yolov8n.pt')  # nano version for speed
        print("YOLO model loaded successfully!")
    
    def detect_objects(self, image_data):
        """
        Detect objects in image using YOLO
        Args:
            image_data: Base64 encoded image or image path
        Returns:
            List of detected objects with confidence scores
        """
        try:
            # Decode base64 image if needed
            if isinstance(image_data, str) and image_data.startswith('data:image'):
                # Remove data URL prefix
                image_data = image_data.split(',')[1]
            
            # Decode base64 to image
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert PIL to OpenCV format
            opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Run YOLO detection
            results = self.model(opencv_image)
            
            detections = []
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        # Get class name and confidence
                        class_id = int(box.cls[0])
                        class_name = self.model.names[class_id]
                        confidence = float(box.conf[0])
                        
                        # Only include high-confidence detections
                        if confidence > 0.5:
                            detections.append({
                                'class': class_name,
                                'confidence': confidence,
                                'bbox': box.xyxy[0].tolist()  # bounding box coordinates
                            })
            
            # Sort by confidence (highest first)
            detections.sort(key=lambda x: x['confidence'], reverse=True)
            
            return detections[:5]  # Return top 5 detections
            
        except Exception as e:
            print(f"Error in object detection: {e}")
            return []
    
    def get_class_names(self):
        """Get list of all possible class names"""
        return list(self.model.names.values())

# Initialize detector
detector = ObjectDetector()

def detect_objects_in_image(image_data):
    """Main function to detect objects in image"""
    return detector.detect_objects(image_data)
