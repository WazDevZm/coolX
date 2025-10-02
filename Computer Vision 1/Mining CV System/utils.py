#!/usr/bin/env python3
"""
Utility functions for Mining Computer Vision System
==================================================

This module contains utility functions for data processing, 
file operations, and system utilities.
"""

import cv2
import numpy as np
import json
import os
from datetime import datetime
import logging
from typing import Dict, List, Tuple, Optional
import math

def setup_logging(log_level: str = "INFO", log_file: str = "mining_cv.log") -> logging.Logger:
    """Setup logging configuration"""
    logger = logging.getLogger("MiningCV")
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

def save_detection_data(data: Dict, filename: str = None) -> str:
    """Save detection data to JSON file"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"detection_data_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    return filename

def load_detection_data(filename: str) -> Dict:
    """Load detection data from JSON file"""
    with open(filename, 'r') as f:
        return json.load(f)

def calculate_ore_value(ore_type: str, area: float, ore_types_config: Dict) -> float:
    """Calculate estimated value of detected ore"""
    if ore_type not in ore_types_config:
        return 0.0
    
    base_value = ore_types_config[ore_type]['value']
    # Simple area-based value calculation
    value_per_pixel = base_value / 1000  # Base value per 1000 pixels
    return area * value_per_pixel

def calculate_distance(point1: Tuple[int, int], point2: Tuple[int, int]) -> float:
    """Calculate Euclidean distance between two points"""
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def calculate_angle(point1: Tuple[int, int], point2: Tuple[int, int]) -> float:
    """Calculate angle between two points"""
    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]
    return math.degrees(math.atan2(dy, dx))

def resize_image(image: np.ndarray, max_width: int, max_height: int) -> np.ndarray:
    """Resize image while maintaining aspect ratio"""
    height, width = image.shape[:2]
    
    if width <= max_width and height <= max_height:
        return image
    
    scale = min(max_width/width, max_height/height)
    new_width = int(width * scale)
    new_height = int(height * scale)
    
    return cv2.resize(image, (new_width, new_height))

def enhance_image(image: np.ndarray, method: str = "clahe") -> np.ndarray:
    """Enhance image for better detection"""
    if method == "clahe":
        # Contrast Limited Adaptive Histogram Equalization
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        lab[:, :, 0] = clahe.apply(lab[:, :, 0])
        return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    
    elif method == "histogram":
        # Histogram equalization
        yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
        yuv[:, :, 0] = cv2.equalizeHist(yuv[:, :, 0])
        return cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
    
    elif method == "gamma":
        # Gamma correction
        gamma = 1.5
        lookup_table = np.array([((i / 255.0) ** (1.0 / gamma)) * 255
                                for i in np.arange(0, 256)]).astype("uint8")
        return cv2.LUT(image, lookup_table)
    
    return image

def detect_edges(image: np.ndarray, method: str = "canny") -> np.ndarray:
    """Detect edges in image"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    if method == "canny":
        return cv2.Canny(gray, 50, 150)
    elif method == "sobel":
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        return np.sqrt(sobelx**2 + sobely**2)
    elif method == "laplacian":
        return cv2.Laplacian(gray, cv2.CV_64F)
    
    return gray

def create_color_mask(image: np.ndarray, lower_color: Tuple[int, int, int], 
                     upper_color: Tuple[int, int, int]) -> np.ndarray:
    """Create color mask for specific color range"""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    return cv2.inRange(hsv, np.array(lower_color), np.array(upper_color))

def find_largest_contour(contours: List) -> Optional[np.ndarray]:
    """Find the largest contour from a list of contours"""
    if not contours:
        return None
    
    return max(contours, key=cv2.contourArea)

def draw_bounding_box(image: np.ndarray, contour: np.ndarray, 
                     color: Tuple[int, int, int] = (0, 255, 0), 
                     thickness: int = 2) -> np.ndarray:
    """Draw bounding box around contour"""
    x, y, w, h = cv2.boundingRect(contour)
    return cv2.rectangle(image, (x, y), (x + w, y + h), color, thickness)

def draw_contour_info(image: np.ndarray, contour: np.ndarray, 
                     text: str, color: Tuple[int, int, int] = (0, 255, 0)) -> np.ndarray:
    """Draw contour information on image"""
    x, y, w, h = cv2.boundingRect(contour)
    cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    return image

def calculate_contour_center(contour: np.ndarray) -> Tuple[int, int]:
    """Calculate center point of contour"""
    M = cv2.moments(contour)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        return (cx, cy)
    return (0, 0)

def is_contour_valid(contour: np.ndarray, min_area: int = 100) -> bool:
    """Check if contour meets minimum requirements"""
    area = cv2.contourArea(contour)
    return area >= min_area

def create_roi_mask(image_shape: Tuple[int, int], roi_points: List[Tuple[int, int]]) -> np.ndarray:
    """Create region of interest mask"""
    mask = np.zeros(image_shape[:2], dtype=np.uint8)
    if roi_points:
        points = np.array(roi_points, dtype=np.int32)
        cv2.fillPoly(mask, [points], 255)
    return mask

def apply_roi_mask(image: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """Apply region of interest mask to image"""
    return cv2.bitwise_and(image, image, mask=mask)

def calculate_image_statistics(image: np.ndarray) -> Dict:
    """Calculate basic image statistics"""
    mean_color = np.mean(image, axis=(0, 1))
    std_color = np.std(image, axis=(0, 1))
    
    return {
        'mean_bgr': mean_color.tolist(),
        'std_bgr': std_color.tolist(),
        'brightness': np.mean(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)),
        'contrast': np.std(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
    }

def create_heatmap(data: List[Tuple[int, int]], image_shape: Tuple[int, int]) -> np.ndarray:
    """Create heatmap from point data"""
    heatmap = np.zeros(image_shape[:2], dtype=np.float32)
    
    for x, y in data:
        if 0 <= x < image_shape[1] and 0 <= y < image_shape[0]:
            heatmap[y, x] += 1
    
    # Normalize heatmap
    if np.max(heatmap) > 0:
        heatmap = heatmap / np.max(heatmap)
    
    return heatmap

def format_timestamp(timestamp: str = None) -> str:
    """Format timestamp for display"""
    if timestamp is None:
        timestamp = datetime.now().isoformat()
    
    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def format_duration(seconds: float) -> str:
    """Format duration in human-readable format"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"

def validate_config(config: Dict) -> bool:
    """Validate configuration parameters"""
    required_keys = ['CAMERA_INDEX', 'MIN_ORE_AREA', 'ORE_TYPES']
    
    for key in required_keys:
        if key not in config:
            return False
    
    return True

def create_directory_if_not_exists(directory: str) -> bool:
    """Create directory if it doesn't exist"""
    try:
        os.makedirs(directory, exist_ok=True)
        return True
    except Exception as e:
        print(f"Error creating directory {directory}: {e}")
        return False

def get_file_size_mb(filename: str) -> float:
    """Get file size in MB"""
    try:
        size_bytes = os.path.getsize(filename)
        return size_bytes / (1024 * 1024)
    except:
        return 0.0

def cleanup_old_files(directory: str, max_files: int = 100) -> int:
    """Clean up old files, keeping only the most recent ones"""
    try:
        files = []
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                files.append((filepath, os.path.getmtime(filepath)))
        
        # Sort by modification time (newest first)
        files.sort(key=lambda x: x[1], reverse=True)
        
        # Remove old files
        removed_count = 0
        for filepath, _ in files[max_files:]:
            try:
                os.remove(filepath)
                removed_count += 1
            except:
                pass
        
        return removed_count
    except:
        return 0
