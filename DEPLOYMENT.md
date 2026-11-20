# SmartDrive Guardian AI - Deployment & Testing Guide

## 🚀 Deployment Options

### Option 1: Desktop Application (Windows, macOS, Linux)

#### Windows

1. **Automated Setup:**
   - Double-click `run.bat`
   - Script will handle Python, venv, and dependencies
   - Application launches automatically

2. **Manual Setup:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   python smartdrive.py
   ```

#### macOS/Linux

1. **Using Shell Script:**
   ```bash
   chmod +x run.sh
   ./run.sh
   ```

2. **Manual Setup:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python3 smartdrive.py
   ```

### Option 2: CLI (Server/Headless Environment)

```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run monitoring for 5 minutes
python smartdrive_cli.py --duration 300

# Check diagnostic history
python smartdrive_cli.py --history 20
```

### Option 3: Docker Container (Production)

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY smartdrive_cli.py .
COPY smartdrive.db* .

CMD ["python", "smartdrive_cli.py", "--duration", "3600"]
```

Build and run:
```bash
docker build -t smartdrive-ai .
docker run -v /app/smartdrive.db:/app/smartdrive.db smartdrive-ai
```

---

## ✅ Testing Guide

### 1. Pre-Launch Verification

**Check Python Installation:**
```bash
python --version
# Expected: Python 3.7 or higher
```

**Check Dependencies:**
```bash
pip list | grep matplotlib
# Expected: matplotlib 3.5.0 or higher
```

**Verify File Structure:**
```bash
ls -la smartdrive*.py
ls -la requirements.txt
# Should show both files
```

### 2. Syntax Validation

**Validate Main Application:**
```bash
python -m py_compile smartdrive.py
echo "✓ GUI application syntax OK"
```

**Validate CLI Application:**
```bash
python -m py_compile smartdrive_cli.py
echo "✓ CLI application syntax OK"
```

### 3. Database Testing

**Verify Database Creation:**
```bash
rm smartdrive.db 2>/dev/null  # Clean slate
python -c "from smartdrive import DatabaseManager; db = DatabaseManager(); print('✓ Database created')"
```

**Check Schema:**
```bash
sqlite3 smartdrive.db ".schema"
# Should show 3 tables: vehicle_parameters, diagnostics, alerts
```

### 4. Unit Tests

**Test Vehicle Simulator:**
```python
from smartdrive import VehicleSimulator

sim = VehicleSimulator()
sim.simulate_driving_scenario()
state = sim.get_current_state()

assert 70 <= state['engine_temp'] <= 130, "Temp out of range"
assert 800 <= state['rpm'] <= 6000, "RPM out of range"
assert 0 <= state['speed'] <= 200, "Speed out of range"
print("✓ Vehicle Simulator tests passed")
```

**Test Fault Detection:**
```python
from smartdrive import FaultDetectionEngine

engine = FaultDetectionEngine()
params = {
    'engine_temp': 120,
    'rpm': 5000,
    'speed': 100,
    'oil_level': 15,
    'brake_response': 0.5,
    'fuel_level': 50
}

result = engine.predict_fault(params)
assert 'fault' in result, "Fault key missing"
assert 0 <= result['confidence'] <= 100, "Confidence out of range"

severity = engine.classify_severity(params, result)
assert severity in ['Safe', 'Warning', 'Critical'], "Invalid severity"

recommendations = engine.generate_recommendations(params, result['fault'], severity)
assert isinstance(recommendations, list), "Recommendations not a list"
print("✓ Fault Detection Engine tests passed")
```

**Test Database:**
```python
from smartdrive import DatabaseManager

db = DatabaseManager('test.db')
test_params = {
    'engine_temp': 95.5,
    'rpm': 2500,
    'speed': 60,
    'oil_level': 85.0,
    'brake_response': 0.3,
    'fuel_level': 75.0
}

db.save_vehicle_parameters(test_params)
recent = db.get_recent_parameters(1)
assert len(recent) >= 1, "Failed to save/retrieve"
print("✓ Database Manager tests passed")
```

### 5. Integration Test (CLI Mode)

**Run 30-second monitoring:**
```bash
python smartdrive_cli.py --duration 30
# Should output real-time diagnostics without errors
```

**Verify database population:**
```bash
sqlite3 smartdrive.db "SELECT COUNT(*) FROM vehicle_parameters;"
# Should show ~30 records (1 per second)

sqlite3 smartdrive.db "SELECT COUNT(*) FROM diagnostics;"
# Should show ~30 records
```

### 6. Integration Test (GUI Mode - Manual)

1. **Launch application:**
   ```bash
   python smartdrive.py
   ```

2. **Verify GUI elements:**
   - ✅ Control panel visible (Start/Stop buttons)
   - ✅ Parameter panel shows all 6 metrics
   - ✅ Diagnostics section present
   - ✅ Trend chart area visible
   - ✅ Alerts panel visible

3. **Start monitoring:**
   - Click "▶ Start Monitoring"
   - ✅ Status changes to "Monitoring Active"
   - ✅ Stop button becomes enabled

4. **Verify data flow (5-10 seconds):**
   - ✅ Parameters update (numbers change)
   - ✅ Fault prediction appears
   - ✅ Recommendations populate
   - ✅ Chart updates (after ~5 seconds)

5. **Test severity levels:**
   - Run for 1-2 minutes
   - ✅ See severity change from Safe → Warning
   - ✅ See color-coded severity level

6. **Test alerts:**
   - ✅ Warnings appear in alerts panel
   - ✅ Timestamps correct
   - ✅ Can clear history with button

### 7. Performance Testing

**Load Test - GUI:**
```python
# Run for 5 minutes, measure resource usage
import psutil
import smartdrive

# Monitor during GUI execution
# Expected: <10% CPU, <100MB RAM
```

**Load Test - CLI:**
```bash
# Run for 1 hour
time python smartdrive_cli.py --duration 3600
# Should complete without memory issues
```

**Database Growth:**
```bash
# Check database size after 1 hour
du -h smartdrive.db
# Expected: <1 MB growth for 1-hour run
```

### 8. Error Recovery Testing

**Test Missing Dependencies:**
```bash
# Temporarily hide matplotlib
mv /path/to/matplotlib.py /path/to/matplotlib.py.bak

python smartdrive.py
# Should show clear error about missing matplotlib
```

**Test Database Corruption:**
```bash
# Corrupt database
echo "corrupted" > smartdrive.db

python smartdrive.py
# Should recreate database or show clear error
```

**Test Keyboard Interrupt:**
```bash
# CLI mode
python smartdrive_cli.py --duration 300
# Press Ctrl+C at 10 seconds
# Should gracefully exit with summary
```

---

## 📊 Test Results Template

### System Configuration
- **OS**: Windows/macOS/Linux
- **Python Version**: 3.x.x
- **Matplotlib Version**: x.x.x
- **Database**: SQLite3

### Test Execution

| Test | Status | Notes |
|------|--------|-------|
| Syntax Check | ✓ PASS | No errors |
| Database Creation | ✓ PASS | Tables created |
| Simulator | ✓ PASS | Values in range |
| Fault Engine | ✓ PASS | Predictions valid |
| GUI Launch | ✓ PASS | Window appears |
| Data Flow | ✓ PASS | Updates visible |
| Alerts | ✓ PASS | Display correct |
| Performance | ✓ PASS | CPU < 10% |

### Issues Found
- None

### Recommendations
- Application ready for production use

---

## 🐛 Troubleshooting Common Issues

### Issue: "No module named 'matplotlib'"

**Diagnosis:**
```bash
pip list | grep matplotlib
```

**Solution:**
```bash
pip install matplotlib>=3.5.0
```

**Verification:**
```bash
python -c "import matplotlib; print(matplotlib.__version__)"
```

### Issue: "sqlite3.OperationalError: database is locked"

**Cause:** Multiple processes accessing database

**Solution:**
```bash
# Kill existing Python processes
pkill -f smartdrive.py

# Remove lock files (if any)
rm smartdrive.db-journal 2>/dev/null

# Restart application
python smartdrive.py
```

### Issue: GUI window appears but freezes

**Cause:** Event loop blocked by long operation

**Diagnosis:**
```python
# Check in code for blocking operations outside main thread
```

**Solution:**
- Ensure long operations run in background threads (already implemented)
- Verify `after()` is used for UI updates
- Check for infinite loops in main thread

### Issue: Charts not updating

**Cause:** Insufficient data points or matplotlib render issue

**Solution:**
```bash
# Wait at least 10 seconds for trends to accumulate
# Or restart with fresh database:
rm smartdrive.db
python smartdrive.py
```

### Issue: Application crashes on startup

**Diagnosis:**
```bash
python smartdrive.py 2>&1 | head -20
# Shows first 20 lines of error
```

**Solutions:**
- Verify all dependencies installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (need 3.7+)
- Clear pycache: `rm -rf __pycache__`
- Verify file permissions: `ls -la smartdrive.py`

---

## 🔍 Monitoring in Production

### Health Checks

**Every 5 minutes:**
```bash
ps aux | grep smartdrive  # Verify process running
wc -l smartdrive.db      # Check records growing
```

**Every hour:**
```bash
du -h smartdrive.db      # Check database size
sqlite3 smartdrive.db "SELECT COUNT(*) FROM alerts WHERE severity='Critical';"
```

**Every day:**
```bash
# Backup database
cp smartdrive.db smartdrive.db.backup.$(date +%Y%m%d)

# Clear old alerts (>30 days)
sqlite3 smartdrive.db "DELETE FROM alerts WHERE datetime(timestamp) < datetime('now', '-30 days');"
```

### Logging

Create `smartdrive_logging.py`:
```python
import logging
from datetime import datetime

logging.basicConfig(
    filename=f'smartdrive_{datetime.now().date()}.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info("Application started")
logging.error("Critical alert generated")
```

### Alerts

Set up monitoring:
```bash
# Watch for critical errors
tail -f smartdrive.log | grep "Critical"
```

---

## 📈 Expected Performance Metrics

### GUI Mode
- **CPU Usage**: 3-8% (depends on system)
- **Memory Usage**: 80-150 MB
- **Update Latency**: <500ms
- **Database Insert Time**: 10-50ms

### CLI Mode
- **CPU Usage**: 1-3%
- **Memory Usage**: 30-50 MB
- **Update Latency**: <100ms
- **Database Insert Time**: 5-20ms

### Database
- **Record Size**: ~200 bytes per parameter record
- **Growth Rate**: ~100 KB per hour of monitoring
- **Query Performance**: <100ms for 1000 records

---

## 🎯 Success Criteria

Application is production-ready when:

- ✅ All syntax checks pass without errors
- ✅ Database creates and populates correctly
- ✅ GUI launches without crashes
- ✅ Data flows in real-time (updates visible within 1 second)
- ✅ Fault detection activates with realistic data
- ✅ Severity levels change appropriately
- ✅ Recommendations display context-appropriately
- ✅ No memory leaks (sustained <200MB for hours)
- ✅ Database remains responsive (queries <100ms)
- ✅ Graceful shutdown on Ctrl+C

---

## 📞 Support & Escalation

### Level 1: Check Documentation
- README.md - General overview
- QUICKSTART.md - Getting started
- TECHNICAL.md - Architecture & API

### Level 2: Debug
- Enable verbose logging
- Check database integrity
- Review system resources
- Inspect recent diagnostics

### Level 3: Contact Developer
- Review error logs
- Collect system information
- Document reproducible steps

---

**SmartDrive Guardian AI - Ready for Testing and Deployment** 🚀
