#!/usr/bin/env python3
"""
Mining CV System Demo
====================

A demonstration script that shows the capabilities of the Mining Computer Vision System
without requiring a live camera feed. Uses sample images and simulated data.
"""

import cv2
import numpy as np
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
from main import MiningCVSystem
import config
import utils

class MiningCVDemo:
    def __init__(self):
        self.demo_data = self.create_demo_data()
        self.sample_images = self.create_sample_images()
        
    def create_demo_data(self):
        """Create sample detection data for demonstration"""
        return {
            'ore_detections': [
                {'type': 'gold', 'value': 500, 'area': 1200, 'position': (100, 150, 50, 60)},
                {'type': 'copper', 'value': 150, 'area': 800, 'position': (200, 300, 40, 45)},
                {'type': 'iron', 'value': 100, 'area': 1500, 'position': (350, 200, 60, 70)},
                {'type': 'silver', 'value': 200, 'area': 600, 'position': (450, 100, 30, 35)}
            ],
            'safety_violations': [
                {'type': 'No Helmet', 'position': (150, 200, 80, 100)},
                {'type': 'No PPE', 'position': (300, 250, 70, 90)}
            ],
            'equipment_alerts': [
                {'type': 'Rust Detected', 'position': (400, 300, 120, 80)},
                {'type': 'Oil Leak', 'position': (100, 400, 90, 60)}
            ],
            'environmental_alerts': [
                {'type': 'High Dust', 'level': 150},
                {'type': 'Gas Detected', 'level': 200}
            ]
        }
    
    def create_sample_images(self):
        """Create sample images for demonstration"""
        images = {}
        
        # Create ore detection sample
        ore_img = np.zeros((480, 640, 3), dtype=np.uint8)
        ore_img[:] = (50, 50, 50)  # Dark background
        
        # Add different colored "ore" patches
        cv2.rectangle(ore_img, (100, 150), (150, 210), (0, 255, 255), -1)  # Gold
        cv2.rectangle(ore_img, (200, 300), (240, 345), (0, 255, 255), -1)  # Copper
        cv2.rectangle(ore_img, (350, 200), (410, 270), (0, 255, 0), -1)   # Iron
        cv2.rectangle(ore_img, (450, 100), (480, 135), (255, 255, 255), -1)  # Silver
        
        images['ore_detection'] = ore_img
        
        # Create safety monitoring sample
        safety_img = np.zeros((480, 640, 3), dtype=np.uint8)
        safety_img[:] = (30, 30, 30)  # Dark background
        
        # Add person without helmet
        cv2.ellipse(safety_img, (200, 200), (40, 50), 0, 0, 360, (200, 200, 200), -1)  # Head
        cv2.rectangle(safety_img, (150, 250), (250, 400), (100, 100, 100), -1)  # Body
        
        # Add person with helmet
        cv2.ellipse(safety_img, (400, 200), (40, 50), 0, 0, 360, (200, 200, 200), -1)  # Head
        cv2.ellipse(safety_img, (400, 180), (45, 30), 0, 0, 360, (0, 0, 255), -1)  # Helmet
        cv2.rectangle(safety_img, (350, 250), (450, 400), (100, 100, 100), -1)  # Body
        
        images['safety_monitoring'] = safety_img
        
        # Create equipment monitoring sample
        equipment_img = np.zeros((480, 640, 3), dtype=np.uint8)
        equipment_img[:] = (40, 40, 40)  # Dark background
        
        # Add equipment with rust
        cv2.rectangle(equipment_img, (100, 200), (300, 350), (0, 100, 200), -1)  # Equipment
        cv2.rectangle(equipment_img, (120, 220), (280, 330), (0, 0, 255), -1)  # Rust patches
        
        # Add equipment with oil leak
        cv2.rectangle(equipment_img, (400, 150), (600, 300), (0, 100, 200), -1)  # Equipment
        cv2.rectangle(equipment_img, (420, 280), (580, 300), (0, 0, 0), -1)  # Oil leak
        
        images['equipment_monitoring'] = equipment_img
        
        # Create environmental monitoring sample
        env_img = np.zeros((480, 640, 3), dtype=np.uint8)
        env_img[:] = (60, 60, 60)  # Dusty background
        
        # Add dust particles
        for _ in range(50):
            x = np.random.randint(0, 640)
            y = np.random.randint(0, 480)
            cv2.circle(env_img, (x, y), 2, (150, 150, 150), -1)
        
        # Add gas cloud
        cv2.ellipse(env_img, (400, 300), (80, 40), 0, 0, 360, (0, 255, 255), -1)
        
        images['environmental_monitoring'] = env_img
        
        return images
    
    def run_demo(self):
        """Run the complete demonstration"""
        print("Mining Computer Vision System - Demo Mode")
        print("=" * 50)
        
        # Create demo directories
        os.makedirs("demo_output", exist_ok=True)
        os.makedirs("demo_output/images", exist_ok=True)
        os.makedirs("demo_output/reports", exist_ok=True)
        
        # Process each module
        modules = ['ore_detection', 'safety_monitoring', 'equipment_monitoring', 'environmental_monitoring']
        
        for module in modules:
            print(f"\nProcessing {module.replace('_', ' ').title()} Module...")
            self.process_module(module)
        
        # Generate comprehensive report
        self.generate_demo_report()
        
        print("\nDemo completed! Check 'demo_output' directory for results.")
    
    def process_module(self, module_name):
        """Process a specific module with demo data"""
        image = self.sample_images[module_name]
        
        if module_name == 'ore_detection':
            processed_image = self.demo_ore_detection(image)
        elif module_name == 'safety_monitoring':
            processed_image = self.demo_safety_monitoring(image)
        elif module_name == 'equipment_monitoring':
            processed_image = self.demo_equipment_monitoring(image)
        elif module_name == 'environmental_monitoring':
            processed_image = self.demo_environmental_monitoring(image)
        else:
            processed_image = image
        
        # Save processed image
        output_path = f"demo_output/images/{module_name}_result.jpg"
        cv2.imwrite(output_path, processed_image)
        print(f"  - Processed image saved: {output_path}")
    
    def demo_ore_detection(self, image):
        """Demo ore detection functionality"""
        processed = image.copy()
        
        # Simulate ore detection
        for detection in self.demo_data['ore_detections']:
            x, y, w, h = detection['position']
            ore_type = detection['type']
            value = detection['value']
            
            # Draw bounding box
            cv2.rectangle(processed, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Add label
            label = f"{ore_type.title()} (${value})"
            cv2.putText(processed, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        return processed
    
    def demo_safety_monitoring(self, image):
        """Demo safety monitoring functionality"""
        processed = image.copy()
        
        # Simulate face detection and helmet checking
        for violation in self.demo_data['safety_violations']:
            x, y, w, h = violation['position']
            violation_type = violation['type']
            
            # Draw violation box
            cv2.rectangle(processed, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(processed, violation_type, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        return processed
    
    def demo_equipment_monitoring(self, image):
        """Demo equipment monitoring functionality"""
        processed = image.copy()
        
        # Simulate equipment detection
        for alert in self.demo_data['equipment_alerts']:
            x, y, w, h = alert['position']
            alert_type = alert['type']
            
            # Draw alert box
            cv2.rectangle(processed, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(processed, alert_type, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        return processed
    
    def demo_environmental_monitoring(self, image):
        """Demo environmental monitoring functionality"""
        processed = image.copy()
        
        # Add environmental information
        dust_level = 150
        gas_detected = True
        
        cv2.putText(processed, f"Dust Level: {dust_level}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        if gas_detected:
            cv2.putText(processed, "GAS DETECTED!", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        return processed
    
    def generate_demo_report(self):
        """Generate comprehensive demo report"""
        report = {
            'demo_info': {
                'timestamp': datetime.now().isoformat(),
                'system': 'Mining Computer Vision System',
                'version': '1.0.0',
                'mode': 'Demo'
            },
            'statistics': {
                'total_ore_detections': len(self.demo_data['ore_detections']),
                'safety_violations': len(self.demo_data['safety_violations']),
                'equipment_alerts': len(self.demo_data['equipment_alerts']),
                'environmental_alerts': len(self.demo_data['environmental_alerts']),
                'total_ore_value': sum(d['value'] for d in self.demo_data['ore_detections'])
            },
            'ore_detections': self.demo_data['ore_detections'],
            'safety_violations': self.demo_data['safety_violations'],
            'equipment_alerts': self.demo_data['equipment_alerts'],
            'environmental_alerts': self.demo_data['environmental_alerts'],
            'recommendations': [
                "Implement regular safety training sessions",
                "Schedule equipment maintenance for rust-affected machinery",
                "Install dust suppression systems",
                "Deploy gas detection sensors in high-risk areas",
                "Establish PPE compliance monitoring protocols"
            ]
        }
        
        # Save report
        report_path = "demo_output/reports/demo_report.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"  - Demo report generated: {report_path}")
        
        # Create summary
        self.create_demo_summary(report)
    
    def create_demo_summary(self, report):
        """Create a visual summary of the demo"""
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle('Mining CV System - Demo Results', fontsize=16)
        
        # Ore detection summary
        ore_types = [d['type'] for d in self.demo_data['ore_detections']]
        ore_values = [d['value'] for d in self.demo_data['ore_detections']]
        
        axes[0, 0].bar(ore_types, ore_values, color=['gold', 'orange', 'gray', 'silver'])
        axes[0, 0].set_title('Ore Detection Results')
        axes[0, 0].set_ylabel('Value ($)')
        
        # Safety violations
        violation_types = [v['type'] for v in self.demo_data['safety_violations']]
        axes[0, 1].pie([1] * len(violation_types), labels=violation_types, autopct='%1.0f%%')
        axes[0, 1].set_title('Safety Violations')
        
        # Equipment alerts
        alert_types = [a['type'] for a in self.demo_data['equipment_alerts']]
        axes[1, 0].bar(alert_types, [1] * len(alert_types), color=['red', 'orange'])
        axes[1, 0].set_title('Equipment Alerts')
        axes[1, 0].set_ylabel('Count')
        
        # Environmental monitoring
        env_data = ['Dust Level', 'Gas Detection']
        env_values = [150, 1]
        axes[1, 1].bar(env_data, env_values, color=['brown', 'red'])
        axes[1, 1].set_title('Environmental Monitoring')
        axes[1, 1].set_ylabel('Level')
        
        plt.tight_layout()
        plt.savefig('demo_output/reports/demo_summary.png', dpi=300, bbox_inches='tight')
        print("  - Visual summary created: demo_output/reports/demo_summary.png")

if __name__ == "__main__":
    demo = MiningCVDemo()
    demo.run_demo()
