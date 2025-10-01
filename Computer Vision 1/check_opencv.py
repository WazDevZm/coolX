#!/usr/bin/env python3
"""
OpenCV Installation Checker
===========================

This script checks your OpenCV installation and provides diagnostic information.
"""

import sys
import cv2

def check_opencv_installation():
    """Check OpenCV installation and available modules"""
    print("🔍 OpenCV Installation Diagnostic")
    print("=" * 50)
    
    # Check OpenCV version
    print(f"OpenCV Version: {cv2.__version__}")
    print(f"Python Version: {sys.version}")
    print()
    
    # Check available attributes
    print("📋 Checking OpenCV modules...")
    
    # Essential modules for our application
    essential_modules = [
        'VideoCapture',
        'imread',
        'imshow',
        'waitKey',
        'destroyAllWindows',
        'cvtColor',
        'GaussianBlur',
        'absdiff',
        'threshold',
        'findContours',
        'contourArea',
        'boundingRect',
        'rectangle',
        'putText',
        'FONT_HERSHEY_SIMPLEX',
        'flip',
        'getStructuringElement',
        'morphologyEx',
        'MORPH_ELLIPSE',
        'MORPH_OPEN',
        'MORPH_CLOSE',
        'THRESH_BINARY',
        'RETR_EXTERNAL',
        'CHAIN_APPROX_SIMPLE'
    ]
    
    available_modules = []
    missing_modules = []
    
    for module in essential_modules:
        if hasattr(cv2, module):
            available_modules.append(module)
            print(f"✅ {module}")
        else:
            missing_modules.append(module)
            print(f"❌ {module} - MISSING")
    
    print()
    print(f"📊 Summary:")
    print(f"   Available: {len(available_modules)}/{len(essential_modules)}")
    print(f"   Missing: {len(missing_modules)}")
    
    if missing_modules:
        print()
        print("⚠️  Missing critical modules:")
        for module in missing_modules:
            print(f"   - {module}")
    
    # Check if VideoCapture works
    print()
    print("🎥 Testing VideoCapture...")
    try:
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("✅ VideoCapture(0) - SUCCESS")
            ret, frame = cap.read()
            if ret:
                print("✅ Frame reading - SUCCESS")
                print(f"   Frame shape: {frame.shape}")
            else:
                print("❌ Frame reading - FAILED")
            cap.release()
        else:
            print("❌ VideoCapture(0) - FAILED (Camera not accessible)")
    except Exception as e:
        print(f"❌ VideoCapture test failed: {e}")
    
    # Recommendations
    print()
    print("💡 Recommendations:")
    if missing_modules:
        print("1. Reinstall OpenCV with video support:")
        print("   pip uninstall opencv-python")
        print("   pip install opencv-python")
        print()
        print("2. If that doesn't work, try:")
        print("   pip install opencv-contrib-python")
    else:
        print("✅ OpenCV installation looks good!")
        print("   The issue might be with camera access or permissions.")

if __name__ == "__main__":
    check_opencv_installation()
