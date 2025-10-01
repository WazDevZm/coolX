#!/usr/bin/env python3
"""
OpenCV Installation Fixer
=========================

This script helps fix OpenCV installation issues.
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and show the result"""
    print(f"\n🔧 {description}")
    print(f"Running: {command}")
    print("-" * 50)
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ SUCCESS")
            if result.stdout:
                print(result.stdout)
        else:
            print("❌ FAILED")
            if result.stderr:
                print(f"Error: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def main():
    print("🔧 OpenCV Installation Fixer")
    print("=" * 50)
    print("This script will help fix OpenCV installation issues.")
    print()
    
    # Check current installation
    print("📋 Checking current OpenCV installation...")
    try:
        import cv2
        print(f"✅ OpenCV version: {cv2.__version__}")
        
        # Test VideoCapture
        if hasattr(cv2, 'VideoCapture'):
            print("✅ VideoCapture is available")
        else:
            print("❌ VideoCapture is missing")
            
    except ImportError:
        print("❌ OpenCV is not installed")
    
    print("\n" + "=" * 50)
    print("🔧 FIXING OPENCV INSTALLATION")
    print("=" * 50)
    
    # Step 1: Uninstall existing OpenCV
    print("\n1️⃣ Uninstalling existing OpenCV packages...")
    run_command("pip uninstall opencv-python opencv-contrib-python -y", 
                "Removing existing OpenCV packages")
    
    # Step 2: Install OpenCV with video support
    print("\n2️⃣ Installing OpenCV with video support...")
    success = run_command("pip install opencv-python", 
                         "Installing opencv-python")
    
    if not success:
        print("\n3️⃣ Trying alternative installation...")
        run_command("pip install opencv-contrib-python", 
                   "Installing opencv-contrib-python")
    
    # Step 3: Verify installation
    print("\n4️⃣ Verifying installation...")
    try:
        import cv2
        print(f"✅ OpenCV version: {cv2.__version__}")
        
        if hasattr(cv2, 'VideoCapture'):
            print("✅ VideoCapture is available")
            
            # Test camera access
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                print("✅ Camera access: SUCCESS")
                cap.release()
            else:
                print("⚠️ Camera access: FAILED (camera may be in use)")
        else:
            print("❌ VideoCapture is still missing")
            
    except ImportError as e:
        print(f"❌ OpenCV import failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 NEXT STEPS")
    print("=" * 50)
    print("1. Run the diagnostic script: python check_opencv.py")
    print("2. Try running the main application: python main.py")
    print("3. If issues persist, try:")
    print("   - Restart your terminal/command prompt")
    print("   - Check if your camera is being used by another application")
    print("   - Try running as administrator (Windows)")

if __name__ == "__main__":
    main()
