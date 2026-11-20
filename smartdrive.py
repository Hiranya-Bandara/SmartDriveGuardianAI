"""
SmartDrive Guardian AI - Real-Time Vehicle Error Detection and Predictive Safety Assistant
A comprehensive vehicle monitoring system with AI-based fault prediction and safety alerts.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, timedelta
import random
import threading
import time
from collections import deque
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import json
import platform
if platform.system() == 'Windows':
    import winsound


# ============================================================================
# DATABASE MANAGEMENT
# ============================================================================

class DatabaseManager:
    """Manages SQLite database for vehicle diagnostics and history."""
    
    def __init__(self, db_path="smartdrive.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Vehicle Parameters Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vehicle_parameters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                engine_temp REAL,
                rpm INTEGER,
                speed INTEGER,
                oil_level REAL,
                brake_response REAL,
                fuel_level REAL
            )
        ''')
        
        # Diagnostics Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS diagnostics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                predicted_fault TEXT,
                confidence_level REAL,
                severity TEXT,
                fault_scores TEXT,
                recommendations TEXT
            )
        ''')
        
        # Alerts History Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                severity TEXT,
                message TEXT,
                action_taken TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_vehicle_parameters(self, params):
        """Save vehicle parameters to database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO vehicle_parameters 
            (engine_temp, rpm, speed, oil_level, brake_response, fuel_level)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (params['engine_temp'], params['rpm'], params['speed'],
              params['oil_level'], params['brake_response'], params['fuel_level']))
        
        conn.commit()
        conn.close()
    
    def save_diagnostic(self, diagnostic_data):
        """Save diagnostic analysis to database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO diagnostics 
            (predicted_fault, confidence_level, severity, fault_scores, recommendations)
            VALUES (?, ?, ?, ?, ?)
        ''', (diagnostic_data['fault'], diagnostic_data['confidence'],
              diagnostic_data['severity'], 
              json.dumps(diagnostic_data['scores']),
              json.dumps(diagnostic_data['recommendations'])))
        
        conn.commit()
        conn.close()
    
    def save_alert(self, severity, message, action=""):
        """Save alert to database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO alerts (severity, message, action_taken)
            VALUES (?, ?, ?)
        ''', (severity, message, action))
        
        conn.commit()
        conn.close()
    
    def get_recent_parameters(self, limit=100):
        """Retrieve recent vehicle parameters."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM vehicle_parameters 
            ORDER BY timestamp DESC LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        return results
    
    def get_recent_diagnostics(self, limit=20):
        """Retrieve recent diagnostics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM diagnostics 
            ORDER BY timestamp DESC LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        return results


# ============================================================================
# VEHICLE DATA SIMULATOR
# ============================================================================

class VehicleSimulator:
    """Simulates real-time vehicle data with realistic patterns."""
    
    def __init__(self):
        self.engine_temp = 85
        self.rpm = 1000
        self.speed = 0
        self.oil_level = 100
        self.brake_response = 0.2
        self.fuel_level = 80
        
        # Trend tracking for predictive analysis
        self.temp_history = deque(maxlen=60)
        self.rpm_history = deque(maxlen=60)
        self.oil_history = deque(maxlen=60)
    
    def simulate_driving_scenario(self):
        """Simulate realistic driving patterns."""
        scenario = random.choice(['normal', 'acceleration', 'idle', 'fault_emerging'])
        
        if scenario == 'normal':
            self.engine_temp += random.uniform(-1, 2)
            self.rpm += random.randint(-200, 300)
            self.speed += random.randint(-5, 10)
            self.oil_level -= random.uniform(0.01, 0.05)
            self.brake_response += random.uniform(-0.05, 0.05)
            self.fuel_level -= random.uniform(0.02, 0.1)
        
        elif scenario == 'acceleration':
            self.engine_temp += random.uniform(2, 5)
            self.rpm += random.randint(500, 1500)
            self.speed += random.randint(10, 30)
            self.oil_level -= random.uniform(0.05, 0.15)
            self.brake_response = 0.15 + random.uniform(-0.05, 0.05)
            self.fuel_level -= random.uniform(0.15, 0.3)
        
        elif scenario == 'idle':
            self.engine_temp -= random.uniform(0, 1.5)
            self.rpm = 800 + random.randint(-100, 100)
            self.speed = random.randint(0, 5)
            self.oil_level -= random.uniform(0, 0.02)
            self.brake_response = 0.2
            self.fuel_level -= random.uniform(0.01, 0.05)
        
        elif scenario == 'fault_emerging':
            # Simulate emerging fault conditions
            if random.random() < 0.3:
                self.engine_temp += random.uniform(3, 8)
                self.rpm += random.randint(200, 400)
                self.oil_level -= random.uniform(0.1, 0.3)
        
        # Constrain values to realistic ranges
        self.engine_temp = max(70, min(130, self.engine_temp))
        self.rpm = max(800, min(6000, self.rpm))
        self.speed = max(0, min(200, self.speed))
        self.oil_level = max(0, min(100, self.oil_level))
        self.brake_response = max(0.1, min(1.0, self.brake_response))
        self.fuel_level = max(0, min(100, self.fuel_level))
        
        # Store history for trend analysis
        self.temp_history.append(self.engine_temp)
        self.rpm_history.append(self.rpm)
        self.oil_history.append(self.oil_level)
    
    def get_current_state(self):
        """Return current vehicle state as dictionary."""
        return {
            'engine_temp': round(self.engine_temp, 2),
            'rpm': int(self.rpm),
            'speed': int(self.speed),
            'oil_level': round(self.oil_level, 2),
            'brake_response': round(self.brake_response, 2),
            'fuel_level': round(self.fuel_level, 2)
        }


# ============================================================================
# AI FAULT DETECTION ENGINE
# ============================================================================

class FaultDetectionEngine:
    """Rule-based AI system for fault prediction and severity classification."""
    
    def __init__(self):
        self.fault_definitions = {
            'Cooling System Failure': {
                'engine_temp': (110, 5),  # (threshold, weight)
                'rpm': (4000, 2),
                'oil_level': (30, 1)
            },
            'Engine Lubrication Failure': {
                'oil_level': (20, 6),
                'engine_temp': (100, 2),
                'rpm': (4000, 1)
            },
            'Brake System Issue': {
                'brake_response': (0.8, 4),
                'speed': (50, 2)
            },
            'Transmission Problem': {
                'rpm': (5500, 3),
                'engine_temp': (105, 2),
                'oil_level': (25, 2)
            },
            'Fuel System Warning': {
                'fuel_level': (15, 4),
                'speed': (80, 1)
            },
            'Radiator Blockage': {
                'engine_temp': (115, 4),
                'rpm': (3500, 2)
            }
        }
    
    def calculate_fault_scores(self, vehicle_params):
        """Calculate weighted scores for each potential fault."""
        fault_scores = {}
        
        for fault_name, criteria in self.fault_definitions.items():
            score = 0
            
            for param, (threshold, weight) in criteria.items():
                if param in vehicle_params:
                    value = vehicle_params[param]
                    
                    # Calculate how much the parameter exceeds threshold
                    if value > threshold:
                        excess = value - threshold
                        score += excess * weight / 10
            
            fault_scores[fault_name] = round(score, 2)
        
        return fault_scores
    
    def predict_fault(self, vehicle_params):
        """Predict the most probable fault with confidence level."""
        fault_scores = self.calculate_fault_scores(vehicle_params)
        
        # Find fault with highest score
        max_fault = max(fault_scores, key=fault_scores.get)
        max_score = fault_scores[max_fault]
        
        # Calculate confidence level (0-100%)
        total_possible_score = 100
        confidence = min(100, (max_score / total_possible_score) * 100)
        
        return {
            'fault': max_fault,
            'confidence': round(confidence, 1),
            'scores': fault_scores
        }
    
    def classify_severity(self, vehicle_params, fault_data):
        """Classify issue severity as Safe, Warning, or Critical."""
        
        # Critical thresholds
        if (vehicle_params['engine_temp'] > 115 or
            vehicle_params['oil_level'] < 15 or
            vehicle_params['brake_response'] > 0.9 or
            vehicle_params['fuel_level'] < 10):
            return 'Critical'
        
        # Warning thresholds
        if (vehicle_params['engine_temp'] > 105 or
            vehicle_params['oil_level'] < 25 or
            vehicle_params['brake_response'] > 0.7 or
            vehicle_params['fuel_level'] < 20 or
            fault_data['confidence'] > 60):
            return 'Warning'
        
        return 'Safe'
    
    def generate_recommendations(self, vehicle_params, fault, severity):
        """Generate actionable recommendations based on fault and severity."""
        recommendations = []
        
        if severity == 'Critical':
            recommendations.append("⚠️  STOP THE VEHICLE IMMEDIATELY!")
            recommendations.append("Turn on hazard lights and move to safety")
        
        if 'Cooling' in fault:
            recommendations.append("Check coolant level and radiator")
            recommendations.append("Allow engine to cool before restarting")
            recommendations.append("Reduce engine load")
        
        if 'Lubrication' in fault:
            recommendations.append("Check oil level immediately")
            recommendations.append("Add oil if needed")
            recommendations.append("Avoid high RPM driving")
        
        if 'Brake' in fault:
            recommendations.append("Check brake pads and fluid")
            recommendations.append("Test brakes gently")
            recommendations.append("Visit service center soon")
        
        if 'Transmission' in fault:
            recommendations.append("Avoid aggressive acceleration")
            recommendations.append("Drive smoothly and at moderate speeds")
        
        if 'Fuel' in fault:
            recommendations.append("Refuel at the nearest gas station")
        
        if severity == 'Warning' and not recommendations:
            recommendations.append("Monitor the vehicle closely")
            recommendations.append("Schedule maintenance check soon")
        
        if severity == 'Safe':
            recommendations.append("Continue normal driving")
            recommendations.append("Regular maintenance recommended")
        
        return recommendations


# ============================================================================
# MAIN GUI APPLICATION
# ============================================================================

class SmartDriveApplication(tk.Tk):
    """Main desktop application for SmartDrive Guardian AI."""
    
    def __init__(self):
        super().__init__()
        
        self.title("SmartDrive Guardian AI - Vehicle Diagnostic System")
        self.geometry("1400x950")
        self.configure(bg="#1a1a2e")
        
        # Set icon and styling
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_theme()
        
        # Initialize components
        self.db = DatabaseManager()
        self.simulator = VehicleSimulator()
        self.engine = FaultDetectionEngine()
        
        self.monitoring = False
        self.monitoring_thread = None
        
        # Data for trends
        self.time_points = deque(maxlen=60)
        self.temp_trend = deque(maxlen=60)
        self.rpm_trend = deque(maxlen=60)
        self.oil_trend = deque(maxlen=60)
        
        self.setup_ui()
        self.update_time = 0
    
    def configure_theme(self):
        """Configure professional dark theme with custom colors."""
        colors = {
            'bg': '#1a1a2e',
            'fg': '#eaeaea',
            'accent': '#0f3460',
            'success': '#00d4ff',
            'warning': '#ffa500',
            'error': '#ff4444',
            'button_bg': '#16213e',
            'button_fg': '#eaeaea'
        }
        
        # Configure ttk theme colors
        self.style.configure('TFrame', background='#1a1a2e', foreground='#eaeaea')
        self.style.configure('TLabel', background='#1a1a2e', foreground='#eaeaea')
        self.style.configure('TLabelframe', background='#1a1a2e', foreground='#00d4ff')
        self.style.configure('TLabelframe.Label', foreground='#00d4ff', background='#1a1a2e')
        self.style.configure('TButton', background='#16213e', foreground='#eaeaea')
        self.style.map('TButton',
                      background=[('active', '#0f3460'), ('pressed', '#16213e')],
                      foreground=[('active', '#00d4ff')])
        
        self.colors = colors
        self.last_beep_time = 0  # Track last beep to avoid spam
    
    def play_alert_sound(self, severity):
        """Play different beep patterns based on severity level."""
        # Prevent beep spam - only allow one beep every 5 seconds
        current_time = time.time()
        if current_time - self.last_beep_time < 5:
            return
        
        self.last_beep_time = current_time
        
        if platform.system() != 'Windows':
            return  # Sound alerts only on Windows
        
        try:
            if severity == 'Critical':
                # Urgent pattern: 3 rapid beeps
                for _ in range(3):
                    winsound.Beep(1000, 300)  # 1000 Hz, 300ms
                    time.sleep(0.1)
            elif severity == 'Warning':
                # Warning pattern: 2 beeps
                for _ in range(2):
                    winsound.Beep(800, 200)   # 800 Hz, 200ms
                    time.sleep(0.1)
        except Exception as e:
            print(f"Sound alert error: {e}")
    
    def setup_ui(self):
        """Setup the user interface."""
        
        # Banner/Header Section
        banner_frame = tk.Frame(self, bg="#0f3460", height=80)
        banner_frame.pack(fill=tk.X, side=tk.TOP)
        banner_frame.pack_propagate(False)
        
        # Banner content
        banner_content = tk.Frame(banner_frame, bg="#0f3460")
        banner_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Title with emoji
        title_label = tk.Label(banner_content, text="🚗 SmartDrive Guardian AI", 
                              font=("Arial", 24, "bold"), 
                              fg="#00d4ff", bg="#0f3460")
        title_label.pack(side=tk.LEFT)
        
        # Subtitle
        subtitle_label = tk.Label(banner_content, 
                                 text="Real-Time Vehicle Diagnostic System",
                                 font=("Arial", 10), 
                                 fg="#eaeaea", bg="#0f3460")
        subtitle_label.pack(side=tk.LEFT, padx=20)
        
        # Version info
        version_label = tk.Label(banner_content, 
                                text="v1.0 | AI-Powered",
                                font=("Arial", 9, "italic"), 
                                fg="#888888", bg="#0f3460")
        version_label.pack(side=tk.RIGHT)
        
        # Main container
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top control panel
        control_frame = ttk.LabelFrame(main_frame, text="⚙️ Control Panel", padding=10)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.start_btn = ttk.Button(control_frame, text="▶ Start Monitoring", 
                                    command=self.start_monitoring)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(control_frame, text="⏹ Stop Monitoring", 
                                   command=self.stop_monitoring, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame, text="📊 Clear History", 
                  command=self.clear_history).pack(side=tk.LEFT, padx=5)
        
        self.status_label = ttk.Label(control_frame, text="Status: Idle", 
                                      font=("Arial", 10, "bold"))
        self.status_label.pack(side=tk.RIGHT, padx=5)
        
        # Content container with two sections
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Current readings and diagnostics
        left_frame = ttk.Frame(content_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Current Parameters
        self.setup_parameters_panel(left_frame)
        
        # Diagnostics Info
        self.setup_diagnostics_panel(left_frame)
        
        # Right panel - trends and alerts
        right_frame = ttk.Frame(content_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Trend Chart
        self.setup_chart_panel(right_frame)
        
        # Alerts
        self.setup_alerts_panel(right_frame)
    
    def setup_parameters_panel(self, parent):
        """Setup vehicle parameters display."""
        params_frame = ttk.LabelFrame(parent, text="Vehicle Parameters", padding=10)
        params_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.param_labels = {}
        params = [
            ('engine_temp', 'Engine Temperature', '°C'),
            ('rpm', 'RPM', 'rev/min'),
            ('speed', 'Speed', 'km/h'),
            ('oil_level', 'Oil Level', '%'),
            ('brake_response', 'Brake Response', 'sec'),
            ('fuel_level', 'Fuel Level', '%')
        ]
        
        for param_id, param_name, unit in params:
            frame = ttk.Frame(params_frame)
            frame.pack(fill=tk.X, pady=5)
            
            ttk.Label(frame, text=param_name + ":", width=20).pack(side=tk.LEFT)
            
            value_label = ttk.Label(frame, text="-- " + unit, font=("Arial", 11, "bold"))
            value_label.pack(side=tk.LEFT, padx=10)
            
            self.param_labels[param_id] = value_label
    
    def setup_diagnostics_panel(self, parent):
        """Setup diagnostics information display."""
        diag_frame = ttk.LabelFrame(parent, text="Diagnostic Analysis", padding=10)
        diag_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Predicted Fault
        ttk.Label(diag_frame, text="Predicted Fault:", 
                 font=("Arial", 9, "bold")).pack(anchor=tk.W)
        self.fault_label = ttk.Label(diag_frame, text="--", 
                                     font=("Arial", 10), foreground="blue")
        self.fault_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Confidence Level
        ttk.Label(diag_frame, text="Confidence Level:", 
                 font=("Arial", 9, "bold")).pack(anchor=tk.W)
        self.confidence_label = ttk.Label(diag_frame, text="--", 
                                         font=("Arial", 10))
        self.confidence_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Severity
        ttk.Label(diag_frame, text="Severity Level:", 
                 font=("Arial", 9, "bold")).pack(anchor=tk.W)
        self.severity_label = ttk.Label(diag_frame, text="--", 
                                       font=("Arial", 11, "bold"))
        self.severity_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Recommendations
        ttk.Label(diag_frame, text="Recommendations:", 
                 font=("Arial", 9, "bold")).pack(anchor=tk.W)
        
        self.recommendations_text = tk.Text(diag_frame, height=8, width=50, 
                                           font=("Arial", 9))
        self.recommendations_text.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(diag_frame, orient=tk.VERTICAL, 
                                 command=self.recommendations_text.yview)
        self.recommendations_text.config(yscrollcommand=scrollbar.set)
    
    def setup_chart_panel(self, parent):
        """Setup trend chart display."""
        chart_frame = ttk.LabelFrame(parent, text="Parameter Trends (Last 60 seconds)", 
                                    padding=10)
        chart_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        
        self.canvas = FigureCanvasTkAgg(self.figure, master=chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.ax.set_title("Vehicle Parameter Trends")
        self.ax.set_xlabel("Time (seconds)")
        self.ax.set_ylabel("Value")
        self.ax.legend(loc="upper left")
    
    def setup_alerts_panel(self, parent):
        """Setup alerts and history display."""
        alerts_frame = ttk.LabelFrame(parent, text="Recent Alerts & History", 
                                     padding=10)
        alerts_frame.pack(fill=tk.BOTH, expand=True)
        
        # Alerts text area
        self.alerts_text = tk.Text(alerts_frame, height=20, width=50, 
                                  font=("Arial", 9), bg="#f9f9f9")
        self.alerts_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        scrollbar = ttk.Scrollbar(alerts_frame, orient=tk.VERTICAL, 
                                 command=self.alerts_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.alerts_text.config(yscrollcommand=scrollbar.set)
    
    def start_monitoring(self):
        """Start vehicle monitoring."""
        self.monitoring = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status_label.config(text="Status: Monitoring Active ✓")
        
        self.monitoring_thread = threading.Thread(target=self.monitoring_loop, daemon=True)
        self.monitoring_thread.start()
    
    def stop_monitoring(self):
        """Stop vehicle monitoring."""
        self.monitoring = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Monitoring Stopped")
    
    def monitoring_loop(self):
        """Main monitoring loop running in background thread."""
        while self.monitoring:
            try:
                # Simulate vehicle data
                self.simulator.simulate_driving_scenario()
                params = self.simulator.get_current_state()
                
                # Record to database
                self.db.save_vehicle_parameters(params)
                
                # Run diagnostics
                fault_data = self.engine.predict_fault(params)
                severity = self.engine.classify_severity(params, fault_data)
                recommendations = self.engine.generate_recommendations(
                    params, fault_data['fault'], severity
                )
                
                # Save diagnostic data
                diagnostic_data = {
                    'fault': fault_data['fault'],
                    'confidence': fault_data['confidence'],
                    'severity': severity,
                    'scores': fault_data['scores'],
                    'recommendations': recommendations
                }
                self.db.save_diagnostic(diagnostic_data)
                
                # Update UI
                self.after(0, self.update_ui, params, fault_data, severity, recommendations)
                
                # Save alert if not safe
                if severity != 'Safe':
                    alert_msg = f"{severity}: {fault_data['fault']} ({fault_data['confidence']}% confidence)"
                    self.db.save_alert(severity, alert_msg)
                
                time.sleep(1)  # Update every second
                
            except Exception as e:
                print(f"Error in monitoring loop: {e}")
                time.sleep(1)
    
    def update_ui(self, params, fault_data, severity, recommendations):
        """Update UI with latest vehicle data and diagnostics."""
        try:
            # Update parameter labels
            self.param_labels['engine_temp'].config(text=f"{params['engine_temp']} °C")
            self.param_labels['rpm'].config(text=f"{params['rpm']} rev/min")
            self.param_labels['speed'].config(text=f"{params['speed']} km/h")
            self.param_labels['oil_level'].config(text=f"{params['oil_level']} %")
            self.param_labels['brake_response'].config(text=f"{params['brake_response']} sec")
            self.param_labels['fuel_level'].config(text=f"{params['fuel_level']} %")
            
            # Update diagnostics
            self.fault_label.config(text=fault_data['fault'])
            self.confidence_label.config(text=f"{fault_data['confidence']}%")
            
            # Color-code severity
            severity_colors = {'Safe': 'green', 'Warning': 'orange', 'Critical': 'red'}
            self.severity_label.config(text=severity, 
                                      foreground=severity_colors.get(severity, 'black'))
            
            # Play alert sound for Critical and Warning severity
            if severity in ['Critical', 'Warning']:
                self.play_alert_sound(severity)
            
            # Update recommendations
            self.recommendations_text.config(state=tk.NORMAL)
            self.recommendations_text.delete(1.0, tk.END)
            recommendations_text = "\n".join(recommendations)
            self.recommendations_text.insert(tk.END, recommendations_text)
            self.recommendations_text.config(state=tk.DISABLED)
            
            # Update trends
            self.time_points.append(len(self.time_points))
            self.temp_trend.append(params['engine_temp'])
            self.rpm_trend.append(params['rpm'] / 100)  # Scale for visibility
            self.oil_trend.append(params['oil_level'])
            
            # Update chart every 5 seconds
            self.update_time += 1
            if self.update_time % 5 == 0:
                self.update_chart()
            
            # Update alerts
            if severity != 'Safe':
                severity_symbol = '🔴' if severity == 'Critical' else '🟠'
                alert_text = (f"{severity_symbol} [{datetime.now().strftime('%H:%M:%S')}] "
                            f"{severity}: {fault_data['fault']} ({fault_data['confidence']}%)\n")
                
                self.alerts_text.config(state=tk.NORMAL)
                self.alerts_text.insert(tk.END, alert_text)
                self.alerts_text.see(tk.END)
                self.alerts_text.config(state=tk.DISABLED)
        
        except Exception as e:
            print(f"Error updating UI: {e}")
    
    def update_chart(self):
        """Update trend chart."""
        try:
            self.ax.clear()
            
            if len(self.time_points) > 0:
                time_array = list(self.time_points)
                
                self.ax.plot(time_array, list(self.temp_trend), label='Engine Temp (°C)', 
                           marker='o', markersize=3)
                self.ax.plot(time_array, list(self.rpm_trend), label='RPM (÷100)', 
                           marker='s', markersize=3)
                self.ax.plot(time_array, list(self.oil_trend), label='Oil Level (%)', 
                           marker='^', markersize=3)
                
                self.ax.set_xlabel("Time (updates)")
                self.ax.set_ylabel("Value")
                self.ax.set_title("Vehicle Parameter Trends")
                self.ax.legend(loc="upper left")
                self.ax.grid(True, alpha=0.3)
            
            self.canvas.draw()
        
        except Exception as e:
            print(f"Error updating chart: {e}")
    
    def clear_history(self):
        """Clear alerts display."""
        if messagebox.askyesno("Clear History", "Clear all displayed alerts?"):
            self.alerts_text.config(state=tk.NORMAL)
            self.alerts_text.delete(1.0, tk.END)
            self.alerts_text.config(state=tk.DISABLED)


# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    app = SmartDriveApplication()
    app.mainloop()
