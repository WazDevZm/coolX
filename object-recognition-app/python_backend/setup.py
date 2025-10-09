#!/usr/bin/env python3
"""
Setup script for Object Detection Backend
Installs required dependencies and downloads YOLO model
"""

import subprocess
import sys
import os

def install_requirements():
    """Install Python requirements"""
    print("Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def download_yolo_model():
    """Download YOLO model"""
    print("Downloading YOLO model...")
    try:
        from ultralytics import YOLO
        model = YOLO('yolov8n.pt')  # This will download the model
        print("✅ YOLO model downloaded successfully!")
        return True
    except Exception as e:
        print(f"❌ Error downloading YOLO model: {e}")
        return False

def main():
    print("🚀 Setting up Object Detection Backend...")
    print("=" * 50)
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed at dependency installation")
        return False
    
    # Download YOLO model
    if not download_yolo_model():
        print("❌ Setup failed at model download")
        return False
    
    print("=" * 50)
    print("✅ Setup completed successfully!")
    print("📝 To start the backend server, run:")
    print("   python server.py")
    print("🌐 The API will be available at: http://localhost:5000")
    
    return True

if __name__ == "__main__":
    main()
