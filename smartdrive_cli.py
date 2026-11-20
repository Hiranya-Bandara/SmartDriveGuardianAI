"""
SmartDrive Guardian AI - Command Line Interface (CLI) Version
Alternative to GUI for server/headless environments
"""

import sqlite3
from datetime import datetime
import random
import time
from collections import deque
import sys
import json


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
                'engine_temp': (110, 5),
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
                    
                    if value > threshold:
                        excess = value - threshold
                        score += excess * weight / 10
            
            fault_scores[fault_name] = round(score, 2)
        
        return fault_scores
    
    def predict_fault(self, vehicle_params):
        """Predict the most probable fault with confidence level."""
        fault_scores = self.calculate_fault_scores(vehicle_params)
        
        max_fault = max(fault_scores, key=fault_scores.get)
        max_score = fault_scores[max_fault]
        
        confidence = min(100, (max_score / 100) * 100)
        
        return {
            'fault': max_fault,
            'confidence': round(confidence, 1),
            'scores': fault_scores
        }
    
    def classify_severity(self, vehicle_params, fault_data):
        """Classify issue severity as Safe, Warning, or Critical."""
        
        if (vehicle_params['engine_temp'] > 115 or
            vehicle_params['oil_level'] < 15 or
            vehicle_params['brake_response'] > 0.9 or
            vehicle_params['fuel_level'] < 10):
            return 'Critical'
        
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
# CLI APPLICATION
# ============================================================================

class SmartDriveCLI:
    """Command-line interface for SmartDrive Guardian AI."""
    
    def __init__(self):
        self.db = DatabaseManager()
        self.simulator = VehicleSimulator()
        self.engine = FaultDetectionEngine()
        self.update_count = 0
    
    def print_header(self):
        """Print application header."""
        print("\n" + "="*70)
        print("  SmartDrive Guardian AI - Vehicle Diagnostic System (CLI)")
        print("  Real-Time Error Detection and Predictive Safety Assistant")
        print("="*70 + "\n")
    
    def print_separator(self):
        """Print a separator line."""
        print("-" * 70)
    
    def print_vehicle_parameters(self, params):
        """Print current vehicle parameters."""
        print("\n📊 VEHICLE PARAMETERS:")
        print(f"   Engine Temperature: {params['engine_temp']:>6.2f}°C   │ RPM: {params['rpm']:>5} rev/min")
        print(f"   Oil Level:          {params['oil_level']:>6.2f}%    │ Speed: {params['speed']:>5} km/h")
        print(f"   Brake Response:     {params['brake_response']:>6.2f}sec  │ Fuel Level: {params['fuel_level']:>5.2f}%")
    
    def print_diagnostics(self, fault_data, severity, recommendations):
        """Print diagnostic analysis."""
        severity_symbol = {
            'Safe': '🟢',
            'Warning': '🟠',
            'Critical': '🔴'
        }.get(severity, '⚪')
        
        print(f"\n🔍 DIAGNOSTIC ANALYSIS:")
        print(f"   Predicted Fault:   {fault_data['fault']}")
        print(f"   Confidence Level:  {fault_data['confidence']}%")
        print(f"   Severity Level:    {severity_symbol} {severity}")
        
        print(f"\n📋 FAULT SCORES:")
        for fault_name, score in sorted(fault_data['scores'].items(), 
                                       key=lambda x: x[1], reverse=True):
            bar_length = int(score / 2)
            bar = "█" * bar_length
            print(f"   {fault_name:<30} {score:>6.2f} {bar}")
        
        print(f"\n✅ RECOMMENDATIONS:")
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. {rec}")
    
    def run_monitoring(self, duration=60):
        """Run vehicle monitoring for specified duration."""
        self.print_header()
        
        print(f"Starting monitoring for {duration} seconds...")
        print("Press Ctrl+C to stop early.\n")
        
        self.print_separator()
        
        start_time = time.time()
        
        try:
            while time.time() - start_time < duration:
                self.update_count += 1
                
                # Simulate vehicle data
                self.simulator.simulate_driving_scenario()
                params = self.simulator.get_current_state()
                
                # Save to database
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
                
                # Display results
                print(f"\n⏱️  Update #{self.update_count} - {datetime.now().strftime('%H:%M:%S')}")
                self.print_vehicle_parameters(params)
                self.print_diagnostics(fault_data, severity, recommendations)
                
                # Save alert if not safe
                if severity != 'Safe':
                    alert_msg = f"{severity}: {fault_data['fault']} ({fault_data['confidence']}% confidence)"
                    self.db.save_alert(severity, alert_msg)
                
                self.print_separator()
                
                # Wait before next update
                time.sleep(2)
        
        except KeyboardInterrupt:
            print("\n\n⏹️  Monitoring stopped by user.")
        
        self.print_summary()
    
    def print_summary(self):
        """Print monitoring summary."""
        print("\n" + "="*70)
        print("  MONITORING SUMMARY")
        print("="*70)
        
        # Get statistics from database
        conn = sqlite3.connect("smartdrive.db")
        cursor = conn.cursor()
        
        # Count records
        cursor.execute("SELECT COUNT(*) FROM vehicle_parameters")
        param_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM diagnostics WHERE severity='Warning'")
        warning_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM diagnostics WHERE severity='Critical'")
        critical_count = cursor.fetchone()[0]
        
        # Get averages
        cursor.execute("SELECT AVG(engine_temp), MAX(engine_temp), MIN(engine_temp) FROM vehicle_parameters")
        temp_data = cursor.fetchone()
        
        cursor.execute("SELECT AVG(oil_level), MIN(oil_level) FROM vehicle_parameters")
        oil_data = cursor.fetchone()
        
        conn.close()
        
        print(f"\n📊 Data Collected:")
        print(f"   Total Parameter Records:  {param_count}")
        print(f"   Warnings Generated:       {warning_count}")
        print(f"   Critical Alerts:          {critical_count}")
        
        if temp_data[0]:
            print(f"\n🌡️  Temperature Statistics:")
            print(f"   Average: {temp_data[0]:>6.2f}°C")
            print(f"   Maximum: {temp_data[1]:>6.2f}°C")
            print(f"   Minimum: {temp_data[2]:>6.2f}°C")
        
        if oil_data[0]:
            print(f"\n🛢️  Oil Level Statistics:")
            print(f"   Average: {oil_data[0]:>6.2f}%")
            print(f"   Minimum: {oil_data[1]:>6.2f}%")
        
        print(f"\n💾 Data saved to: smartdrive.db")
        print("="*70 + "\n")
    
    def show_history(self, limit=10):
        """Show recent diagnostic history."""
        print("\n" + "="*70)
        print(f"  RECENT DIAGNOSTICS (Last {limit})")
        print("="*70 + "\n")
        
        conn = sqlite3.connect("smartdrive.db")
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT timestamp, predicted_fault, confidence_level, severity
            FROM diagnostics
            ORDER BY timestamp DESC LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        if not results:
            print("No diagnostic history available.\n")
            return
        
        for row in results:
            timestamp, fault, confidence, severity = row
            severity_symbol = {
                'Safe': '🟢',
                'Warning': '🟠',
                'Critical': '🔴'
            }.get(severity, '⚪')
            
            print(f"{severity_symbol} [{timestamp}]")
            print(f"   Fault: {fault}")
            print(f"   Confidence: {confidence}%")
            print()


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="SmartDrive Guardian AI - Vehicle Diagnostic System"
    )
    parser.add_argument(
        '--duration',
        type=int,
        default=60,
        help='Monitoring duration in seconds (default: 60)'
    )
    parser.add_argument(
        '--history',
        type=int,
        help='Show last N diagnostic records'
    )
    
    args = parser.parse_args()
    
    cli = SmartDriveCLI()
    
    if args.history:
        cli.show_history(args.history)
    else:
        cli.run_monitoring(args.duration)


if __name__ == "__main__":
    main()
