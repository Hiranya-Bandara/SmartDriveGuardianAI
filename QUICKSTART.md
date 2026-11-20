# SmartDrive Guardian AI - Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Step 1: Install Python
- Download Python 3.7+ from [python.org](https://python.org)
- Make sure to check "Add Python to PATH" during installation

### Step 2: Install Dependencies
Open a terminal in the project directory and run:
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application

**Windows:**
- Double-click `run.bat`

**macOS/Linux:**
```bash
bash run.sh
```

**Or directly:**
```bash
python smartdrive.py
```

---

## 📖 First Time Using the App?

### 1. **Understanding the Interface**

The application is divided into 4 sections:

```
┌─────────────────────────────────────────────────┐
│         CONTROL PANEL (Top)                     │
│  [Start] [Stop] [Clear] | Status: Idle         │
├──────────────────────────┬──────────────────────┤
│                          │                      │
│  LEFT PANEL              │   RIGHT PANEL        │
│                          │                      │
│ • Vehicle Parameters    │  • Trend Charts      │
│ • Diagnostic Analysis   │  • Alerts & History  │
│ • Recommendations       │                      │
│                          │                      │
└──────────────────────────┴──────────────────────┘
```

### 2. **Starting Your First Monitoring Session**

1. Click the **"▶ Start Monitoring"** button
2. The application will begin simulating vehicle data
3. Watch the parameters update in real-time
4. After ~5-10 seconds, you'll see trend charts and diagnostics

### 3. **Reading the Diagnostics**

**Example scenario:**
```
Vehicle Parameters
├─ Engine Temperature: 108°C  ← Getting warm
├─ RPM: 4500 rev/min          ← High RPM
├─ Oil Level: 72%             ← Acceptable
├─ Speed: 120 km/h
├─ Brake Response: 0.35 sec
└─ Fuel Level: 52%

Diagnostic Analysis
├─ Predicted Fault: Cooling System Failure
├─ Confidence Level: 78%
├─ Severity Level: ⚠️ Warning
└─ Recommendations:
   • Check coolant level and radiator
   • Allow engine to cool before restarting
   • Reduce engine load
```

### 4. **Understanding Severity Levels**

- 🟢 **Safe**: Normal driving, no action needed
- 🟠 **Warning**: Potential issue, check soon
- 🔴 **Critical**: Stop immediately!

---

## 🎯 Common Scenarios

### Scenario 1: Engine Overheating
**What You'll See:**
- Engine Temperature > 105°C
- High RPM values
- Fault Predicted: "Cooling System Failure" (60-85% confidence)

**What to Do:**
- Check coolant level
- Allow engine to cool
- Reduce driving stress

### Scenario 2: Low Oil Level
**What You'll See:**
- Oil Level < 25%
- Engine Temperature slightly elevated
- Fault Predicted: "Engine Lubrication Failure" (70-90% confidence)

**What to Do:**
- Add oil immediately
- Avoid high RPM driving
- Check for leaks

### Scenario 3: Brake Issues
**What You'll See:**
- Brake Response Time > 0.7 seconds
- Fault Predicted: "Brake System Issue" (60-75% confidence)

**What to Do:**
- Check brake pads
- Visit service center
- Test brakes gently

### Scenario 4: Low Fuel
**What You'll See:**
- Fuel Level < 15%
- Fault Predicted: "Fuel System Warning" (50-80% confidence)

**What to Do:**
- Refuel immediately
- Avoid running out of fuel (damages pump)

---

## 📊 Using the Trend Charts

The charts show the last 60 seconds of data for:
- **Engine Temperature** (orange with circles): Should stay 80-100°C during normal driving
- **RPM** (blue with squares): Divided by 100 for scale (so 2000 RPM shows as 20)
- **Oil Level** (green with triangles): Should stay above 50%

**What trends tell you:**
- Steadily rising temperature → Cooling problem
- Rapid oil level drop → Leak or consumption
- Spiking RPM with temperature spike → Transmission issue

---

## 🗄️ Database and History

All your vehicle data is automatically saved in `smartdrive.db`. You can:

1. **View recent diagnostics:**
   ```bash
   sqlite3 smartdrive.db
   SELECT * FROM diagnostics ORDER BY timestamp DESC LIMIT 5;
   ```

2. **Check alert history:**
   ```
   SELECT * FROM alerts WHERE severity='Critical' LIMIT 10;
   ```

3. **Analyze trends:**
   ```
   SELECT AVG(engine_temp), MAX(engine_temp) FROM vehicle_parameters;
   ```

---

## ⚙️ Advanced Features

### Customizing Fault Thresholds
Edit the `fault_definitions` in `smartdrive.py` to adjust sensitivity:
```python
'Cooling System Failure': {
    'engine_temp': (110, 5),  # Threshold: 110°C, Weight: 5
    ...
}
```

### Adjusting Simulation Parameters
Modify the `VehicleSimulator` class to create different driving scenarios:
```python
self.engine_temp = max(70, min(130, self.engine_temp))  # Min/Max range
```

---

## 🔧 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'matplotlib'"
**Solution:**
```bash
pip install matplotlib
```

### Issue: Application is slow or freezing
**Solution:**
- Close other applications to free up resources
- The monitoring runs in a background thread, so it shouldn't freeze the UI

### Issue: Database file keeps growing
**Solution:**
- The database stores all historical data. To reset:
  ```bash
  rm smartdrive.db  # macOS/Linux
  del smartdrive.db  # Windows
  ```
- Restart the application to create a fresh database

### Issue: Charts not updating
**Solution:**
- Wait 5+ seconds after starting monitoring
- Charts update every 5 seconds
- Ensure at least 2-3 data points exist

---

## 📈 Monitoring Tips

1. **Start simple**: Just watch how parameters change normally
2. **Experiment**: Let it run for 2-3 minutes to see different scenarios
3. **Check history**: Use the alerts panel to screen recorded issues
4. **Verify predictions**: See if the predicted faults make sense based on parameters
5. **Export data**: Use the database for further analysis

---

## 🎓 Learning from SmartDrive

This application teaches:

- **Rule-Based AI**: How systems make decisions without machine learning
- **Real-time Monitoring**: Continuous data collection and analysis
- **Multi-threaded Design**: Background processing with UI responsiveness
- **Database Design**: Storing and retrieving structured data
- **Data Visualization**: Making data understandable through charts

---

## 🆘 Need Help?

1. Check the **README.md** for detailed documentation
2. Review **System Architecture** section in README
3. Examine the Python code comments in `smartdrive.py`
4. Try adjusting parameters in the code for custom scenarios

---

## 🚀 Next Steps

After you're comfortable with the basic application:

1. **Experiment with scenarios**:
   - Modify simulator to create extreme conditions
   - Test how the AI responds

2. **Analyze real data**:
   - Run monitoring for 10+ minutes
   - Export and analyze patterns

3. **Extend functionality**:
   - Add more fault types
   - Implement ML-based predictions
   - Create mobile app integration

4. **Contribute**:
   - Add new features
   - Improve recommendations
   - Enhance visualizations

---

**Happy Monitoring! 🚗 Safe Driving!** 🛡️
