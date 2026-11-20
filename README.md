# SmartDrive Guardian AI - Desktop Application

**Real-Time Vehicle Error Detection and Predictive Safety Assistant**

A comprehensive Python-based desktop application that simulates intelligent vehicle diagnostics, predicts mechanical failures, and provides actionable safety recommendations using AI-based fault detection.

---

## 🚀 Features

### 1. **Real-Time Vehicle Monitoring**
   - Continuously monitors 6 key vehicle parameters:
     - Engine Temperature (70-130°C)
     - RPM (800-6000 rev/min)
     - Speed (0-200 km/h)
     - Oil Level (0-100%)
     - Brake Response Time (0.1-1.0 sec)
     - Fuel Level (0-100%)

### 2. **AI-Based Fault Detection**
   - Weighted scoring algorithm analyzes multiple symptoms simultaneously
   - Predicts 6 types of mechanical faults:
     - Cooling System Failure
     - Engine Lubrication Failure
     - Brake System Issue
     - Transmission Problem
     - Fuel System Warning
     - Radiator Blockage

### 3. **Severity Classification**
   - **Safe** (Green): Normal driving, no action required
   - **Warning** (Orange): Potential problem, check soon
   - **Critical** (Red): Immediate action needed

### 4. **Actionable Recommendations**
   - Context-specific guidance for drivers
   - Different recommendations based on fault type and severity
   - Priority alerts for critical issues

### 5. **Trend Analysis & Visualization**
   - Real-time charts showing parameter trends
   - 60-second historical data for visualization
   - Helps identify patterns and predict failures

### 6. **Database Integration (SQLite)**
   - Stores all vehicle parameters
   - Saves diagnostic analysis results
   - Maintains alert history
   - Enables long-term trend analysis

---

## 🔧 Installation

### Prerequisites
- Python 3.7 or higher
- Windows, macOS, or Linux

### Setup Instructions

1. **Navigate to the project directory:**
   ```bash
   cd d:\VenukaMora\SmartDriveGuardianAI1
   ```

2. **Create a Python virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # macOS/Linux
   ```

3. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python smartdrive.py
   ```

---

## 📊 How It Works

### System Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Vehicle Simulator                          │
│   (Generates realistic vehicle parameters)              │
└─────────────┬───────────────────────────────────────────┘
              │
┌─────────────▼───────────────────────────────────────────┐
│         Fault Detection Engine (AI Logic)               │
│   ├─ Calculate fault scores (weighted scoring)          │
│   ├─ Predict most probable fault                        │
│   ├─ Classify severity (Safe/Warning/Critical)          │
│   └─ Generate recommendations                           │
└─────────────┬───────────────────────────────────────────┘
              │
┌─────────────▼───────────────────────────────────────────┐
│              Database Manager                           │
│   ├─ Save vehicle parameters                            │
│   ├─ Store diagnostics results                          │
│   ├─ Record alerts                                      │
│   └─ Retrieve history                                   │
└─────────────┬───────────────────────────────────────────┘
              │
┌─────────────▼───────────────────────────────────────────┐
│         Desktop GUI (Tkinter)                           │
│   ├─ Real-time parameter display                        │
│   ├─ Diagnostic analysis panel                          │
│   ├─ Trend charts (matplotlib)                          │
│   └─ Alert history                                      │
└─────────────────────────────────────────────────────────┘
```

### Fault Detection Algorithm

**Weighted Scoring System:**

Each parameter contributes a weighted score to potential faults:

```
Cooling System Failure Score = 
    (Engine Temp - 110°C) × 5 +
    (RPM - 4000) × 2 / 1000 +
    (100% - Oil Level) × 1

If score > threshold → Fault detected
If multiple high scores exist → Most probable fault is selected
```

**Confidence Level Calculation:**
```
Confidence (%) = (Fault Score / Maximum Possible Score) × 100
```

### Data Flow

1. **Simulation**: Vehicle parameters are randomly generated within realistic ranges
2. **Analysis**: Fault detection engine calculates scores for all potential faults
3. **Prediction**: Most probable fault is identified with confidence level
4. **Classification**: Severity is determined based on parameter thresholds
5. **Recommendations**: Actionable guidance is generated
6. **Storage**: All data is saved to SQLite database
7. **Display**: UI shows real-time parameters, diagnostics, and trends

---

## 🎮 Using the Application

### Starting Monitoring

1. **Click "▶ Start Monitoring"** button to begin vehicle simulation
2. The system will start generating realistic vehicle data
3. Real-time parameters appear in the left panel
4. Diagnostics are analyzed and displayed
5. Charts and alerts update in real-time

### Interpreting the Display

**Left Panel:**
- **Vehicle Parameters**: Current values of all monitored metrics
- **Diagnostic Analysis**: Predicted fault, confidence level, severity
- **Recommendations**: Specific guidance based on detected conditions

**Right Panel:**
- **Parameter Trends**: Chart showing 60-second history of key metrics
- **Alerts & History**: All severity-2+ alerts with timestamps

### Controls

- **▶ Start Monitoring**: Begin vehicle monitoring
- **⏹ Stop Monitoring**: Pause monitoring
- **📊 Clear History**: Clear displayed alerts
- **Status Indicator**: Shows current monitoring state

---

## 📈 Understanding Fault Scores

Each fault has a scoring threshold. For example:

| Fault Type | Temperature Score | RPM Score | Oil Score | Threshold |
|------------|-------------------|-----------|-----------|-----------|
| Cooling System | High | Medium | Low | >= 10 |
| Lubrication | Medium | Low | High | >= 12 |
| Brake Issue | N/A | N/A | N/A | >= 8 |
| Transmission | Medium | High | Medium | >= 12 |
| Fuel Warning | N/A | N/A | N/A | >= 4 |

---

## 🗄️ Database Structure

### Tables

**vehicle_parameters**
- Stores all monitored vehicle metrics
- Timestamp, engine_temp, rpm, speed, oil_level, brake_response, fuel_level

**diagnostics**
- Records fault predictions and analysis
- Timestamp, predicted_fault, confidence_level, severity, fault_scores, recommendations

**alerts**
- Maintains alert history
- Timestamp, severity, message, action_taken

### Accessing Database

The application stores data in `smartdrive.db` (SQLite). You can query it:

```bash
sqlite3 smartdrive.db
SELECT * FROM vehicle_parameters LIMIT 10;
SELECT * FROM diagnostics ORDER BY timestamp DESC;
```

---

## 🤖 AI Techniques Used

1. **Rule-Based AI**: Predefined rules evaluate vehicle parameters
2. **Weighted Scoring**: Multiple symptoms combined for diagnosis
3. **Pattern Detection**: Identifies anomalies across parameters
4. **Severity Classification**: Risk-based alert prioritization
5. **Trend Analysis**: Predicts failures based on parameter trends

---

## 📊 Simulation Scenarios

The vehicle simulator creates realistic scenarios:

- **Normal**: Steady driving with gradual parameter changes
- **Acceleration**: High RPM, temperature increase, fuel consumption
- **Idle**: Low RPM, stable temperature, minimal consumption
- **Fault Emerging**: Unusual parameter combinations indicating problems

---

## 🎯 Use Cases

1. **Fleet Management**: Monitor vehicle health across multiple vehicles
2. **Preventive Maintenance**: Detect issues before critical failure
3. **Driver Safety**: Alert drivers to potential hazards
4. **Cost Reduction**: Prevent expensive repairs through early detection
5. **Insurance/Telematics**: Track vehicle health and driving patterns
6. **Educational Use**: Understand AI applications in IoT systems

---

## 🔮 Future Enhancements

- **Machine Learning**: Train models on real vehicle data for better predictions
- **Mobile App**: Send alerts to driver's smartphone
- **OBD-II Integration**: Connect to real vehicle hardware
- **Cloud Sync**: Store data in cloud for fleet analytics
- **Voice Alerts**: Text-to-speech notifications
- **GPS Integration**: Location-based emergency alerts
- **Predictive Analytics**: Long-term vehicle health predictions

---

## 🐛 Troubleshooting

### Application won't start
- Ensure Python 3.7+ is installed: `python --version`
- Check dependencies: `pip install -r requirements.txt`

### No data appearing
- Click "▶ Start Monitoring" button
- Check that process is running (look for status indicator)

### Charts not updating
- Ensure matplotlib is installed: `pip install matplotlib`
- Wait 5+ seconds for chart to initialize

### Database errors
- Delete `smartdrive.db` to reset database
- Ensure write permissions in project directory

---

## 📝 Example Output

### Console Output (When Running):
```
SmartDrive Guardian AI - Monitoring Started
Engine: 95°C | RPM: 2500 | Speed: 60 km/h | Oil: 85% | Brake: 0.2s | Fuel: 75%
Predicted Fault: Cooling System Failure (45% confidence)
Severity: Safe
---
Engine: 108°C | RPM: 4500 | Speed: 120 km/h | Oil: 72% | Brake: 0.35s | Fuel: 52%
Predicted Fault: Cooling System Failure (78% confidence)
Severity: Warning
Recommendations:
  - Check coolant level and radiator
  - Allow engine to cool before restarting
---
Engine: 118°C | RPM: 5200 | Speed: 140 km/h | Oil: 45% | Brake: 0.85s | Fuel: 30%
Predicted Fault: Engine Lubrication Failure (92% confidence)
Severity: Critical
Recommendations:
  - ⚠️  STOP THE VEHICLE IMMEDIATELY!
  - Turn on hazard lights and move to safety
  - Check oil level immediately
```

---

## 📚 Project Structure

```
SmartDriveGuardianAI1/
├── smartdrive.py          # Main application
├── requirements.txt       # Python dependencies
├── README.md              # This file
└── smartdrive.db          # SQLite database (created on first run)
```

---

## 📖 Documentation References

- [Python tkinter documentation](https://docs.python.org/3/library/tkinter.html)
- [SQLite3 documentation](https://docs.python.org/3/library/sqlite3.html)
- [Matplotlib documentation](https://matplotlib.org/)

---

## 👨‍💻 Developer

**Venuka Bandara**  
AI Essentials: From Data to Agents  
University of Moratuwa

---

## 📋 License

This project is created for educational purposes as part of AI Essentials course.

---

## 🎓 Learning Outcomes

This project demonstrates:

✅ Real-time data monitoring and simulation  
✅ AI-based decision making (rule-based systems)  
✅ Database design and management  
✅ Desktop application development (Tkinter GUI)  
✅ Data visualization (Matplotlib)  
✅ Multi-threaded application architecture  
✅ Practical AI application in IoT/Vehicle systems  
✅ Predictive analytics and trend analysis  

---

**SmartDrive Guardian AI** - Keeping Drivers Safe Through Intelligent Predictions 🚗🛡️
