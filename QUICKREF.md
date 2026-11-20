# 🚗 SmartDrive Guardian AI - Quick Reference Card

## 🚀 START HERE (Choose Your Path)

### ⚡ Fastest Start (2 min)
```
Windows: Double-click run.bat
macOS/Linux: bash run.sh
Then: Click "▶ Start Monitoring"
```

### 📖 Learn First (20 min)
```
1. Read: PROJECT_SUMMARY.md (overview)
2. Read: QUICKSTART.md (setup guide)
3. Run: python smartdrive.py
```

### 👨‍💻 Deep Dive (2 hours)
```
1. Read: README.md (complete guide)
2. Study: TECHNICAL.md (architecture)
3. Review: smartdrive.py (code)
4. Experiment: Modify & run
```

---

## 📋 What This Does

**SmartDrive Guardian AI** is an intelligent vehicle monitoring system that:
- 🔍 Monitors 6 vehicle parameters in real-time
- 🧠 Uses AI to detect 6 types of mechanical faults
- ⚠️ Classifies severity (Safe/Warning/Critical)
- 💡 Recommends specific actions
- 💾 Persists all data to database
- 📊 Visualizes trends in real-time

---

## ⚙️ Core Features

| Feature | Details |
|---------|---------|
| **Parameters** | Temp, RPM, Speed, Oil, Brakes, Fuel |
| **Faults** | Cooling, Lubrication, Brakes, Transmission, Fuel, Radiator |
| **Severity** | Safe (🟢) / Warning (🟠) / Critical (🔴) |
| **Database** | SQLite with 3 tables |
| **Interfaces** | GUI (Tkinter) + CLI |
| **Visualizations** | Real-time trend charts |

---

## 📁 Key Files

```
smartdrive.py        → GUI app (run this!)
smartdrive_cli.py    → CLI version
requirements.txt     → Dependencies
run.bat / run.sh     → Launchers
README.md            → Full guide
TECHNICAL.md         → Deep dive
```

---

## 🎮 Using the GUI

```
1. Click "▶ Start Monitoring" → Begins real-time monitoring
2. Watch Parameters → Update every second
3. View Diagnostics → Shows predicted fault
4. Check Severity → Color-coded urgency level
5. Read Recommendations → Context-specific advice
6. See Trends → Charts after ~5 seconds
7. Click "⏹ Stop Monitoring" → Stop monitoring
```

---

## ⌨️ Using CLI

```bash
# Monitor for 60 seconds
python smartdrive_cli.py --duration 60

# Show last 10 diagnostics
python smartdrive_cli.py --history 10

# Monitor for 5 minutes
python smartdrive_cli.py --duration 300
```

---

## 🔧 Quick Setup

### Windows (Easiest)
```
1. Download files
2. Double-click run.bat ← That's it!
```

### macOS/Linux
```bash
bash run.sh
```

### Manual (All Platforms)
```bash
pip install matplotlib
python smartdrive.py
```

---

## 📊 Fault Types

| Fault | Trigger |
|-------|---------|
| **Cooling System Failure** | High temp + High RPM |
| **Engine Lubrication Failure** | Low oil + High temp |
| **Brake System Issue** | High brake response |
| **Transmission Problem** | Very high RPM |
| **Fuel System Warning** | Low fuel |
| **Radiator Blockage** | Very high temp |

---

## 🎯 Severity Levels

```
🟢 SAFE
   - No issues
   - Continue driving
   - Regular maintenance ok

🟠 WARNING  
   - Potential problem detected
   - Check system soon
   - Schedule maintenance

🔴 CRITICAL
   - Stop immediately
   - Major issue detected
   - Emergency action needed
```

---

## 📚 Documentation Map

```
START HERE ─────→ PROJECT_SUMMARY.md (5 min)
     ↓
   SETUP ───────→ QUICKSTART.md (10 min)
     ↓
   USAGE ───────→ README.md (30 min)
     ↓
   LEARN ───────→ TECHNICAL.md (60 min)
     ↓
   DEPLOY ──────→ DEPLOYMENT.md (60 min)
```

---

## 🐛 Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| Won't start | Check Python 3.7+ installed |
| "No matplotlib" | `pip install matplotlib` |
| No data updating | Wait 5 sec, then check |
| Database error | Delete smartdrive.db & restart |
| GUI frozen | It's ok, monitoring runs in background |

---

## 📈 Database Queries

```bash
# View recent parameters
sqlite3 smartdrive.db "SELECT * FROM vehicle_parameters LIMIT 5;"

# View diagnostics
sqlite3 smartdrive.db "SELECT * FROM diagnostics LIMIT 5;"

# View critical alerts
sqlite3 smartdrive.db "SELECT * FROM alerts WHERE severity='Critical';"

# Get statistics
sqlite3 smartdrive.db "SELECT COUNT(*) FROM vehicle_parameters;"
```

---

## 🔍 What Gets Saved?

**vehicle_parameters**
- Engine temp, RPM, speed, oil, brakes, fuel
- One record per second

**diagnostics**
- Predicted fault, confidence, severity
- Fault scores, recommendations

**alerts**
- Alert severity and message
- Timestamp of each alert

---

## 💻 System Requirements

| Item | Requirement |
|------|-------------|
| **OS** | Windows / macOS / Linux |
| **Python** | 3.7 or higher |
| **RAM** | 512 MB minimum |
| **Disk** | 50 MB free |
| **Display** | 1024×768 for GUI |

---

## 🚗 Vehicle Parameters Monitored

| Parameter | Range | What It Means |
|-----------|-------|--------------|
| **Temp** | 70-130°C | Engine health |
| **RPM** | 800-6000 | Engine stress |
| **Speed** | 0-200 km/h | Driving speed |
| **Oil** | 0-100% | Lubrication |
| **Brakes** | 0.1-1.0 sec | Brake performance |
| **Fuel** | 0-100% | Fuel remaining |

---

## 🎓 Learning Path by Role

### Student
```
1. PROJECT_SUMMARY.md - Understand concept
2. README.md - Learn features  
3. smartdrive.py - Read code
4. TECHNICAL.md - Understand theory
5. Modify code & experiment
```

### Developer
```
1. README.md - Feature overview
2. TECHNICAL.md - Architecture
3. smartdrive.py - Implementation
4. Smart.py smartdrive_cli.py - CLI version
5. Plan extensions
```

### Manager
```
1. PROJECT_SUMMARY.md - Project overview
2. README.md - Feature checklist
3. DEPLOYMENT.md - Deployment info
4. MANIFEST.md - Quality verification
```

---

## 🔗 All Documents

| Doc | Purpose | Time |
|-----|---------|------|
| INDEX.md | Navigate docs | 10 min |
| PROJECT_SUMMARY.md | Overview | 15 min |
| QUICKSTART.md | Quick setup | 10 min |
| README.md | Complete guide | 30 min |
| TECHNICAL.md | Architecture | 60 min |
| DEPLOYMENT.md | Testing/Deploy | 60 min |
| MANIFEST.md | Verification | 10 min |
| This card | Quick ref | 2 min |

---

## ✅ Verification Checklist

- [ ] Download all files
- [ ] Verify Python 3.7+ installed
- [ ] Run: `pip install -r requirements.txt`
- [ ] Run: `python smartdrive.py` (or double-click run.bat)
- [ ] Click "▶ Start Monitoring"
- [ ] See parameters update
- [ ] Wait 5+ seconds for charts
- [ ] Read recommendations
- [ ] Stop monitoring
- [ ] Check database created

---

## 🎯 Common Tasks

```bash
# Setup
pip install -r requirements.txt

# Run GUI
python smartdrive.py

# Run CLI (60 seconds)
python smartdrive_cli.py --duration 60

# Check history
python smartdrive_cli.py --history 20

# Query database
sqlite3 smartdrive.db ".schema"

# Clear database
rm smartdrive.db  # macOS/Linux
del smartdrive.db # Windows
```

---

## 🌐 Technologies Used

- **Python 3.7+** - Core language
- **Tkinter** - GUI framework (built-in)
- **SQLite3** - Database (built-in)
- **Matplotlib** - Visualization
- **Threading** - Background monitoring
- **JSON** - Data serialization

---

## 🏆 Project Highlights

✨ **Complete** - All features implemented  
✨ **Documented** - 2500+ lines of docs  
✨ **Tested** - Testing guide provided  
✨ **Ready** - Production-grade code  
✨ **Extensible** - Easy to modify & enhance  

---

## 📞 Need Help?

```
Quick answers → Check QUICKSTART.md
Feature details → Read README.md
Architecture → Study TECHNICAL.md
Issues → See DEPLOYMENT.md
Navigate all → Use INDEX.md
```

---

## 🎬 Ready? Let's Go!

### Next Steps:

**Option A: Just Run It (2 min)**
```
Windows: Double-click run.bat
Others: bash run.sh
Click Start → Watch it work!
```

**Option B: Learn First (20 min)**
```
1. Read PROJECT_SUMMARY.md
2. Read QUICKSTART.md
3. Run application
4. Explore features
```

**Option C: Deep Dive (2 hours)**
```
1. Read README.md
2. Study TECHNICAL.md
3. Review source code
4. Modify & experiment
```

---

## 🚀 You're Ready!

All files present ✅
Documentation complete ✅
Ready to run ✅

**Choose an option above and get started!**

---

**SmartDrive Guardian AI - Quick Reference**  
*Real-Time Vehicle Monitoring with Predictive AI*

🚗 Happy driving! 🛡️
