#!/usr/bin/env python3
"""
Configuration file for Mining Computer Vision System
==================================================

This file contains all configurable parameters for the mining CV system.
Modify these settings to customize the system for your specific mining operation.
"""

# Camera Settings
CAMERA_INDEX = 0  # Try 0, 1, 2 if camera not detected
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
FPS_TARGET = 30

# Detection Parameters
MIN_ORE_AREA = 500  # Minimum area for ore detection (pixels)
MIN_EQUIPMENT_AREA = 1000  # Minimum area for equipment detection (pixels)
FACE_DETECTION_SCALE = 1.1
FACE_DETECTION_NEIGHBORS = 4

# Ore Classification
ORE_TYPES = {
    'iron': {
        'color_range': [(0, 50, 50), (20, 255, 255)],
        'value': 100,
        'color': (0, 255, 0)  # Green
    },
    'copper': {
        'color_range': [(10, 100, 100), (30, 255, 255)],
        'value': 150,
        'color': (0, 255, 255)  # Yellow
    },
    'gold': {
        'color_range': [(20, 100, 100), (40, 255, 255)],
        'value': 500,
        'color': (0, 255, 255)  # Yellow
    },
    'silver': {
        'color_range': [(0, 0, 100), (180, 30, 255)],
        'value': 200,
        'color': (255, 255, 255)  # White
    },
    'coal': {
        'color_range': [(0, 0, 0), (180, 255, 50)],
        'value': 80,
        'color': (0, 0, 0)  # Black
    }
}

# Safety Monitoring
HELMET_DETECTION_THRESHOLD = 0.1  # Minimum bright pixel ratio for helmet detection
SAFETY_VIOLATION_COOLDOWN = 5  # Seconds between violation alerts

# Equipment Monitoring
RUST_DETECTION_THRESHOLD = 0.1  # Minimum rust pixel ratio
OIL_LEAK_THRESHOLD = 0.2  # Minimum oil pixel ratio
EQUIPMENT_HEALTH_CHECK_INTERVAL = 10  # Seconds between health checks

# Environmental Monitoring
DUST_DETECTION_SENSITIVITY = 100  # Dust detection threshold
GAS_DETECTION_HUE_THRESHOLD = 100  # Unusual hue threshold
GAS_DETECTION_SATURATION_THRESHOLD = 50  # Low saturation threshold

# UI Settings
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
VIDEO_WIDTH = 600
VIDEO_HEIGHT = 400
ANALYTICS_REFRESH_RATE = 1  # Seconds

# Data Storage
MAX_DETECTION_HISTORY = 1000
MAX_VIOLATIONS = 500
MAX_ALERTS = 500
REPORT_SAVE_DIRECTORY = "reports"
IMAGE_SAVE_DIRECTORY = "captures"

# Alert Settings
ENABLE_AUDIO_ALERTS = True
ENABLE_VISUAL_ALERTS = True
ALERT_DURATION = 3  # Seconds

# Performance Settings
PROCESSING_THREAD_PRIORITY = "normal"
ENABLE_GPU_ACCELERATION = False  # Set to True if CUDA is available
MEMORY_OPTIMIZATION = True

# Logging
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_FILE = "mining_cv.log"
ENABLE_CONSOLE_LOGGING = True

# Export Settings
EXPORT_FORMAT = "json"  # json, csv, xml
INCLUDE_IMAGES_IN_REPORT = False
REPORT_COMPRESSION = True

# Advanced Features
ENABLE_MACHINE_LEARNING = False  # Requires additional ML models
ENABLE_DEEP_LEARNING = False  # Requires TensorFlow/PyTorch
ENABLE_REAL_TIME_STREAMING = False  # For network streaming
ENABLE_DATABASE_INTEGRATION = False  # For database storage

# Mining Site Specific Settings
SITE_NAME = "Default Mining Site"
SITE_LOCATION = "Unknown"
OPERATION_TYPE = "Underground"  # Underground, Surface, Quarry
SHIFT_DURATION = 8  # Hours
MAX_WORKERS_PER_SHIFT = 50

# Safety Thresholds
MAX_SAFETY_VIOLATIONS_PER_HOUR = 5
CRITICAL_SAFETY_THRESHOLD = 3
EQUIPMENT_MAINTENANCE_THRESHOLD = 10
ENVIRONMENTAL_ALERT_THRESHOLD = 5

# Notification Settings
EMAIL_ALERTS = False
SMS_ALERTS = False
WEBHOOK_URL = None
DISCORD_WEBHOOK = None
SLACK_WEBHOOK = None

# Integration Settings
API_ENDPOINT = None
API_KEY = None
ENABLE_CLOUD_SYNC = False
CLOUD_PROVIDER = "aws"  # aws, azure, gcp
