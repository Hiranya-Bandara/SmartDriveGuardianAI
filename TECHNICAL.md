# SmartDrive Guardian AI - Technical Documentation

## 📋 Table of Contents
1. [System Architecture](#system-architecture)
2. [Component Descriptions](#component-descriptions)
3. [Database Schema](#database-schema)
4. [Fault Detection Algorithm](#fault-detection-algorithm)
5. [API Reference](#api-reference)
6. [Configuration Guide](#configuration-guide)
7. [Performance Considerations](#performance-considerations)
8. [Extension Points](#extension-points)

---

## 🏗️ System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE LAYER                    │
│  ┌──────────────────────┬──────────────────────────────────┐ │
│  │   GUI (Tkinter)      │   CLI (Command Line)             │ │
│  │  • Real-time Display │  • Batch Processing              │ │
│  │  • Trend Charts      │  • Server Integration            │ │
│  │  • Alert Alerts      │  • Headless Operation            │ │
│  └──────────────────────┴──────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                        │
│  ┌──────────────────────┬──────────────────────────────────┐ │
│  │ VehicleSimulator     │  FaultDetectionEngine            │ │
│  │ • Generates Params   │  • Weighted Scoring             │ │
│  │ • Realistic Patterns │  • Fault Prediction             │ │
│  │ • Trend Tracking     │  • Severity Classification      │ │
│  │                      │  • Recommendations              │ │
│  └──────────────────────┴──────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────┐
│                    DATA LAYER                               │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │         DatabaseManager (SQLite3)                        │ │
│  │  • Vehicle Parameters Table                             │ │
│  │  • Diagnostics Table                                    │ │
│  │  • Alerts Table                                         │ │
│  └──────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow Diagram

```
┌──────────────────┐
│ VehicleSimulator │ (Generate simulated sensor data)
└────────┬─────────┘
         │ Vehicle Parameters Dict
         ↓
┌──────────────────────────┐
│ FaultDetectionEngine     │
│ 1. Calculate Scores      │ (Analyze symptoms)
│ 2. Predict Fault         │
│ 3. Classify Severity     │ (Determine urgency)
│ 4. Generate Recommend.   │
└────────┬─────────────────┘
         │ Diagnostic Data
         ↓
┌──────────────────────┐
│  DatabaseManager     │
│  • Save Parameters   │ (Persist all data)
│  • Save Diagnostics  │
│  • Save Alerts       │
└────────┬─────────────┘
         │ Database Records
         ↓
┌──────────────────────┐
│   User Interface     │
│  • Display Results   │ (Present to user)
│  • Show Trends       │
│  • Alert User        │
└──────────────────────┘
```

---

## 🔧 Component Descriptions

### 1. VehicleSimulator

**Purpose:** Generates realistic vehicle parameters simulating actual driving conditions.

**Key Methods:**
```python
simulate_driving_scenario()  # Updates parameters based on random scenario
get_current_state()         # Returns dict with current parameter values
```

**Parameters Generated:**
- `engine_temp`: 70-130°C (realistic engine operating range)
- `rpm`: 800-6000 (revolutions per minute)
- `speed`: 0-200 (km/h)
- `oil_level`: 0-100 (percentage)
- `brake_response`: 0.1-1.0 (seconds)
- `fuel_level`: 0-100 (percentage)

**Scenarios:**
- **Normal**: Steady driving with gradual changes
- **Acceleration**: High RPM, temperature, fuel consumption
- **Idle**: Low RPM, stable parameters
- **Fault Emerging**: Unusual combinations simulating mechanical issues

### 2. FaultDetectionEngine

**Purpose:** Implements rule-based AI to predict mechanical faults.

**Key Methods:**
```python
calculate_fault_scores(vehicle_params)        # Compute weighted scores
predict_fault(vehicle_params)                 # Identify most probable fault
classify_severity(vehicle_params, fault_data) # Determine urgency level
generate_recommendations(...)                 # Create actionable guidance
```

**Fault Types:**
1. **Cooling System Failure** - High temp + High RPM
2. **Engine Lubrication Failure** - Low oil + High temp
3. **Brake System Issue** - High brake response time
4. **Transmission Problem** - Very high RPM + High temp
5. **Fuel System Warning** - Low fuel level
6. **Radiator Blockage** - Very high temperature

**Severity Thresholds:**
```python
Critical if:
  - engine_temp > 115°C OR
  - oil_level < 15% OR
  - brake_response > 0.9s OR
  - fuel_level < 10%

Warning if:
  - engine_temp > 105°C OR
  - oil_level < 25% OR
  - brake_response > 0.7s OR
  - fuel_level < 20% OR
  - confidence > 60%

Safe: Otherwise
```

### 3. DatabaseManager

**Purpose:** Manages SQLite persistence for all diagnostic data.

**Key Methods:**
```python
init_database()              # Create tables
save_vehicle_parameters()    # Store sensor data
save_diagnostic()           # Store analysis results
save_alert()               # Log alerts
get_recent_parameters()    # Retrieve history
get_recent_diagnostics()   # Retrieve diagnostics
```

### 4. GUI Application (Tkinter)

**Purpose:** Provides real-time visual interface for monitoring.

**Components:**
- **Control Panel**: Start/Stop monitoring, Status display
- **Parameters Panel**: Current vehicle metrics
- **Diagnostics Panel**: Fault prediction, severity, recommendations
- **Trend Charts**: Real-time matplotlib visualization
- **Alerts Panel**: Historical alert log

**Threading Model:**
- Main thread: UI responsive, handles user events
- Background thread: Monitoring loop, data collection
- Queue-free design: Direct UI updates via `after()` method

### 5. CLI Application (smartdrive_cli.py)

**Purpose:** Command-line interface for headless environments.

**Usage:**
```bash
python smartdrive_cli.py --duration 120  # Monitor for 120 seconds
python smartdrive_cli.py --history 20   # Show last 20 diagnostics
```

**Features:**
- Text-based output with emoji indicators
- Real-time parameter display
- Severity color-coding via emoji (🟢🟠🔴)
- Compact fault score visualization
- Summary statistics

---

## 🗄️ Database Schema

### Table: vehicle_parameters

```sql
CREATE TABLE vehicle_parameters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    engine_temp REAL,        -- Engine temperature in Celsius
    rpm INTEGER,             -- Revolutions per minute
    speed INTEGER,           -- Current speed in km/h
    oil_level REAL,          -- Oil level percentage
    brake_response REAL,     -- Brake response time in seconds
    fuel_level REAL          -- Fuel level percentage
);
```

**Sample Query:**
```sql
-- Get average engine temperature for last 10 minutes
SELECT AVG(engine_temp), COUNT(*) 
FROM vehicle_parameters
WHERE timestamp > datetime('now', '-10 minutes');
```

### Table: diagnostics

```sql
CREATE TABLE diagnostics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    predicted_fault TEXT,      -- Name of predicted fault
    confidence_level REAL,     -- Confidence percentage (0-100)
    severity TEXT,             -- Safe / Warning / Critical
    fault_scores TEXT,         -- JSON string of all fault scores
    recommendations TEXT       -- JSON array of recommendations
);
```

**Sample Data:**
```json
{
  "fault": "Cooling System Failure",
  "confidence": 82.5,
  "severity": "Warning",
  "scores": {
    "Cooling System Failure": 8.25,
    "Engine Lubrication Failure": 3.2,
    ...
  },
  "recommendations": [
    "Check coolant level and radiator",
    "Allow engine to cool before restarting"
  ]
}
```

### Table: alerts

```sql
CREATE TABLE alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    severity TEXT,             -- Warning / Critical
    message TEXT,              -- Alert description
    action_taken TEXT          -- Action taken by driver (optional)
);
```

---

## 🧠 Fault Detection Algorithm

### Weighted Scoring System

**Step 1: Parameter Threshold Evaluation**

For each fault and parameter:
```
if parameter_value > threshold:
    score += (parameter_value - threshold) × weight
```

**Example:**
```python
engine_temp = 115°C
Cooling System Failure threshold = 110°C
weight = 5

score = (115 - 110) × 5 = 25
```

**Step 2: Multi-Symptom Analysis**

```python
cooling_failure_score = 0

if engine_temp > 110:
    cooling_failure_score += (engine_temp - 110) × 5

if rpm > 4000:
    cooling_failure_score += (rpm - 4000) / 1000 × 2

if oil_level < 30:
    cooling_failure_score += (30 - oil_level) × 1
```

**Step 3: Fault Selection**

```python
all_faults = {
    "Cooling System": 8.5,
    "Lubrication": 4.2,
    "Brake System": 2.1,
    ...
}

predicted_fault = max(all_faults, key=all_faults.get)
max_score = all_faults[predicted_fault]

confidence = min(100, (max_score / 100) × 100)
```

**Step 4: Severity Determination**

Critical conditions checked first:
```python
if (engine_temp > 115) or (oil_level < 15) or \
   (brake_response > 0.9) or (fuel_level < 10):
    severity = "Critical"
elif (engine_temp > 105) or (oil_level < 25) or \
     (confidence > 60):
    severity = "Warning"
else:
    severity = "Safe"
```

**Step 5: Recommendation Generation**

Based on fault type and severity:
```python
if severity == "Critical":
    add("STOP THE VEHICLE IMMEDIATELY!")
    add("Turn on hazard lights")

if "Cooling" in fault:
    add("Check coolant level")
    add("Allow engine to cool")

if severity == "Warning":
    add("Monitor vehicle closely")
    add("Schedule maintenance")
```

---

## 📚 API Reference

### VehicleSimulator

```python
class VehicleSimulator:
    """Vehicle parameter simulator."""
    
    def __init__(self):
        """Initialize simulator with default values."""
    
    def simulate_driving_scenario(self):
        """
        Update vehicle parameters based on random scenario.
        Updates: engine_temp, rpm, speed, oil_level, brake_response, fuel_level
        """
    
    def get_current_state(self) -> dict:
        """
        Return current vehicle state.
        
        Returns:
            {
                'engine_temp': float,
                'rpm': int,
                'speed': int,
                'oil_level': float,
                'brake_response': float,
                'fuel_level': float
            }
        """
```

### FaultDetectionEngine

```python
class FaultDetectionEngine:
    """AI-based fault detection and prediction."""
    
    def calculate_fault_scores(self, vehicle_params: dict) -> dict:
        """
        Calculate weighted scores for each potential fault.
        
        Args:
            vehicle_params: Dictionary with vehicle parameters
        
        Returns:
            {
                'fault_name': score,
                ...
            }
        """
    
    def predict_fault(self, vehicle_params: dict) -> dict:
        """
        Predict most probable fault.
        
        Args:
            vehicle_params: Current vehicle parameters
        
        Returns:
            {
                'fault': str,
                'confidence': float (0-100),
                'scores': dict
            }
        """
    
    def classify_severity(self, vehicle_params: dict, fault_data: dict) -> str:
        """
        Classify severity of detected issue.
        
        Args:
            vehicle_params: Current vehicle parameters
            fault_data: Fault prediction result
        
        Returns:
            'Safe' | 'Warning' | 'Critical'
        """
    
    def generate_recommendations(self, vehicle_params: dict, 
                                fault: str, severity: str) -> list:
        """
        Generate actionable recommendations.
        
        Args:
            vehicle_params: Current vehicle parameters
            fault: Predicted fault name
            severity: Severity classification
        
        Returns:
            List of recommendation strings
        """
```

### DatabaseManager

```python
class DatabaseManager:
    """SQLite database management."""
    
    def save_vehicle_parameters(self, params: dict) -> None:
        """Save vehicle parameters to database."""
    
    def save_diagnostic(self, diagnostic_data: dict) -> None:
        """Save diagnostic analysis to database."""
    
    def save_alert(self, severity: str, message: str, 
                   action: str = "") -> None:
        """Save alert to database."""
    
    def get_recent_parameters(self, limit: int = 100) -> list:
        """Retrieve recent vehicle parameters."""
    
    def get_recent_diagnostics(self, limit: int = 20) -> list:
        """Retrieve recent diagnostics."""
```

---

## ⚙️ Configuration Guide

### Adjusting Fault Thresholds

Edit `FaultDetectionEngine.fault_definitions`:

```python
self.fault_definitions = {
    'Cooling System Failure': {
        'engine_temp': (110, 5),    # (threshold, weight)
        'rpm': (4000, 2),
        'oil_level': (30, 1)
    },
    ...
}
```

**Format:**
- First value: Threshold (parameter must exceed this)
- Second value: Weight (importance in scoring)

**Example: Make cooling detection more sensitive**
```python
'engine_temp': (105, 8)  # Lower threshold, higher weight
```

### Adjusting Severity Thresholds

Edit `classify_severity()` method:

```python
# Make critical level stricter
if (vehicle_params['engine_temp'] > 125 or  # was 115
    vehicle_params['oil_level'] < 10):      # was 15
    return 'Critical'
```

### Modifying Simulation Scenarios

Edit `VehicleSimulator.simulate_driving_scenario()`:

```python
elif scenario == 'aggressive_driving':
    self.engine_temp += random.uniform(5, 10)  # More aggressive
    self.rpm += random.randint(1000, 2000)
    self.oil_level -= random.uniform(0.2, 0.5)
```

### Changing Update Frequency

**In GUI:**
```python
time.sleep(1)  # Update every 1 second
# Change to: time.sleep(0.5) for faster updates
```

**In CLI:**
```python
time.sleep(2)  # Change update interval
# Change to: time.sleep(1) for faster display
```

---

## ⚡ Performance Considerations

### Memory Usage

- **Vehicle Simulator**: ~100 bytes (6 float values)
- **Fault scores dict**: ~500 bytes (6 faults × 2 values)
- **Database**: Grows ~2KB per 100 updates (100 seconds = 200 bytes)

**Estimated Usage for 1 hour monitoring:**
- Parameters: 100 KB
- Diagnostics: 100 KB
- Alerts: 50 KB
- Total: ~250 KB

### CPU Usage

- **Simulation**: <1% (simple random number generation)
- **Scoring**: <1% (arithmetic operations)
- **Database I/O**: 1-2% (write operations)
- **GUI rendering**: 2-5% (tkinter + matplotlib)
- **Total**: 3-8% on modern systems

### Optimization Tips

1. **Reduce chart update frequency:**
```python
if self.update_time % 10 == 0:  # Update every 10 seconds instead of 5
    self.update_chart()
```

2. **Limit database query size:**
```python
get_recent_parameters(limit=50)  # Instead of 100
```

3. **Use CLI for headless servers:**
- No GUI overhead
- Minimal memory usage
- Suitable for continuous monitoring

---

## 🔌 Extension Points

### Adding New Fault Types

1. **Add to fault_definitions:**
```python
'Alternator Failure': {
    'battery_voltage': (12, 4),
    'rpm': (3000, 1)
}
```

2. **Add vehicle parameter:**
```python
self.battery_voltage = 13.5  # in VehicleSimulator
```

3. **Update recommendation logic:**
```python
if 'Alternator' in fault:
    recommendations.append("Check alternator function")
```

### Adding Machine Learning

Replace fault detection:
```python
def predict_fault_ml(self, vehicle_params):
    # Use trained model instead of rule-based scoring
    predictions = self.ml_model.predict(vehicle_params)
    return predictions
```

### Adding Real Sensor Integration

Replace simulator:
```python
class RealVehicleData:
    def get_obd2_data(self):
        # Read from OBD-II adapter
        return {
            'engine_temp': obd.query(OBDCommand.ENGINE_COOLANT_TEMP),
            ...
        }
```

### Adding Mobile App Integration

Use API endpoint:
```python
@app.route('/api/diagnostics')
def get_diagnostics():
    latest = db.get_recent_diagnostics(1)[0]
    return jsonify(latest)
```

### Adding Voice Alerts

```python
import pyttsx3

def voice_alert(self, message):
    engine = pyttsx3.init()
    engine.say(message)
    engine.runAndWait()
```

### Adding Data Export

```python
def export_to_csv(self):
    df = pd.read_sql_query(
        "SELECT * FROM diagnostics", 
        sqlite3.connect("smartdrive.db")
    )
    df.to_csv("diagnostics_export.csv")
```

---

## 🧪 Testing Examples

### Unit Test - Fault Scoring

```python
def test_cooling_system_fault():
    engine = FaultDetectionEngine()
    params = {
        'engine_temp': 120,
        'rpm': 4500,
        'speed': 100,
        'oil_level': 50,
        'brake_response': 0.3,
        'fuel_level': 50
    }
    
    result = engine.predict_fault(params)
    assert 'Cooling' in result['fault']
    assert result['confidence'] > 60
```

### Integration Test - Full Pipeline

```python
def test_full_monitoring_cycle():
    sim = VehicleSimulator()
    engine = FaultDetectionEngine()
    db = DatabaseManager()
    
    sim.simulate_driving_scenario()
    params = sim.get_current_state()
    
    fault_data = engine.predict_fault(params)
    severity = engine.classify_severity(params, fault_data)
    
    db.save_vehicle_parameters(params)
    db.save_diagnostic({...})
    
    assert db.get_recent_parameters(1) is not None
```

---

## 📊 Monitoring Statistics

Query useful monitoring data:

```sql
-- Average temperature over time
SELECT 
    datetime(timestamp, 'start of minute') as minute,
    AVG(engine_temp) as avg_temp,
    COUNT(*) as samples
FROM vehicle_parameters
GROUP BY minute
ORDER BY minute DESC;

-- Fault frequency
SELECT 
    predicted_fault,
    COUNT(*) as occurrences,
    AVG(confidence_level) as avg_confidence
FROM diagnostics
GROUP BY predicted_fault
ORDER BY occurrences DESC;

-- Critical alerts
SELECT 
    timestamp,
    message,
    action_taken
FROM alerts
WHERE severity = 'Critical'
ORDER BY timestamp DESC
LIMIT 20;
```

---

## 🔍 Debugging Tips

### Enable Verbose Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug(f"Fault scores: {fault_scores}")
logger.info(f"Detected: {fault_data['fault']}")
```

### Inspect Database

```bash
sqlite3 smartdrive.db ".mode column" "SELECT * FROM diagnostics LIMIT 5;"
```

### Monitor Performance

```python
import time
start = time.time()
result = engine.predict_fault(params)
duration = time.time() - start
print(f"Prediction took {duration*1000:.2f}ms")
```

---

**SmartDrive Guardian AI - Technical Documentation Complete** 📚
