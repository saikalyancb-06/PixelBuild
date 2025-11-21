# ⚡ Quick Start Guide (15 Minutes)

Get the Fake App Detection System running in 15 minutes!

## Prerequisites
- Python 3.9+
- Node.js 16+
- Git

---

## Step 1: Setup Backend (5 minutes)

```powershell
# Navigate to project
cd PixelBuild

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Install dependencies (this may take a few minutes)
pip install -r requirements.txt

# Create environment file
copy .env.example .env

# Initialize database
python backend\init_db.py

# Load demo data
python data\create_demo_data.py
```

---

## Step 2: Start Backend (1 minute)

```powershell
# Start FastAPI server
python backend\main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**Keep this terminal running!**

---

## Step 3: Setup Frontend (3 minutes)

Open a **new terminal**:

```powershell
cd PixelBuild\frontend

# Install dependencies
npm install

# Start development server
npm start
```

The browser should automatically open to http://localhost:3000

---

## Step 4: Explore the Dashboard (5 minutes)

### Dashboard Page
- View overall metrics
- See detection statistics
- Check performance graphs

### Detections Page
- Browse detected fake apps
- View risk levels (CRITICAL/HIGH/MEDIUM/LOW)
- Confirm detections
- Create takedown requests

### Brands Page
- Add new brands for protection
- View protected brands

### Scans Page
- Create new scan jobs
- Monitor scan progress
- View scan results

---

## Testing the System

### Test 1: View Existing Detections
1. Go to **Detections** page
2. You should see 10 fake apps detected
3. Click on any detection to view details

### Test 2: Check Metrics
1. Go to **Dashboard**
2. See metrics:
   - 10,000 apps scanned
   - 127 fake apps detected
   - 99.99% detection rate
   - 94% takedown success

### Test 3: Manual Detection Test

Open a **new terminal**:

```powershell
cd PixelBuild
.\venv\Scripts\activate

# Run a quick test
python -c "
from ml_models.text_similarity.detector import TextSimilarityDetector

detector = TextSimilarityDetector()
score, reasons = detector.compare_names('PayPal', 'PayPaI')

print(f'Similarity Score: {score:.2%}')
print('Reasons:')
for reason in reasons:
    print(f'  - {reason}')
"
```

You should see high similarity (>85%) indicating a potential fake!

---

## Troubleshooting

### Backend won't start

**Error:** `ModuleNotFoundError: No module named 'fastapi'`
```powershell
# Make sure virtual environment is activated
.\venv\Scripts\activate

# Reinstall requirements
pip install -r requirements.txt
```

**Error:** `Database connection failed`
```powershell
# Use SQLite (simpler for demo)
# Edit .env file:
DATABASE_URL=sqlite:///./fakeapp.db

# Recreate database
python backend\init_db.py
python data\create_demo_data.py
```

### Frontend won't start

**Error:** `npm ERR! code ENOENT`
```powershell
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Error:** `Port 3000 already in use`
```powershell
# Kill the process using port 3000
netstat -ano | findstr :3000
# Note the PID and kill it:
taskkill /PID <PID> /F

# Or use a different port
$env:PORT=3001; npm start
```

### ML Models Not Working

**Error:** `No module named 'torch'`
```powershell
# Install PyTorch separately (CPU version for demo)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

---

## Quick Demo Script

Once everything is running:

### 1. Show Dashboard (30 seconds)
- Navigate to http://localhost:3000
- Point out key metrics
- Show the charts

### 2. Show Detections (1 minute)
- Go to Detections page
- Filter by confidence (try 90%+)
- Click on a CRITICAL risk detection
- Show the detection reasons

### 3. Create Takedown (30 seconds)
- Select a detection
- Click "Takedown"
- Show confirmation

### 4. Show Brands (30 seconds)
- Navigate to Brands page
- Show protected brands
- Demonstrate adding a new brand

**Total Demo Time: 3 minutes**

---

## Next Steps

### For Hackathon Presentation:
1. Read `PITCH_SCRIPT.md` for speaking points
2. Review `HACKATHON_GUIDE.md` for detailed info
3. Practice the demo 3-5 times
4. Prepare backup screenshots/video

### For Further Development:
1. Integrate real Google Play Store API
2. Add email notifications
3. Implement real certificate analysis
4. Deploy to cloud (AWS/Azure/GCP)

---

## API Endpoints

Backend API is available at http://localhost:8000

**Key Endpoints:**
- `GET /api/brands` - List all protected brands
- `POST /api/scans` - Create a new scan job
- `GET /api/detections?min_confidence=0.9` - Get detections
- `POST /api/takedowns` - Create takedown request
- `GET /api/metrics` - Get overall metrics

**API Documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Architecture Overview

```
┌─────────────────┐
│   Frontend      │  React + Material-UI
│  (Port 3000)    │  Dashboard, Charts, Tables
└────────┬────────┘
         │ HTTP/REST
         ▼
┌─────────────────┐
│   Backend API   │  FastAPI + Python
│  (Port 8000)    │  Business Logic, DB Access
└────────┬────────┘
         │
         ├─────────────────┐
         │                 │
         ▼                 ▼
┌─────────────┐   ┌────────────────┐
│  Database   │   │  ML Detectors  │
│  (SQLite)   │   │  - Icon CNN    │
│             │   │  - Text NLP    │
│  - Brands   │   │  - Cert Check  │
│  - Apps     │   │  - Review AI   │
│  - Detections│  └────────────────┘
└─────────────┘
```

---

## Success Checklist

Before you present:

- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Can see dashboard with metrics
- [ ] Can view detections
- [ ] Demo data is loaded
- [ ] You've practiced the demo
- [ ] Backup plan ready (screenshots/video)

---

## Support

If you encounter issues:

1. Check the error messages carefully
2. Review the Troubleshooting section above
3. Check `logs/app.log` for backend errors
4. Browser console for frontend errors
5. Google the specific error message

---

**You're ready to go! 🚀**

Good luck with your hackathon! Remember: Focus on the demo, tell a compelling story, and show the real-world impact.
