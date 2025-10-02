#!/usr/bin/env python3
"""
Mining Computer Vision System
============================

A comprehensive computer vision system designed specifically for mining operations.
This system provides multiple modules to enhance safety, efficiency, and monitoring
in mining environments.

Features:
- Ore Detection & Classification
- Safety Monitoring (PPE Compliance)
- Equipment Monitoring
- Environmental Monitoring
- Real-time Analytics Dashboard
- Data Logging & Reporting

Author: AI Assistant
Dependencies: opencv-python, numpy, tkinter, scikit-learn, matplotlib
"""

import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
import json
import os
from datetime import datetime
import math
try:
    from sklearn.cluster import KMeans
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    KMeans = None

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    plt = None

from collections import deque
import warnings
warnings.filterwarnings('ignore')

class MiningCVSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Mining Computer Vision System")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1a1a1a')
        
        # System state
        self.camera = None
        self.is_running = False
        self.current_module = "ore_detection"
        
        # Data storage
        self.detection_history = deque(maxlen=1000)
        self.safety_violations = []
        self.equipment_alerts = []
        self.environmental_data = []
        
        # Detection parameters
        self.ore_detection_enabled = True
        self.safety_monitoring_enabled = True
        self.equipment_monitoring_enabled = True
        self.environmental_monitoring_enabled = True
        
        # Ore classification model (simplified)
        self.ore_types = {
            'iron': {'color_range': [(0, 50, 50), (20, 255, 255)], 'value': 100},
            'copper': {'color_range': [(10, 100, 100), (30, 255, 255)], 'value': 150},
            'gold': {'color_range': [(20, 100, 100), (40, 255, 255)], 'value': 500},
            'silver': {'color_range': [(0, 0, 100), (180, 30, 255)], 'value': 200}
        }
        
        self.setup_ui()
        self.setup_camera()
        
    def setup_ui(self):
        """Setup the main user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(main_frame, text="Mining Computer Vision System", 
                              font=('Arial', 16, 'bold'), fg='white', bg='#1a1a1a')
        title_label.pack(pady=(0, 10))
        
        # Control panel
        control_frame = ttk.LabelFrame(main_frame, text="System Controls", padding=10)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Module selection
        module_frame = ttk.Frame(control_frame)
        module_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(module_frame, text="Active Module:").pack(side=tk.LEFT)
        self.module_var = tk.StringVar(value="ore_detection")
        module_combo = ttk.Combobox(module_frame, textvariable=self.module_var, 
                                   values=["ore_detection", "safety_monitoring", 
                                          "equipment_monitoring", "environmental_monitoring"],
                                   state="readonly", width=20)
        module_combo.pack(side=tk.LEFT, padx=(10, 0))
        module_combo.bind('<<ComboboxSelected>>', self.on_module_change)
        
        # Control buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X)
        
        self.start_btn = ttk.Button(button_frame, text="Start System", command=self.start_system)
        self.start_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_btn = ttk.Button(button_frame, text="Stop System", command=self.stop_system, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.capture_btn = ttk.Button(button_frame, text="Capture Image", command=self.capture_image)
        self.capture_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.report_btn = ttk.Button(button_frame, text="Generate Report", command=self.generate_report)
        self.report_btn.pack(side=tk.LEFT)
        
        # Main content area
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Video display
        video_frame = ttk.LabelFrame(content_frame, text="Live Feed", padding=5)
        video_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.video_label = tk.Label(video_frame, bg='black', width=60, height=30)
        self.video_label.pack()
        
        # Analytics panel
        analytics_frame = ttk.LabelFrame(content_frame, text="Analytics", padding=5)
        analytics_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Detection stats
        stats_frame = ttk.LabelFrame(analytics_frame, text="Detection Statistics", padding=5)
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.stats_text = tk.Text(stats_frame, height=8, width=30, font=('Consolas', 9))
        self.stats_text.pack()
        
        # Alerts panel
        alerts_frame = ttk.LabelFrame(analytics_frame, text="System Alerts", padding=5)
        alerts_frame.pack(fill=tk.BOTH, expand=True)
        
        self.alerts_text = tk.Text(alerts_frame, height=10, width=30, font=('Consolas', 9))
        self.alerts_text.pack()
        
        # Status bar
        self.status_var = tk.StringVar(value="System Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X, pady=(10, 0))
        
    def setup_camera(self):
        """Initialize camera"""
        try:
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                self.camera = cv2.VideoCapture(1)
            self.status_var.set("Camera initialized")
        except Exception as e:
            self.status_var.set(f"Camera error: {str(e)}")
            
    def start_system(self):
        """Start the mining CV system"""
        if self.camera is None:
            messagebox.showerror("Error", "Camera not available")
            return
            
        self.is_running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status_var.set("System Running")
        
        # Start processing thread
        self.processing_thread = threading.Thread(target=self.process_frames)
        self.processing_thread.daemon = True
        self.processing_thread.start()
        
    def stop_system(self):
        """Stop the mining CV system"""
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_var.set("System Stopped")
        
    def process_frames(self):
        """Main processing loop"""
        while self.is_running:
            ret, frame = self.camera.read()
            if not ret:
                continue
                
            # Process based on current module
            processed_frame = self.process_frame(frame)
            
            # Display frame
            self.display_frame(processed_frame)
            
            # Update analytics
            self.update_analytics()
            
            time.sleep(0.03)  # ~30 FPS
            
    def process_frame(self, frame):
        """Process frame based on current module"""
        if self.current_module == "ore_detection":
            return self.detect_ore(frame)
        elif self.current_module == "safety_monitoring":
            return self.monitor_safety(frame)
        elif self.current_module == "equipment_monitoring":
            return self.monitor_equipment(frame)
        elif self.current_module == "environmental_monitoring":
            return self.monitor_environment(frame)
        else:
            return frame
            
    def detect_ore(self, frame):
        """Detect and classify ore in the frame"""
        # Convert to HSV for better color detection
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Create mask for each ore type
        for ore_type, params in self.ore_types.items():
            lower = np.array(params['color_range'][0])
            upper = np.array(params['color_range'][1])
            mask = cv2.inRange(hsv, lower, upper)
            
            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 500:  # Minimum area threshold
                    # Draw bounding box
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    
                    # Add label
                    label = f"{ore_type.title()} (${params['value']})"
                    cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    
                    # Log detection
                    detection = {
                        'timestamp': datetime.now().isoformat(),
                        'ore_type': ore_type,
                        'value': params['value'],
                        'area': area,
                        'position': (x, y, w, h)
                    }
                    self.detection_history.append(detection)
        
        return frame
        
    def monitor_safety(self, frame):
        """Monitor safety compliance (helmet detection, PPE)"""
        # Convert to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Load Haar cascade for face detection
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        for (x, y, w, h) in faces:
            # Check for helmet (simplified - look for bright colors above face)
            roi = frame[y-20:y, x:x+w] if y > 20 else None
            
            if roi is not None:
                # Simple helmet detection based on color
                helmet_detected = self.detect_helmet(roi)
                
                if helmet_detected:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(frame, "PPE Compliant", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                else:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                    cv2.putText(frame, "SAFETY VIOLATION", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    
                    # Log violation
                    violation = {
                        'timestamp': datetime.now().isoformat(),
                        'type': 'No Helmet',
                        'position': (x, y, w, h)
                    }
                    self.safety_violations.append(violation)
        
        return frame
        
    def detect_helmet(self, roi):
        """Simple helmet detection based on color analysis"""
        if roi.size == 0:
            return False
            
        # Convert to HSV
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        
        # Look for bright colors (typical helmet colors)
        bright_mask = cv2.inRange(hsv, (0, 0, 200), (180, 30, 255))
        bright_pixels = cv2.countNonZero(bright_mask)
        
        return bright_pixels > (roi.shape[0] * roi.shape[1] * 0.1)
        
    def monitor_equipment(self, frame):
        """Monitor mining equipment status"""
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Edge detection for equipment
        edges = cv2.Canny(gray, 50, 150)
        
        # Find contours that might be equipment
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 1000:  # Large objects
                x, y, w, h = cv2.boundingRect(contour)
                
                # Check for equipment health (simplified)
                equipment_health = self.assess_equipment_health(frame[y:y+h, x:x+w])
                
                if equipment_health == "Good":
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(frame, "Equipment OK", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                else:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                    cv2.putText(frame, f"Alert: {equipment_health}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    
                    # Log equipment alert
                    alert = {
                        'timestamp': datetime.now().isoformat(),
                        'type': equipment_health,
                        'position': (x, y, w, h)
                    }
                    self.equipment_alerts.append(alert)
        
        return frame
        
    def assess_equipment_health(self, roi):
        """Assess equipment health based on visual analysis"""
        if roi.size == 0:
            return "Unknown"
            
        # Convert to HSV
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        
        # Check for rust (reddish colors)
        rust_mask = cv2.inRange(hsv, (0, 50, 50), (20, 255, 255))
        rust_pixels = cv2.countNonZero(rust_mask)
        
        # Check for oil leaks (dark colors)
        oil_mask = cv2.inRange(hsv, (0, 0, 0), (180, 255, 50))
        oil_pixels = cv2.countNonZero(oil_mask)
        
        total_pixels = roi.shape[0] * roi.shape[1]
        
        if rust_pixels > total_pixels * 0.1:
            return "Rust Detected"
        elif oil_pixels > total_pixels * 0.2:
            return "Oil Leak"
        else:
            return "Good"
            
    def monitor_environment(self, frame):
        """Monitor environmental conditions"""
        # Convert to different color spaces for analysis
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Dust detection (grayish particles)
        dust_mask = cv2.inRange(hsv, (0, 0, 100), (180, 30, 200))
        dust_level = cv2.countNonZero(dust_mask)
        
        # Gas detection (color changes)
        gas_detected = self.detect_gas(frame)
        
        # Display environmental info
        info_y = 30
        cv2.putText(frame, f"Dust Level: {dust_level}", (10, info_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        if gas_detected:
            cv2.putText(frame, "GAS DETECTED!", (10, info_y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            # Log environmental alert
            env_alert = {
                'timestamp': datetime.now().isoformat(),
                'type': 'Gas Detected',
                'dust_level': dust_level
            }
            self.environmental_data.append(env_alert)
        
        return frame
        
    def detect_gas(self, frame):
        """Detect gas presence (simplified)"""
        # Convert to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Look for color distortions that might indicate gas
        # This is a simplified detection - real gas detection would need specialized sensors
        mean_color = np.mean(hsv, axis=(0, 1))
        
        # Check for unusual color shifts
        if mean_color[0] > 100 or mean_color[1] < 50:  # Unusual hue or low saturation
            return True
        return False
        
    def display_frame(self, frame):
        """Display frame in the GUI"""
        # Resize frame to fit display
        height, width = frame.shape[:2]
        max_width, max_height = 600, 400
        
        if width > max_width or height > max_height:
            scale = min(max_width/width, max_height/height)
            new_width = int(width * scale)
            new_height = int(height * scale)
            frame = cv2.resize(frame, (new_width, new_height))
        
        # Convert to RGB for tkinter
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_pil = Image.fromarray(frame_rgb)
        frame_tk = ImageTk.PhotoImage(frame_pil)
        
        self.video_label.configure(image=frame_tk)
        self.video_label.image = frame_tk
        
    def update_analytics(self):
        """Update analytics display"""
        # Update stats
        stats_text = f"Detection Statistics:\n"
        stats_text += f"Total Detections: {len(self.detection_history)}\n"
        stats_text += f"Safety Violations: {len(self.safety_violations)}\n"
        stats_text += f"Equipment Alerts: {len(self.equipment_alerts)}\n"
        stats_text += f"Environmental Alerts: {len(self.environmental_data)}\n\n"
        
        if self.detection_history:
            recent_detections = list(self.detection_history)[-5:]
            stats_text += "Recent Detections:\n"
            for detection in recent_detections:
                stats_text += f"- {detection['ore_type']} (${detection['value']})\n"
        
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, stats_text)
        
        # Update alerts
        alerts_text = "System Alerts:\n"
        if self.safety_violations:
            alerts_text += f"SAFETY: {len(self.safety_violations)} violations\n"
        if self.equipment_alerts:
            alerts_text += f"EQUIPMENT: {len(self.equipment_alerts)} alerts\n"
        if self.environmental_data:
            alerts_text += f"ENVIRONMENT: {len(self.environmental_data)} alerts\n"
        
        if not any([self.safety_violations, self.equipment_alerts, self.environmental_data]):
            alerts_text += "All systems normal"
        
        self.alerts_text.delete(1.0, tk.END)
        self.alerts_text.insert(1.0, alerts_text)
        
    def on_module_change(self, event):
        """Handle module change"""
        self.current_module = self.module_var.get()
        self.status_var.set(f"Switched to {self.current_module.replace('_', ' ').title()}")
        
    def capture_image(self):
        """Capture current frame"""
        if self.camera is not None:
            ret, frame = self.camera.read()
            if ret:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"mining_capture_{timestamp}.jpg"
                cv2.imwrite(filename, frame)
                self.status_var.set(f"Image saved: {filename}")
                
    def generate_report(self):
        """Generate mining operations report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_detections': len(self.detection_history),
            'safety_violations': len(self.safety_violations),
            'equipment_alerts': len(self.equipment_alerts),
            'environmental_alerts': len(self.environmental_data),
            'ore_value_estimate': sum(d['value'] for d in self.detection_history),
            'detections': list(self.detection_history),
            'violations': self.safety_violations,
            'equipment_alerts': self.equipment_alerts,
            'environmental_data': self.environmental_data
        }
        
        filename = f"mining_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
            
        self.status_var.set(f"Report generated: {filename}")
        
    def run(self):
        """Run the application"""
        self.root.mainloop()
        
    def __del__(self):
        """Cleanup"""
        if self.camera is not None:
            self.camera.release()

if __name__ == "__main__":
    # Import required modules
    try:
        from PIL import Image, ImageTk
        PIL_AVAILABLE = True
    except ImportError:
        PIL_AVAILABLE = False
        print("PIL/Pillow not available. Some features may not work.")
    
    if PIL_AVAILABLE:
        app = MiningCVSystem()
        app.run()
    else:
        print("Missing dependency: PIL/Pillow")
        print("Please install required packages:")
        print("pip install opencv-python numpy pillow scikit-learn matplotlib")
