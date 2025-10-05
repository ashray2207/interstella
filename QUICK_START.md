# 🚀 KhetSetGo - Quick Start Guide

Get KhetSetGo running in under 5 minutes!

## ⚡ Super Quick Setup (Automated)

### Option 1: Automated Setup Script
```bash
# Run the automated setup script
python setup.py
```

That's it! The script will:
- ✅ Check all prerequisites
- ✅ Install all dependencies  
- ✅ Configure environment files
- ✅ Initialize the database
- ✅ Set up the complete project structure

### Option 2: Manual Quick Setup

#### 1. Prerequisites Check
```bash
# Check Python (3.8+ required)
python --version

# Check Node.js (16+ required)  
node --version
```

#### 2. Install Dependencies
```bash
# Backend dependencies
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r backend/requirements.txt

# Frontend dependencies
cd frontend
npm install
cd ..
```

#### 3. Start the Application
```bash
# Start both servers
python run_app.py
```

## 🎯 Access Your Application

- **🌐 Main App:** http://localhost:3000
- **🔧 API:** http://localhost:5000

## 🧪 Quick Test

1. Open http://localhost:3000
2. Click "Go to Dashboard" 
3. Create a new farm with these sample coordinates:
   - **Latitude:** 28.6139
   - **Longitude:** 77.2090
   - **District:** Delhi
   - **Crop Type:** Wheat
4. Generate recommendations and explore the dashboard!

## 🆘 Need Help?

- **Full Installation Guide:** See [INSTALLATION.md](INSTALLATION.md)
- **Troubleshooting:** Check the troubleshooting section in INSTALLATION.md
- **API Documentation:** Visit http://localhost:5000/api/status

## 🎉 You're Ready!

Your smart farming irrigation system is now running! 🌱

---

**Happy Farming!** 🚜✨
