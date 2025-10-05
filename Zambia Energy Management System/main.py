#!/usr/bin/env python3
"""
Zambia Energy Management System
==============================

A comprehensive smart energy management system designed to help solve Zambia's 
load shedding problem through intelligent monitoring, prediction, and optimization.

Features:
- Real-time power consumption monitoring
- Load shedding prediction and scheduling
- Energy optimization algorithms
- Renewable energy integration
- Smart grid management
- User notifications and alerts
- Data analytics and reporting

Author: AI Assistant
Dependencies: tkinter, numpy, pandas, matplotlib, requests, datetime
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time
import json
import os
from datetime import datetime, timedelta
import requests
import random
from collections import deque
import warnings
warnings.filterwarnings('ignore')

class ZambiaEnergySystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Zambia Energy Management System")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1a1a1a')
        
        # System state
        self.is_monitoring = False
        self.current_load = 0
        self.max_capacity = 1000  # MW
        self.renewable_share = 0.15  # 15% renewable
        
        # Load shedding data
        self.load_shedding_schedule = []
        self.consumption_history = deque(maxlen=1000)
        self.optimization_suggestions = []
        
        # Zambian power grid data (simulated)
        self.zambia_power_stations = {
            'Kafue Gorge': {'capacity': 990, 'type': 'hydro', 'status': 'operational'},
            'Kariba North': {'capacity': 1080, 'type': 'hydro', 'status': 'operational'},
            'Itezhi-Tezhi': {'capacity': 120, 'type': 'hydro', 'status': 'operational'},
            'Lusaka West': {'capacity': 300, 'type': 'thermal', 'status': 'operational'},
            'Copperbelt Energy': {'capacity': 200, 'type': 'thermal', 'status': 'operational'},
            'Solar Farms': {'capacity': 150, 'type': 'solar', 'status': 'operational'},
            'Wind Farms': {'capacity': 50, 'type': 'wind', 'status': 'operational'}
        }
        
        # Load shedding zones in Zambia
        self.load_shedding_zones = {
            'Lusaka': {'population': 3000000, 'priority': 'high'},
            'Kitwe': {'population': 500000, 'priority': 'high'},
            'Ndola': {'population': 500000, 'priority': 'high'},
            'Livingstone': {'population': 200000, 'priority': 'medium'},
            'Chipata': {'population': 150000, 'priority': 'medium'},
            'Kabwe': {'population': 200000, 'priority': 'medium'},
            'Chingola': {'population': 150000, 'priority': 'low'},
            'Mufulira': {'population': 100000, 'priority': 'low'}
        }
        
        self.setup_ui()
        self.load_historical_data()
        
    def setup_ui(self):
        """Setup the main user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(main_frame, text="🇿🇲 Zambia Energy Management System", 
                              font=('Arial', 18, 'bold'), fg='white', bg='#1a1a1a')
        title_label.pack(pady=(0, 10))
        
        # Control panel
        control_frame = ttk.LabelFrame(main_frame, text="System Controls", padding=10)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Control buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X)
        
        self.start_btn = ttk.Button(button_frame, text="Start Monitoring", command=self.start_monitoring)
        self.start_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_btn = ttk.Button(button_frame, text="Stop Monitoring", command=self.stop_monitoring, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.optimize_btn = ttk.Button(button_frame, text="Optimize Energy", command=self.optimize_energy)
        self.optimize_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.predict_btn = ttk.Button(button_frame, text="Predict Load Shedding", command=self.predict_load_shedding)
        self.predict_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.report_btn = ttk.Button(button_frame, text="Generate Report", command=self.generate_report)
        self.report_btn.pack(side=tk.LEFT)
        
        # Main content area
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Real-time monitoring
        left_panel = ttk.LabelFrame(content_frame, text="Real-time Monitoring", padding=5)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Power grid status
        grid_frame = ttk.LabelFrame(left_panel, text="Power Grid Status", padding=5)
        grid_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.grid_status_text = tk.Text(grid_frame, height=8, width=50, font=('Consolas', 9))
        self.grid_status_text.pack()
        
        # Load shedding schedule
        schedule_frame = ttk.LabelFrame(left_panel, text="Load Shedding Schedule", padding=5)
        schedule_frame.pack(fill=tk.BOTH, expand=True)
        
        self.schedule_text = tk.Text(schedule_frame, height=10, width=50, font=('Consolas', 9))
        self.schedule_text.pack()
        
        # Right panel - Analytics and charts
        right_panel = ttk.LabelFrame(content_frame, text="Analytics & Optimization", padding=5)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Energy consumption chart
        chart_frame = ttk.LabelFrame(right_panel, text="Energy Consumption", padding=5)
        chart_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, chart_frame)
        self.canvas.get_tk_widget().pack()
        
        # Optimization suggestions
        optimization_frame = ttk.LabelFrame(right_panel, text="Optimization Suggestions", padding=5)
        optimization_frame.pack(fill=tk.BOTH, expand=True)
        
        self.optimization_text = tk.Text(optimization_frame, height=12, width=40, font=('Consolas', 9))
        self.optimization_text.pack()
        
        # Status bar
        self.status_var = tk.StringVar(value="System Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X, pady=(10, 0))
        
    def load_historical_data(self):
        """Load historical energy consumption data"""
        # Simulate historical data for Zambia
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='H')
        base_consumption = 800  # MW base load
        
        # Add seasonal variations (higher in dry season)
        seasonal_factor = 1 + 0.3 * np.sin(2 * np.pi * dates.dayofyear / 365)
        
        # Add daily patterns (higher during peak hours)
        daily_factor = 1 + 0.4 * np.sin(2 * np.pi * dates.hour / 24)
        
        # Add random variations
        random_factor = np.random.normal(1, 0.1, len(dates))
        
        consumption = base_consumption * seasonal_factor * daily_factor * random_factor
        
        self.historical_data = pd.DataFrame({
            'datetime': dates,
            'consumption': consumption,
            'renewable': consumption * self.renewable_share,
            'thermal': consumption * 0.6,
            'hydro': consumption * 0.25
        })
        
    def start_monitoring(self):
        """Start real-time energy monitoring"""
        self.is_monitoring = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status_var.set("Monitoring Active")
        
        # Start monitoring thread
        self.monitoring_thread = threading.Thread(target=self.monitor_energy)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()
        
    def stop_monitoring(self):
        """Stop energy monitoring"""
        self.is_monitoring = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_var.set("Monitoring Stopped")
        
    def monitor_energy(self):
        """Main monitoring loop"""
        while self.is_monitoring:
            # Simulate real-time data
            self.current_load = self.simulate_current_load()
            self.consumption_history.append({
                'timestamp': datetime.now(),
                'load': self.current_load,
                'renewable': self.current_load * self.renewable_share
            })
            
            # Update displays
            self.update_grid_status()
            self.update_consumption_chart()
            self.check_load_shedding_risk()
            
            time.sleep(5)  # Update every 5 seconds
            
    def simulate_current_load(self):
        """Simulate current power consumption"""
        # Base load with time-of-day variations
        hour = datetime.now().hour
        base_load = 800
        
        # Peak hours (6-9 AM, 6-9 PM)
        if 6 <= hour <= 9 or 18 <= hour <= 21:
            peak_factor = 1.3
        else:
            peak_factor = 0.8
            
        # Add random variations
        variation = random.uniform(0.9, 1.1)
        
        return int(base_load * peak_factor * variation)
        
    def update_grid_status(self):
        """Update power grid status display"""
        total_capacity = sum(station['capacity'] for station in self.zambia_power_stations.values())
        utilization = (self.current_load / total_capacity) * 100
        
        status_text = f"Current Load: {self.current_load} MW\n"
        status_text += f"Total Capacity: {total_capacity} MW\n"
        status_text += f"Utilization: {utilization:.1f}%\n"
        status_text += f"Renewable Share: {self.renewable_share*100:.1f}%\n\n"
        
        status_text += "Power Stations Status:\n"
        for station, info in self.zambia_power_stations.items():
            status_text += f"• {station}: {info['capacity']} MW ({info['type']}) - {info['status']}\n"
        
        # Load shedding risk
        if utilization > 90:
            status_text += f"\n⚠️ HIGH RISK - Load shedding likely\n"
        elif utilization > 80:
            status_text += f"\n⚠️ MEDIUM RISK - Monitor closely\n"
        else:
            status_text += f"\n✅ NORMAL - Grid stable\n"
            
        self.grid_status_text.delete(1.0, tk.END)
        self.grid_status_text.insert(1.0, status_text)
        
    def update_consumption_chart(self):
        """Update energy consumption chart"""
        self.ax.clear()
        
        if len(self.consumption_history) > 0:
            # Get last 24 hours of data
            recent_data = list(self.consumption_history)[-24:]
            timestamps = [d['timestamp'] for d in recent_data]
            loads = [d['load'] for d in recent_data]
            renewable = [d['renewable'] for d in recent_data]
            
            self.ax.plot(timestamps, loads, label='Total Load', color='blue', linewidth=2)
            self.ax.plot(timestamps, renewable, label='Renewable', color='green', linewidth=2)
            self.ax.axhline(y=total_capacity, color='red', linestyle='--', label='Capacity Limit')
            
        self.ax.set_title('Real-time Energy Consumption')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Power (MW)')
        self.ax.legend()
        self.ax.grid(True, alpha=0.3)
        
        # Rotate x-axis labels
        plt.setp(self.ax.xaxis.get_majorticklabels(), rotation=45)
        
        self.canvas.draw()
        
    def check_load_shedding_risk(self):
        """Check for load shedding risk and update schedule"""
        total_capacity = sum(station['capacity'] for station in self.zambia_power_stations.values())
        utilization = (self.current_load / total_capacity) * 100
        
        if utilization > 95:
            # High risk - immediate load shedding needed
            self.schedule_load_shedding(immediate=True)
        elif utilization > 85:
            # Medium risk - schedule load shedding
            self.schedule_load_shedding(immediate=False)
            
    def schedule_load_shedding(self, immediate=False):
        """Schedule load shedding for different zones"""
        if immediate:
            # Immediate load shedding
            zones = ['Lusaka', 'Kitwe', 'Ndola']  # High priority zones
            duration = 2  # hours
        else:
            # Scheduled load shedding
            zones = ['Livingstone', 'Chipata', 'Kabwe']  # Medium priority zones
            duration = 1  # hour
            
        for zone in zones:
            schedule_entry = {
                'zone': zone,
                'start_time': datetime.now() if immediate else datetime.now() + timedelta(hours=1),
                'duration': duration,
                'reason': 'High demand' if immediate else 'Preventive measure',
                'priority': self.load_shedding_zones[zone]['priority']
            }
            
            if schedule_entry not in self.load_shedding_schedule:
                self.load_shedding_schedule.append(schedule_entry)
                
        self.update_load_shedding_display()
        
    def update_load_shedding_display(self):
        """Update load shedding schedule display"""
        schedule_text = "Upcoming Load Shedding:\n\n"
        
        if not self.load_shedding_schedule:
            schedule_text += "No scheduled load shedding\n"
        else:
            for entry in self.load_shedding_schedule[:10]:  # Show next 10
                start_time = entry['start_time'].strftime("%H:%M")
                schedule_text += f"• {entry['zone']}: {start_time} ({entry['duration']}h)\n"
                schedule_text += f"  Reason: {entry['reason']}\n"
                schedule_text += f"  Priority: {entry['priority']}\n\n"
                
        self.schedule_text.delete(1.0, tk.END)
        self.schedule_text.insert(1.0, schedule_text)
        
    def predict_load_shedding(self):
        """Predict future load shedding based on consumption patterns"""
        if len(self.consumption_history) < 24:
            messagebox.showwarning("Insufficient Data", "Need at least 24 hours of data for prediction")
            return
            
        # Simple prediction based on historical patterns
        recent_loads = [d['load'] for d in list(self.consumption_history)[-24:]]
        avg_load = np.mean(recent_loads)
        trend = np.polyfit(range(len(recent_loads)), recent_loads, 1)[0]
        
        # Predict next 24 hours
        predictions = []
        for hour in range(24):
            predicted_load = avg_load + trend * hour
            predictions.append(predicted_load)
            
        # Check for load shedding risk
        total_capacity = sum(station['capacity'] for station in self.zambia_power_stations.values())
        risk_hours = [i for i, load in enumerate(predictions) if load > total_capacity * 0.9]
        
        if risk_hours:
            messagebox.showinfo("Load Shedding Prediction", 
                              f"High risk of load shedding in {len(risk_hours)} hours over next 24h")
        else:
            messagebox.showinfo("Load Shedding Prediction", 
                              "Low risk of load shedding in next 24 hours")
                              
    def optimize_energy(self):
        """Optimize energy consumption and generation"""
        suggestions = []
        
        # Analyze current consumption
        if len(self.consumption_history) > 0:
            recent_loads = [d['load'] for d in list(self.consumption_history)[-24:]]
            peak_load = max(recent_loads)
            avg_load = np.mean(recent_loads)
            
            # Peak shaving suggestions
            if peak_load > avg_load * 1.5:
                suggestions.append("🔋 Implement peak shaving with battery storage")
                suggestions.append("⚡ Shift non-essential loads to off-peak hours")
                
            # Renewable energy suggestions
            if self.renewable_share < 0.3:
                suggestions.append("🌞 Increase solar capacity by 50MW")
                suggestions.append("💨 Add wind power capacity")
                suggestions.append("🔋 Install battery storage for renewable energy")
                
            # Grid optimization
            total_capacity = sum(station['capacity'] for station in self.zambia_power_stations.values())
            utilization = (self.current_load / total_capacity) * 100
            
            if utilization > 80:
                suggestions.append("⚡ Activate emergency generation units")
                suggestions.append("🔄 Implement demand response programs")
                suggestions.append("🏭 Coordinate with industrial consumers for load reduction")
                
        # Add general optimization suggestions
        suggestions.extend([
            "💡 Promote energy-efficient appliances",
            "🏠 Implement smart home energy management",
            "🏭 Industrial energy efficiency programs",
            "🌱 Green building initiatives",
            "📊 Real-time energy monitoring for all consumers"
        ])
        
        self.optimization_suggestions = suggestions
        self.update_optimization_display()
        
    def update_optimization_display(self):
        """Update optimization suggestions display"""
        optimization_text = "Energy Optimization Suggestions:\n\n"
        
        for i, suggestion in enumerate(self.optimization_suggestions[:10], 1):
            optimization_text += f"{i}. {suggestion}\n"
            
        self.optimization_text.delete(1.0, tk.END)
        self.optimization_text.insert(1.0, optimization_text)
        
    def generate_report(self):
        """Generate comprehensive energy report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'system_status': {
                'monitoring_active': self.is_monitoring,
                'current_load': self.current_load,
                'total_capacity': sum(station['capacity'] for station in self.zambia_power_stations.values()),
                'utilization_percent': (self.current_load / sum(station['capacity'] for station in self.zambia_power_stations.values())) * 100
            },
            'power_stations': self.zambia_power_stations,
            'load_shedding_schedule': [
                {
                    'zone': entry['zone'],
                    'start_time': entry['start_time'].isoformat(),
                    'duration': entry['duration'],
                    'reason': entry['reason'],
                    'priority': entry['priority']
                } for entry in self.load_shedding_schedule
            ],
            'optimization_suggestions': self.optimization_suggestions,
            'consumption_history': [
                {
                    'timestamp': entry['timestamp'].isoformat(),
                    'load': entry['load'],
                    'renewable': entry['renewable']
                } for entry in list(self.consumption_history)[-100:]  # Last 100 entries
            ]
        }
        
        # Save report
        filename = f"zambia_energy_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
            
        self.status_var.set(f"Report generated: {filename}")
        messagebox.showinfo("Report Generated", f"Energy report saved as {filename}")
        
    def run(self):
        """Run the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = ZambiaEnergySystem()
    app.run()
