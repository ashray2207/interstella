@echo off
echo 🌱 KhetSetGo Smart Farming System - Windows Setup
echo ================================================

echo.
echo 🔍 Checking prerequisites...

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)
echo ✅ Python is installed

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js 16+ from https://nodejs.org/
    pause
    exit /b 1
)
echo ✅ Node.js is installed

echo.
echo 🚀 Starting automated setup...
python setup.py

if errorlevel 1 (
    echo.
    echo ❌ Setup failed. Please check the errors above.
    pause
    exit /b 1
)

echo.
echo 🎉 Setup completed successfully!
echo.
echo 🚀 To start the application, run:
echo    python run_app.py
echo.
echo 📱 Then visit: http://localhost:3000
echo.
pause
