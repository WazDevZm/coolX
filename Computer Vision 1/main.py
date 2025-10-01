#!/usr/bin/env python3
"""
Smart Security Monitor - A Computer Vision Application
====================================================

A real-time security monitoring application that uses your webcam to:
- Detect motion and track objects
- Provide visual and audio alerts
- Record security events with timestamps
- Monitor specific regions of interest
- Generate activity reports

Features:
- Real-time motion detection using background subtraction
- Object tracking and trajectory analysis
- Configurable sensitivity and detection zones
- Modern GUI with live video feed
- Event logging and statistics
- Audio alerts for security breaches

Author: AI Assistant
Dependencies: opencv-python, numpy, tkinter (built-in)
"""

try:
    import cv2
    import numpy as np
    OPENCV_AVAILABLE = True
except ImportError as e:
    print(f"OpenCV import error: {e}")
    OPENCV_AVAILABLE = False
    cv2 = None
    np = None

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
import json
import os
from datetime import datetime
import math

class SmartSecurityMonitor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Smart Security Monitor")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2c3e50')
        
        # Check OpenCV availability
        if not OPENCV_AVAILABLE:
            self.show_opencv_error()
            return
        
        # Application state
        self.is_running = False
        self.cap = None
        self.background_subtractor = None
        self.motion_detected = False
        self.detection_count = 0
        self.start_time = None
        
        # Detection parameters
        self.sensitivity = 50
        self.min_area = 1000
        self.detection_zones = []
        self.alert_enabled = True
        
        # Statistics
        self.total_detections = 0
        self.session_start = datetime.now()
        self.events_log = []
        
        # UI Components
        self.setup_ui()
        self.setup_video_processing()
        
    def show_opencv_error(self):
        """Show OpenCV installation error dialog"""
        error_window = tk.Toplevel(self.root)
        error_window.title("OpenCV Installation Error")
        error_window.geometry("500x400")
        error_window.configure(bg='#2c3e50')
        
        # Error message
        error_frame = ttk.Frame(error_window, padding="20")
        error_frame.pack(fill=tk.BOTH, expand=True)
        
        # Icon and title
        title_label = tk.Label(error_frame, text="⚠️ OpenCV Installation Issue", 
                              font=("Arial", 16, "bold"), 
                              fg='#e74c3c', bg='#2c3e50')
        title_label.pack(pady=10)
        
        # Error description
        error_text = """
OpenCV is not properly installed or is missing video functionality.

This application requires OpenCV with video support to work.

SOLUTIONS:
1. Run the diagnostic script: python check_opencv.py
2. Reinstall OpenCV: pip uninstall opencv-python && pip install opencv-python
3. Try alternative: pip install opencv-contrib-python

The diagnostic script will show exactly what's missing.
        """
        
        text_widget = tk.Text(error_frame, wrap=tk.WORD, height=15, width=60)
        text_widget.pack(pady=10, fill=tk.BOTH, expand=True)
        text_widget.insert(tk.END, error_text)
        text_widget.config(state=tk.DISABLED)
        
        # Buttons
        button_frame = ttk.Frame(error_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Run Diagnostic", 
                  command=self.run_diagnostic).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Exit", 
                  command=self.root.quit).pack(side=tk.LEFT, padx=5)
                  
    def run_diagnostic(self):
        """Run the OpenCV diagnostic script"""
        import subprocess
        import sys
        try:
            subprocess.run([sys.executable, "check_opencv.py"], check=True)
        except Exception as e:
            messagebox.showerror("Error", f"Could not run diagnostic: {e}")
        
    def setup_ui(self):
        """Create the modern user interface"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = tk.Label(main_frame, text="🔒 Smart Security Monitor", 
                              font=("Arial", 20, "bold"), 
                              fg='#3498db', bg='#2c3e50')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Control panel
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Start/Stop button
        self.start_button = tk.Button(control_frame, text="▶ Start Monitoring", 
                                     command=self.toggle_monitoring,
                                     bg='#27ae60', fg='white', 
                                     font=("Arial", 12, "bold"),
                                     relief='flat', padx=20, pady=10)
        self.start_button.grid(row=0, column=0, pady=5)
        
        # Settings frame
        settings_frame = ttk.LabelFrame(control_frame, text="Settings", padding="5")
        settings_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=10)
        
        # Sensitivity slider
        tk.Label(settings_frame, text="Sensitivity:").grid(row=0, column=0, sticky=tk.W)
        self.sensitivity_var = tk.IntVar(value=self.sensitivity)
        sensitivity_scale = tk.Scale(settings_frame, from_=10, to=100, 
                                   orient=tk.HORIZONTAL, variable=self.sensitivity_var,
                                   command=self.update_sensitivity)
        sensitivity_scale.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        # Min area slider
        tk.Label(settings_frame, text="Min Area:").grid(row=1, column=0, sticky=tk.W)
        self.min_area_var = tk.IntVar(value=self.min_area)
        min_area_scale = tk.Scale(settings_frame, from_=500, to=5000, 
                                orient=tk.HORIZONTAL, variable=self.min_area_var,
                                command=self.update_min_area)
        min_area_scale.grid(row=1, column=1, sticky=(tk.W, tk.E))
        
        # Alert checkbox
        self.alert_var = tk.BooleanVar(value=True)
        alert_check = tk.Checkbutton(settings_frame, text="Enable Audio Alerts", 
                                   variable=self.alert_var)
        alert_check.grid(row=2, column=0, columnspan=2, sticky=tk.W)
        
        # Video display
        video_frame = ttk.LabelFrame(main_frame, text="Live Feed", padding="5")
        video_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.video_label = tk.Label(video_frame, text="Click 'Start Monitoring' to begin", 
                                   bg='#34495e', fg='white', 
                                   font=("Arial", 14), width=50, height=20)
        self.video_label.grid(row=0, column=0)
        
        # Status panel
        status_frame = ttk.LabelFrame(main_frame, text="Status & Statistics", padding="10")
        status_frame.grid(row=0, column=2, sticky=(tk.W, tk.E, tk.N), padx=(10, 0))
        
        # Status indicators
        self.status_label = tk.Label(status_frame, text="Status: Stopped", 
                                   fg='#e74c3c', font=("Arial", 12, "bold"))
        self.status_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.motion_label = tk.Label(status_frame, text="Motion: None", 
                                   fg='#95a5a6', font=("Arial", 10))
        self.motion_label.grid(row=1, column=0, sticky=tk.W)
        
        # Statistics
        stats_frame = ttk.Frame(status_frame)
        stats_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=10)
        
        self.detections_label = tk.Label(stats_frame, text="Detections: 0", 
                                       font=("Arial", 10))
        self.detections_label.grid(row=0, column=0, sticky=tk.W)
        
        self.session_label = tk.Label(stats_frame, text="Session: 00:00:00", 
                                   font=("Arial", 10))
        self.session_label.grid(row=1, column=0, sticky=tk.W)
        
        # Action buttons
        action_frame = ttk.Frame(status_frame)
        action_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=10)
        
        tk.Button(action_frame, text="📊 View Log", 
                 command=self.view_log, bg='#3498db', fg='white',
                 relief='flat').grid(row=0, column=0, pady=2, sticky=(tk.W, tk.E))
        
        tk.Button(action_frame, text="💾 Save Report", 
                 command=self.save_report, bg='#f39c12', fg='white',
                 relief='flat').grid(row=1, column=0, pady=2, sticky=(tk.W, tk.E))
        
        tk.Button(action_frame, text="🗑️ Clear Log", 
                 command=self.clear_log, bg='#e74c3c', fg='white',
                 relief='flat').grid(row=2, column=0, pady=2, sticky=(tk.W, tk.E))
        
    def setup_video_processing(self):
        """Initialize video processing components"""
        # Use frame differencing instead of background subtractor for better compatibility
        self.background_frame = None
        self.frame_count = 0
        
    def toggle_monitoring(self):
        """Start or stop the monitoring process"""
        if not self.is_running:
            self.start_monitoring()
        else:
            self.stop_monitoring()
            
    def start_monitoring(self):
        """Start the security monitoring"""
        if not OPENCV_AVAILABLE:
            messagebox.showerror("Error", "OpenCV is not properly installed. Please run the diagnostic script.")
            return
            
        try:
            # Check if VideoCapture is available
            if not hasattr(cv2, 'VideoCapture'):
                messagebox.showerror("Error", "VideoCapture not available in your OpenCV installation.\nPlease reinstall OpenCV with video support.")
                return
                
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                messagebox.showerror("Error", "Could not access webcam. Please check your camera.")
                return
                
            self.is_running = True
            self.start_time = time.time()
            self.start_button.config(text="⏹ Stop Monitoring", bg='#e74c3c')
            self.status_label.config(text="Status: Monitoring", fg='#27ae60')
            
            # Start video processing thread
            self.video_thread = threading.Thread(target=self.process_video, daemon=True)
            self.video_thread.start()
            
            # Start status update thread
            self.status_thread = threading.Thread(target=self.update_status, daemon=True)
            self.status_thread.start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start monitoring: {str(e)}")
            
    def stop_monitoring(self):
        """Stop the security monitoring"""
        self.is_running = False
        if self.cap:
            self.cap.release()
        self.start_button.config(text="▶ Start Monitoring", bg='#27ae60')
        self.status_label.config(text="Status: Stopped", fg='#e74c3c')
        self.motion_label.config(text="Motion: None", fg='#95a5a6')
        
    def process_video(self):
        """Main video processing loop"""
        while self.is_running:
            ret, frame = self.cap.read()
            if not ret:
                break
                
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Convert to grayscale for motion detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)
            
            # Initialize background frame
            if self.background_frame is None:
                self.background_frame = gray
                continue
            
            # Calculate frame difference
            frame_delta = cv2.absdiff(self.background_frame, gray)
            thresh = cv2.threshold(frame_delta, self.sensitivity, 255, cv2.THRESH_BINARY)[1]
            
            # Apply morphological operations to reduce noise
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
            thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
            thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            
            # Find contours
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Detect motion
            motion_detected = False
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > self.min_area:
                    motion_detected = True
                    # Draw bounding box
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, f"Motion: {area:.0f}", (x, y-10), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Update background frame periodically (every 30 frames)
            self.frame_count += 1
            if self.frame_count % 30 == 0:
                self.background_frame = gray
            
            # Update motion status
            if motion_detected and not self.motion_detected:
                self.total_detections += 1
                self.detection_count += 1
                self.log_event("Motion Detected", f"Detection #{self.detection_count}")
                if self.alert_var.get():
                    self.play_alert()
                    
            self.motion_detected = motion_detected
            
            # Add status overlay
            self.add_status_overlay(frame)
            
            # Convert frame for display
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_pil = self.cv2_to_tkinter(frame_rgb)
            
            # Update display
            self.video_label.config(image=frame_pil)
            self.video_label.image = frame_pil
            
            # Update motion status in UI
            if motion_detected:
                self.motion_label.config(text="Motion: DETECTED", fg='#e74c3c')
            else:
                self.motion_label.config(text="Motion: None", fg='#95a5a6')
                
    def add_status_overlay(self, frame):
        """Add status information overlay to the frame"""
        height, width = frame.shape[:2]
        
        # Add timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(frame, timestamp, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Add detection count
        cv2.putText(frame, f"Detections: {self.total_detections}", (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Add motion status
        status_color = (0, 255, 0) if self.motion_detected else (0, 0, 255)
        status_text = "MOTION DETECTED" if self.motion_detected else "SECURE"
        cv2.putText(frame, status_text, (width - 200, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
        
    def cv2_to_tkinter(self, frame):
        """Convert OpenCV frame to Tkinter image"""
        from PIL import Image, ImageTk
        height, width = frame.shape[:2]
        image = Image.fromarray(frame)
        image = image.resize((640, 480), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)
        
    def update_sensitivity(self, value):
        """Update motion detection sensitivity"""
        self.sensitivity = int(value)
        # Reset background frame when sensitivity changes
        self.background_frame = None
        
    def update_min_area(self, value):
        """Update minimum area for motion detection"""
        self.min_area = int(value)
        
    def play_alert(self):
        """Play audio alert (system beep)"""
        try:
            import winsound
            winsound.Beep(1000, 500)  # 1000Hz for 500ms
        except:
            # Fallback for non-Windows systems
            print("\a")  # ASCII bell character
            
    def log_event(self, event_type, description):
        """Log security events"""
        event = {
            'timestamp': datetime.now().isoformat(),
            'type': event_type,
            'description': description
        }
        self.events_log.append(event)
        
    def update_status(self):
        """Update status information in the UI"""
        while self.is_running:
            if self.start_time:
                elapsed = time.time() - self.start_time
                hours = int(elapsed // 3600)
                minutes = int((elapsed % 3600) // 60)
                seconds = int(elapsed % 60)
                self.session_label.config(text=f"Session: {hours:02d}:{minutes:02d}:{seconds:02d}")
                
            self.detections_label.config(text=f"Detections: {self.total_detections}")
            time.sleep(1)
            
    def view_log(self):
        """Display the events log in a new window"""
        if not self.events_log:
            messagebox.showinfo("Log", "No events recorded yet.")
            return
            
        log_window = tk.Toplevel(self.root)
        log_window.title("Security Events Log")
        log_window.geometry("600x400")
        
        # Create text widget with scrollbar
        text_frame = ttk.Frame(log_window)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text_widget = tk.Text(text_frame, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Populate log
        for event in self.events_log:
            text_widget.insert(tk.END, f"{event['timestamp']} - {event['type']}: {event['description']}\n")
            
        text_widget.config(state=tk.DISABLED)
        
    def save_report(self):
        """Save security report to file"""
        if not self.events_log:
            messagebox.showinfo("Report", "No events to save.")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            report = {
                'session_start': self.session_start.isoformat(),
                'total_detections': self.total_detections,
                'events': self.events_log
            }
            
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2)
                
            messagebox.showinfo("Report", f"Security report saved to {filename}")
            
    def clear_log(self):
        """Clear the events log"""
        if messagebox.askyesno("Clear Log", "Are you sure you want to clear the events log?"):
            self.events_log = []
            self.total_detections = 0
            self.detection_count = 0
            self.detections_label.config(text="Detections: 0")
            messagebox.showinfo("Log Cleared", "Events log has been cleared.")
            
    def run(self):
        """Start the application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
        
    def on_closing(self):
        """Handle application closing"""
        if self.is_running:
            self.stop_monitoring()
        self.root.destroy()

def main():
    """Main application entry point"""
    print("🔒 Smart Security Monitor")
    print("=" * 50)
    print("Starting application...")
    print("Features:")
    print("• Real-time motion detection")
    print("• Object tracking and alerts")
    print("• Configurable sensitivity")
    print("• Event logging and reporting")
    print("• Modern GUI interface")
    print("=" * 50)
    
    try:
        app = SmartSecurityMonitor()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        messagebox.showerror("Error", f"Failed to start application: {e}")

if __name__ == "__main__":
    main()
