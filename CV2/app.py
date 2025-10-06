#!/usr/bin/env python3
import cv2
import mediapipe as mp
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import threading
import time
import pyautogui
from collections import deque

class HandGestureApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🤖 AI Hand Gesture Recognition")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1a1a1a')

        # MediaPipe
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )

        # Camera
        self.cap = None
        self.is_running = False

        # Gesture
        self.gesture_label = tk.StringVar(value="No gesture detected")
        self.confidence_label = tk.StringVar(value="Confidence: 0%")
        self.fps_label = tk.StringVar(value="FPS: 0")
        self.mouse_mode = False
        self.screen_width, self.screen_height = pyautogui.size()

        self.fps_counter = 0
        self.fps_start_time = time.time()
        self.last_gesture_time = 0
        self.gesture_cooldown = 1.0

        self.setup_ui()
        self.setup_styles()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#00ff88', background='#1a1a1a')
        style.configure('Info.TLabel', font=('Arial', 12), foreground='#ffffff', background='#1a1a1a')
        style.configure('Status.TLabel', font=('Arial', 10), foreground='#ffaa00', background='#1a1a1a')
        style.configure('Modern.TButton', font=('Arial', 11, 'bold'), padding=(10, 5))
        style.map('Modern.TButton', background=[('active', '#00ff88'), ('pressed', '#00cc66')])

    def setup_ui(self):
        # Left panel - Camera
        left_panel = tk.Frame(self.root, bg='#2a2a2a', relief='raised', bd=2)
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        self.video_label = tk.Label(left_panel, bg='#000000')
        self.video_label.pack(expand=True, fill='both')

        # Right panel - Controls
        right_panel = tk.Frame(self.root, bg='#2a2a2a', relief='raised', bd=2)
        right_panel.pack(side='right', fill='y', padx=(10,0))
        right_panel.configure(width=300)

        self.start_btn = ttk.Button(right_panel, text="🚀 Start Camera", command=self.start_camera, style='Modern.TButton')
        self.start_btn.pack(fill='x', pady=5)
        self.stop_btn = ttk.Button(right_panel, text="⏹️ Stop Camera", command=self.stop_camera, style='Modern.TButton', state='disabled')
        self.stop_btn.pack(fill='x', pady=5)

        ttk.Label(right_panel, text="🎯 Current Gesture:", style='Info.TLabel').pack(anchor='w', pady=(20,0))
        ttk.Label(right_panel, textvariable=self.gesture_label, style='Status.TLabel').pack(anchor='w', pady=5)

        ttk.Label(right_panel, text="📊 Confidence:", style='Info.TLabel').pack(anchor='w', pady=(10,0))
        ttk.Label(right_panel, textvariable=self.confidence_label, style='Status.TLabel').pack(anchor='w', pady=5)

        ttk.Label(right_panel, text="⚡ FPS:", style='Info.TLabel').pack(anchor='w', pady=(10,0))
        ttk.Label(right_panel, textvariable=self.fps_label, style='Status.TLabel').pack(anchor='w', pady=5)

        self.mouse_mode_var = tk.BooleanVar()
        ttk.Checkbutton(right_panel, text="🖱️ Virtual Mouse Control", variable=self.mouse_mode_var, command=self.toggle_mouse_mode).pack(anchor='w', pady=10)

    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Could not open camera!")
            return
        self.is_running = True
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        threading.Thread(target=self.camera_loop, daemon=True).start()

    def stop_camera(self):
        self.is_running = False
        if self.cap:
            self.cap.release()
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.gesture_label.set("No gesture detected")
        self.confidence_label.set("Confidence: 0%")

    def toggle_mouse_mode(self):
        self.mouse_mode = self.mouse_mode_var.get()
        if self.mouse_mode:
            messagebox.showinfo("Mouse Mode", "Virtual mouse control enabled!")

    def camera_loop(self):
        while self.is_running:
            ret, frame = self.cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            self.process_frame(frame)
            self.update_video_display(frame)
            self.update_fps()

    def process_frame(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                gesture, confidence = self.detect_gesture(hand_landmarks)
                if gesture != "Unknown" and time.time() - self.last_gesture_time > self.gesture_cooldown:
                    self.gesture_label.set(gesture)
                    self.confidence_label.set(f"{confidence:.1f}%")
                    self.last_gesture_time = time.time()
                    self.handle_gesture_action(gesture, hand_landmarks)

    def detect_gesture(self, landmarks):
        points = np.array([[lm.x, lm.y, lm.z] for lm in landmarks.landmark])
        finger_states = self.get_finger_states(points)
        gesture, confidence = self.classify_gesture(finger_states)
        return gesture, confidence

    def get_finger_states(self, points):
        tip_ids = [4,8,12,16,20]
        finger_states = []
        finger_states.append(points[4][1] < points[3][1]) # thumb
        for i in range(1,5):
            finger_states.append(points[tip_ids[i]][1] < points[tip_ids[i]-2][1])
        return finger_states

    def classify_gesture(self, finger_states):
        thumb, index, middle, ring, pinky = finger_states
        if all(finger_states):
            return "Open Hand", 90.0
        elif not any(finger_states):
            return "Fist", 85.0
        elif index and middle and not ring and not pinky and not thumb:
            return "Peace Sign", 88.0
        elif thumb and not index and not middle and not ring and not pinky:
            return "Thumbs Up", 92.0
        elif index and not middle and not ring and not pinky and not thumb:
            return "Point", 87.0
        else:
            return "Unknown", 0.0

    def handle_gesture_action(self, gesture, landmarks):
        if not self.mouse_mode: return
        if gesture == "Point":
            index_tip = landmarks.landmark[8]
            x, y = int(index_tip.x*self.screen_width), int(index_tip.y*self.screen_height)
            pyautogui.moveTo(x, y, duration=0.1)

    def update_video_display(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        img = img.resize((640,480))
        imgtk = ImageTk.PhotoImage(image=img)
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)

    def update_fps(self):
        self.fps_counter += 1
        current_time = time.time()
        if current_time - self.fps_start_time >= 1.0:
            fps = self.fps_counter / (current_time - self.fps_start_time)
            self.fps_label.set(f"{fps:.1f}")
            self.fps_counter = 0
            self.fps_start_time = current_time

    def run(self):
        self.root.mainloop()
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = HandGestureApp()
    app.run()
