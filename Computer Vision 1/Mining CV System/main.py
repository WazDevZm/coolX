#!/usr/bin/env python3
"""
Mining Computer Vision System (fixed)
- Uses Tkinter for UI and OpenCV for video processing
- Runs frame capture on the main thread via tkinter's after() (safe)
Author: AI Assistant (fixed)
"""

import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import time
import json
import os
from datetime import datetime
import math
from collections import deque
import warnings
warnings.filterwarnings('ignore')

# Import PIL early (used for converting OpenCV image -> Tk image)
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# Optional sklearn / matplotlib checks (non-fatal)
try:
    from sklearn.cluster import KMeans
    SKLEARN_AVAILABLE = True
except Exception:
    SKLEARN_AVAILABLE = False
    KMeans = None

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except Exception:
    MATPLOTLIB_AVAILABLE = False
    plt = None


class MiningCVSystem:
    def __init__(self):
        if not PIL_AVAILABLE:
            raise RuntimeError("PIL/Pillow not available. Install via: pip install pillow")

        self.root = tk.Tk()
        self.root.title("Mining Computer Vision System")
        self.root.geometry("1200x800")
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

        # Ore classification model (simplified HSV ranges)
        self.ore_types = {
            'iron':  {'color_range': [(0, 50, 50), (20, 255, 255)], 'value': 100},
            'copper':{'color_range': [(10, 100, 100), (30, 255, 255)], 'value': 150},
            'gold':  {'color_range': [(20, 100, 100), (40, 255, 255)], 'value': 500},
            'silver':{'color_range': [(0, 0, 100), (180, 30, 255)], 'value': 200}
        }

        # UI and camera setup
        self.setup_ui()
        self.setup_camera()

        # Schedule analytics updater token
        self._analytics_job = None

        # Ensure clean shutdown
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_ui(self):
        """Setup the main user interface"""
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        title_label = tk.Label(main_frame, text="Mining Computer Vision System",
                               font=('Arial', 16, 'bold'), fg='white', bg='#1a1a1a')
        title_label.pack(pady=(0, 10))

        control_frame = ttk.LabelFrame(main_frame, text="System Controls", padding=10)
        control_frame.pack(fill=tk.X, pady=(0, 10))

        module_frame = ttk.Frame(control_frame)
        module_frame.pack(fill=tk.X, pady=(0, 10))
        tk.Label(module_frame, text="Active Module:").pack(side=tk.LEFT)
        self.module_var = tk.StringVar(value="ore_detection")
        module_combo = ttk.Combobox(module_frame, textvariable=self.module_var,
                                    values=["ore_detection", "safety_monitoring",
                                            "equipment_monitoring", "environmental_monitoring"],
                                    state="readonly", width=28)
        module_combo.pack(side=tk.LEFT, padx=(10, 0))
        module_combo.bind('<<ComboboxSelected>>', self.on_module_change)

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

        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)

        video_frame = ttk.LabelFrame(content_frame, text="Live Feed", padding=5)
        video_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Video area - use a label
        self.video_label = tk.Label(video_frame, bg='black')
        self.video_label.pack(fill=tk.BOTH, expand=True)

        analytics_frame = ttk.LabelFrame(content_frame, text="Analytics", padding=5)
        analytics_frame.pack(side=tk.RIGHT, fill=tk.Y)

        stats_frame = ttk.LabelFrame(analytics_frame, text="Detection Statistics", padding=5)
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        self.stats_text = tk.Text(stats_frame, height=12, width=40, font=('Consolas', 9))
        self.stats_text.pack()

        alerts_frame = ttk.LabelFrame(analytics_frame, text="System Alerts", padding=5)
        alerts_frame.pack(fill=tk.BOTH, expand=True)
        self.alerts_text = tk.Text(alerts_frame, height=10, width=40, font=('Consolas', 9))
        self.alerts_text.pack()

        self.status_var = tk.StringVar(value="System Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X, pady=(10, 0))

    def setup_camera(self):
        """Initialize camera safely"""
        # Try common device indices
        for idx in (0, 1, 2):
            cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW) if os.name == 'nt' else cv2.VideoCapture(idx)
            if cap is not None and cap.isOpened():
                self.camera = cap
                # optional: set resolution
                self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
                self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
                self.status_var.set(f"Camera initialized (index {idx})")
                return
            else:
                if cap is not None:
                    cap.release()
        self.status_var.set("No camera found")

    def start_system(self):
        """Start the mining CV system using after() loop"""
        if self.camera is None or not self.camera.isOpened():
            messagebox.showerror("Error", "Camera not available")
            return
        if self.is_running:
            return

        self.is_running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status_var.set("System Running")
        # start frame loop (safe: runs on main thread)
        self.root.after(0, self._frame_loop)
        # schedule analytics updates
        self._analytics_job = self.root.after(1000, self.update_analytics)  # update every 1s

    def stop_system(self):
        """Stop the mining CV system"""
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_var.set("System Stopped")
        # cancel scheduled analytics if running
        if self._analytics_job:
            try:
                self.root.after_cancel(self._analytics_job)
            except Exception:
                pass
            self._analytics_job = None

    def _frame_loop(self):
        """Read one frame, process it, display it, then schedule next call"""
        if not self.is_running:
            return

        ret, frame = self.camera.read()
        if ret and frame is not None:
            try:
                processed = self.process_frame(frame)
                self.display_frame(processed)
            except Exception as e:
                # in production you'd log this
                print("Frame processing error:", e)

        # schedule next frame in ~30ms (~33 FPS)
        self.root.after(30, self._frame_loop)

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
        """Detect and classify ore in the frame (color-based)"""
        try:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        except Exception:
            return frame

        for ore_type, params in self.ore_types.items():
            lower = np.array(params['color_range'][0], dtype=np.uint8)
            upper = np.array(params['color_range'][1], dtype=np.uint8)
            mask = cv2.inRange(hsv, lower, upper)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 500:  # minimum area threshold
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    label = f"{ore_type.title()} (${params['value']})"
                    cv2.putText(frame, label, (x, max(10, y - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    detection = {
                        'timestamp': datetime.now().isoformat(),
                        'ore_type': ore_type,
                        'value': params['value'],
                        'area': area,
                        'position': (int(x), int(y), int(w), int(h))
                    }
                    self.detection_history.append(detection)
        return frame

    def monitor_safety(self, frame):
        """Monitor safety compliance (helmet detection)"""
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        except Exception:
            return frame

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            # Expand region upwards to include helmet area above face
            y1 = max(0, y - int(h * 0.6))
            y2 = y + int(h * 0.1)
            x1 = max(0, x)
            x2 = min(frame.shape[1], x + w)
            roi = frame[y1:y2, x1:x2] if (y2 > y1 and x2 > x1) else None

            helmet_detected = False
            if roi is not None and roi.size != 0:
                helmet_detected = self.detect_helmet(roi)

            if helmet_detected:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, "PPE Compliant", (x, max(10, y - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                            (0, 255, 0), 2)
            else:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(frame, "SAFETY VIOLATION", (x, max(10, y - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                            (0, 0, 255), 2)
                violation = {
                    'timestamp': datetime.now().isoformat(),
                    'type': 'No Helmet',
                    'position': (int(x), int(y), int(w), int(h))
                }
                self.safety_violations.append(violation)
        return frame

    def detect_helmet(self, roi):
        """Simple helmet detection based on bright helmet-like colors"""
        if roi is None or roi.size == 0:
            return False
        try:
            hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        except Exception:
            return False
        # Look for bright helmet colors - broad range including yellow/orange/white
        lower = np.array([0, 50, 150], dtype=np.uint8)
        upper = np.array([50, 255, 255], dtype=np.uint8)
        mask = cv2.inRange(hsv, lower, upper)
        bright_pixels = cv2.countNonZero(mask)
        return bright_pixels > (roi.shape[0] * roi.shape[1] * 0.08)  # 8% threshold

    def monitor_equipment(self, frame):
        """Monitor mining equipment (simple contour + color checks)"""
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        except Exception:
            return frame

        edges = cv2.Canny(gray, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 2000:
                x, y, w, h = cv2.boundingRect(contour)
                roi = frame[y:y + h, x:x + w]
                equipment_health = self.assess_equipment_health(roi)
                color = (0, 255, 0) if equipment_health == "Good" else (0, 0, 255)
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, f"Equipment: {equipment_health}", (x, max(10, y - 10)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                if equipment_health != "Good":
                    alert = {
                        'timestamp': datetime.now().isoformat(),
                        'type': equipment_health,
                        'position': (int(x), int(y), int(w), int(h))
                    }
                    self.equipment_alerts.append(alert)
        return frame

    def assess_equipment_health(self, roi):
        """Assess equipment health based on color heuristics"""
        if roi is None or roi.size == 0:
            return "Unknown"
        try:
            hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        except Exception:
            return "Unknown"
        # Rust: reddish hues
        rust_mask = cv2.inRange(hsv, np.array([0, 80, 50]), np.array([20, 255, 255]))
        rust_pixels = cv2.countNonZero(rust_mask)
        # Oil/dark: low brightness
        oil_mask = cv2.inRange(hsv, np.array([0, 0, 0]), np.array([180, 255, 60]))
        oil_pixels = cv2.countNonZero(oil_mask)
        total = roi.shape[0] * roi.shape[1]
        if total == 0:
            return "Unknown"
        if rust_pixels > total * 0.12:
            return "Rust Detected"
        if oil_pixels > total * 0.2:
            return "Oil Leak"
        return "Good"

    def monitor_environment(self, frame):
        """Simple environmental monitoring (dust & color shift heuristic)"""
        try:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        except Exception:
            return frame
        dust_mask = cv2.inRange(hsv, np.array([0, 0, 80]), np.array([180, 30, 200]))
        dust_level = cv2.countNonZero(dust_mask)
        gas_detected = self.detect_gas(frame)
        cv2.putText(frame, f"Dust Level: {dust_level}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        if gas_detected:
            cv2.putText(frame, "GAS DETECTED!", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            env_alert = {'timestamp': datetime.now().isoformat(), 'type': 'Gas Detected', 'dust_level': int(dust_level)}
            self.environmental_data.append(env_alert)
        return frame

    def detect_gas(self, frame):
        """Very rough mean-color heuristic for gas-like color shift"""
        if frame is None or frame.size == 0:
            return False
        try:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        except Exception:
            return False
        mean_color = np.mean(hsv, axis=(0, 1))
        # Heuristic: unusual hue (>100) or low saturation
        return (mean_color[0] > 100) or (mean_color[1] < 30)

    def display_frame(self, frame):
        """Display frame in the Tkinter label using PIL ImageTk"""
        try:
            # Resize to fit label nicely
            h, w = frame.shape[:2]
            max_w, max_h = 640, 480
            if w > max_w or h > max_h:
                scale = min(max_w / w, max_h / h)
                new_w, new_h = int(w * scale), int(h * scale)
                frame = cv2.resize(frame, (new_w, new_h))
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk  # keep reference
            self.video_label.configure(image=imgtk)
        except Exception as e:
            # On failure, set a black image
            blank = Image.new('RGB', (640, 480), (0, 0, 0))
            imgtk = ImageTk.PhotoImage(blank)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
            print("Display error:", e)

    def update_analytics(self):
        """Update analytics display every second"""
        stats_text = f"Detection Statistics:\n"
        stats_text += f"Total Detections: {len(self.detection_history)}\n"
        stats_text += f"Safety Violations: {len(self.safety_violations)}\n"
        stats_text += f"Equipment Alerts: {len(self.equipment_alerts)}\n"
        stats_text += f"Environmental Alerts: {len(self.environmental_data)}\n\n"
        if len(self.detection_history) > 0:
            recent = list(self.detection_history)[-5:]
            stats_text += "Recent Detections:\n"
            for d in recent:
                stats_text += f"- {d['ore_type']} (${d['value']})\n"
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, stats_text)

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

        # schedule next analytics update in 1s if running
        if self.is_running:
            self._analytics_job = self.root.after(1000, self.update_analytics)

    def on_module_change(self, event):
        self.current_module = self.module_var.get()
        self.status_var.set(f"Switched to {self.current_module.replace('_', ' ').title()}")

    def capture_image(self):
        """Capture current frame and save to disk"""
        if not self.camera or not self.camera.isOpened():
            self.status_var.set("Camera not available for capture")
            return
        ret, frame = self.camera.read()
        if ret and frame is not None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"mining_capture_{timestamp}.jpg"
            cv2.imwrite(filename, frame)
            self.status_var.set(f"Image saved: {filename}")
        else:
            self.status_var.set("Failed to capture image")

    def generate_report(self):
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_detections': len(self.detection_history),
            'safety_violations': len(self.safety_violations),
            'equipment_alerts': len(self.equipment_alerts),
            'environmental_alerts': len(self.environmental_data),
            'ore_value_estimate': sum(d.get('value', 0) for d in self.detection_history),
            'detections': list(self.detection_history),
            'violations': list(self.safety_violations),
            'equipment_alerts': list(self.equipment_alerts),
            'environmental_data': list(self.environmental_data)
        }
        filename = f"mining_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        self.status_var.set(f"Report generated: {filename}")

    def on_close(self):
        """Clean shutdown"""
        self.is_running = False
        if self.camera is not None:
            try:
                self.camera.release()
            except Exception:
                pass
            self.camera = None
        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    try:
        app = MiningCVSystem()
        app.run()
    except RuntimeError as e:
        print(str(e))
        print("Install missing packages: pip install pillow opencv-python numpy")
