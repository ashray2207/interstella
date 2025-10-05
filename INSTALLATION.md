# KhetSetGo - Complete Installation Guide

## 🌱 Smart Crop & Water Advisor - Setup from Scratch

This guide will help you set up the complete KhetSetGo system from scratch, including all dependencies and configuration.

---

## 📋 Prerequisites

Before starting, ensure you have the following installed on your system:

### Required Software
- **Python 3.8+** ([Download here](https://www.python.org/downloads/))
- **Node.js 16+** ([Download here](https://nodejs.org/))
- **Git** ([Download here](https://git-scm.com/downloads))
- **PostgreSQL** (Optional, for production) ([Download here](https://www.postgresql.org/download/))

### Verify Installation
```bash
# Check Python version
python --version
# or
python3 --version

# Check Node.js version
node --version

# Check npm version
npm --version

# Check Git version
git --version
```

---

## 🚀 Step 1: Clone the Repository

```bash
# Clone the repository
git clone <your-repository-url>
cd KhetSetGo

# Or if you're setting up from scratch, create the directory structure
mkdir KhetSetGo
cd KhetSetGo
```

---

## 🐍 Step 2: Backend Setup (Python/Flask)

### 2.1 Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# You should see (venv) in your terminal prompt
```

### 2.2 Install Python Dependencies
```bash
# Navigate to backend directory
cd backend

# Install required packages
pip install -r requirements.txt

# If you encounter issues, try upgrading pip first:
pip install --upgrade pip
```

### 2.3 Environment Configuration
```bash
# Copy environment template
cp env.example .env

# Edit the .env file with your configuration
# You can use any text editor (nano, vim, notepad, etc.)
```

**Edit the `.env` file with your settings:**
```env
# Database Configuration
DATABASE_URL=sqlite:///khetsetgo.db

# NASA POWER API (Get free API key from https://power.larc.nasa.gov/)
NASA_POWER_API_KEY=your_nasa_api_key_here

# Twilio Configuration (SMS Notifications)
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number

# Weather API Keys (Optional)
OPENWEATHER_API_KEY=your_openweather_api_key

# Application Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your_secret_key_here

# CORS Configuration
FRONTEND_URL=http://localhost:3000
```

### 2.4 Initialize Database
```bash
# Run the Flask app to create database tables
python app.py

# The app will create all necessary database tables automatically
# Press Ctrl+C to stop the server after tables are created
```

---

## ⚛️ Step 3: Frontend Setup (React)

### 3.1 Install Node.js Dependencies
```bash
# Navigate to frontend directory (from project root)
cd ../frontend

# Install all dependencies
npm install

# If you encounter permission issues on macOS/Linux:
sudo npm install
```

### 3.2 Frontend Environment Setup
```bash
# Create environment file for React
touch .env

# Add the following content to .env file:
echo "REACT_APP_API_URL=http://localhost:5000/api" > .env
```

---

## 🔧 Step 4: API Keys Setup (Optional but Recommended)

### 4.1 NASA POWER API (Free)
1. Visit [NASA POWER API](https://power.larc.nasa.gov/)
2. Sign up for a free account
3. Get your API key
4. Add it to your backend `.env` file

### 4.2 Twilio (For SMS Notifications)
1. Sign up at [Twilio](https://www.twilio.com/)
2. Get your Account SID and Auth Token
3. Purchase a phone number
4. Add credentials to your backend `.env` file

### 4.3 OpenWeather API (Optional)
1. Sign up at [OpenWeather](https://openweathermap.org/api)
2. Get your free API key
3. Add it to your backend `.env` file

---

## 🎯 Step 5: Run the Application

### Method 1: Using the Launcher Script
```bash
# From the project root directory
python run_app.py
```

This will start both backend and frontend servers automatically.

### Method 2: Manual Start (Two Terminals)

**Terminal 1 - Backend:**
```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Navigate to backend
cd backend

# Start Flask server
python app.py
```

**Terminal 2 - Frontend:**
```bash
# Navigate to frontend
cd frontend

# Start React development server
npm start
```

### 5.1 Access the Application
- **Frontend (Main App):** http://localhost:3000
- **Backend API:** http://localhost:5000
- **API Documentation:** http://localhost:5000/api/status

---

## 🧪 Step 6: Test the Installation

### 6.1 Test Backend API
```bash
# Test health endpoint
curl http://localhost:5000/

# Test API status
curl http://localhost:5000/api/status

# You should see JSON responses
```

### 6.2 Test Frontend
1. Open http://localhost:3000 in your browser
2. You should see the KhetSetGo landing page
3. Navigate through the application:
   - Click "Go to Dashboard"
   - Create a new farm or search for existing ones
   - View the dashboard with sample data

---

## 🐛 Troubleshooting

### Common Issues and Solutions

#### Backend Issues

**1. Import Errors:**
```bash
# Make sure you're in the virtual environment
which python  # Should show path to venv
pip install -r requirements.txt
```

**2. Database Issues:**
```bash
# Delete existing database and recreate
rm backend/khetsetgo.db
python backend/app.py
```

**3. Port Already in Use:**
```bash
# Kill process using port 5000
# On Windows:
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F

# On macOS/Linux:
lsof -ti:5000 | xargs kill -9
```

#### Frontend Issues

**1. npm install fails:**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**2. Port 3000 in use:**
```bash
# Kill process using port 3000
# On Windows:
netstat -ano | findstr :3000
taskkill /PID <PID_NUMBER> /F

# On macOS/Linux:
lsof -ti:3000 | xargs kill -9
```

**3. Build Errors:**
```bash
# Update dependencies
npm update

# If still failing, try:
npm install --legacy-peer-deps
```

---

## 📁 Project Structure

After installation, your project should look like this:

```
KhetSetGo/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── requirements.txt       # Python dependencies
│   ├── models.py             # Database models
│   ├── routes/               # API routes
│   │   ├── farm_routes.py
│   │   ├── data_routes.py
│   │   ├── recommendation_routes.py
│   │   └── notification_routes.py
│   ├── data_fetch/           # Data fetching modules
│   │   ├── nasa_power_api.py
│   │   └── satellite_data.py
│   ├── analytics/            # Analytics and recommendations
│   │   └── recommendation_engine.py
│   └── .env                  # Environment variables
├── frontend/
│   ├── package.json          # Node.js dependencies
│   ├── public/               # Static files
│   ├── src/                  # React source code
│   │   ├── components/       # React components
│   │   ├── context/          # React context
│   │   ├── App.js           # Main App component
│   │   └── index.js         # Entry point
│   └── .env                  # React environment variables
├── run_app.py               # Application launcher
├── README.md                # Project documentation
└── INSTALLATION.md          # This file
```

---

## 🔒 Security Notes

### For Development:
- The current setup uses SQLite database (good for development)
- Default secret keys are provided (change for production)
- CORS is configured for localhost only

### For Production:
1. Use PostgreSQL instead of SQLite
2. Set strong secret keys
3. Configure proper CORS settings
4. Use environment-specific configurations
5. Enable HTTPS
6. Set up proper logging and monitoring

---

## 📞 Support

If you encounter any issues during installation:

1. **Check Prerequisites:** Ensure all required software is installed
2. **Verify Versions:** Make sure Python 3.8+ and Node.js 16+ are installed
3. **Check Logs:** Look at terminal output for error messages
4. **Restart Services:** Try stopping and restarting both servers
5. **Clean Install:** Delete `node_modules` and `venv`, then reinstall

---

## 🎉 Success!

Once everything is running:
- ✅ Backend server running on http://localhost:5000
- ✅ Frontend server running on http://localhost:3000
- ✅ Database initialized with sample data
- ✅ All API endpoints working
- ✅ UI displaying correctly

You're ready to start using KhetSetGo for smart farming decisions! 🌱

---

## 🚀 Next Steps

1. **Create Your First Farm:** Use the farm selection interface
2. **Generate Recommendations:** Let the AI analyze your farm data
3. **Send Notifications:** Test SMS and voice alerts
4. **Explore Analytics:** View weather trends and crop health data
5. **Customize Settings:** Configure crop types and thresholds

Happy Farming! 🚜✨
