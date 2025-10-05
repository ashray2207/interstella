#!/usr/bin/env python3
"""
KhetSetGo Automated Setup Script
This script automates the installation process for the KhetSetGo smart farming system.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(command, cwd=None, shell=True):
    """Run a command and return success status"""
    try:
        result = subprocess.run(command, shell=shell, cwd=cwd, 
                              capture_output=True, text=True)
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr
    except Exception as e:
        return False, str(e)

def check_python_version():
    """Check if Python 3.8+ is installed"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is installed")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is installed")
        print("   Please install Python 3.8 or higher")
        return False

def check_node_version():
    """Check if Node.js 16+ is installed"""
    print("📦 Checking Node.js version...")
    success, output = run_command("node --version")
    if success:
        version_str = output.strip().replace('v', '')
        version_parts = version_str.split('.')
        major = int(version_parts[0])
        if major >= 16:
            print(f"✅ Node.js {version_str} is installed")
            return True
        else:
            print(f"❌ Node.js {version_str} is installed")
            print("   Please install Node.js 16 or higher")
            return False
    else:
        print("❌ Node.js is not installed")
        print("   Please install Node.js from https://nodejs.org/")
        return False

def create_virtual_environment():
    """Create Python virtual environment"""
    print("🔧 Creating Python virtual environment...")
    success, output = run_command(f"{sys.executable} -m venv venv")
    if success:
        print("✅ Virtual environment created successfully")
        return True
    else:
        print(f"❌ Failed to create virtual environment: {output}")
        return False

def install_python_dependencies():
    """Install Python dependencies"""
    print("📚 Installing Python dependencies...")
    
    # Determine the correct pip command based on OS
    if platform.system() == "Windows":
        pip_cmd = "venv\\Scripts\\pip"
    else:
        pip_cmd = "venv/bin/pip"
    
    # Upgrade pip first
    success, _ = run_command(f"python.exe -m pip install --upgrade pip")
    if not success:
        print("⚠️  Warning: Could not upgrade pip")
    
    # Install requirements
    success, output = run_command(f" {pip_cmd} install -r backend/requirements.txt")
    if success:
        print("✅ Python dependencies installed successfully")
        return True
    else:
        print(f"❌ Failed to install Python dependencies: {output}")
        return False

def install_node_dependencies():
    """Install Node.js dependencies"""
    print("📦 Installing Node.js dependencies...")
    success, output = run_command("npm install", cwd="frontend")
    if success:
        print("✅ Node.js dependencies installed successfully")
        return True
    else:
        print(f"❌ Failed to install Node.js dependencies: {output}")
        return False

def setup_environment_files():
    """Setup environment configuration files"""
    print("⚙️  Setting up environment files...")
    
    # Backend .env file
    backend_env_content = """# Database Configuration
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
SECRET_KEY=dev-secret-key-change-in-production

# CORS Configuration
FRONTEND_URL=http://localhost:3000
"""
    
    with open("backend/.env", "w") as f:
        f.write(backend_env_content)
    
    # Frontend .env file
    frontend_env_content = "REACT_APP_API_URL=http://localhost:5000/api\n"
    
    with open("frontend/.env", "w") as f:
        f.write(frontend_env_content)
    
    print("✅ Environment files created successfully")
    print("📝 Please edit backend/.env with your API keys when ready")
    return True

def initialize_database():
    """Initialize the database"""
    print("🗄️  Initializing database...")
    
    # Determine the correct python command based on OS
    if platform.system() == "Windows":
        python_cmd = "venv\\Scripts\\python"
    else:
        python_cmd = "venv/bin/python"
    
    # Run a quick database initialization
    success, output = run_command(f"{python_cmd} -c \"from backend.app import app, db; app.app_context().push(); db.create_all(); print('Database initialized')\"")
    if success:
        print("✅ Database initialized successfully")
        return True
    else:
        print(f"❌ Failed to initialize database: {output}")
        return False

def create_directories():
    """Create necessary directories"""
    print("📁 Creating project directories...")
    
    directories = [
        "backend/routes",
        "backend/data_fetch", 
        "backend/analytics",
        "frontend/src/components",
        "frontend/src/context",
        "frontend/public"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Project directories created")
    return True

def main():
    """Main setup function"""
    print("🌱 KhetSetGo Smart Farming System - Automated Setup")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("backend") or not os.path.exists("frontend"):
        print("❌ Error: Please run this script from the KhetSetGo project root directory")
        print("   Expected structure:")
        print("   KhetSetGo/")
        print("   ├── backend/")
        print("   ├── frontend/")
        print("   └── setup.py")
        return False
    
    # Step 1: Check prerequisites
    print("\n🔍 Step 1: Checking Prerequisites")
    if not check_python_version():
        return False
    if not check_node_version():
        return False
    
    # Step 2: Create directories
    print("\n📁 Step 2: Creating Project Structure")
    if not create_directories():
        return False
    
    # Step 3: Setup Python environment
    print("\n🐍 Step 3: Setting up Python Environment")
    if not create_virtual_environment():
        return False
    if not install_python_dependencies():
        return False
    
    # Step 4: Setup Node.js environment
    print("\n📦 Step 4: Setting up Node.js Environment")
    if not install_node_dependencies():
        return False
    
    # Step 5: Setup environment files
    print("\n⚙️  Step 5: Setting up Configuration")
    if not setup_environment_files():
        return False
    
    # Step 6: Initialize database
    print("\n🗄️  Step 6: Initializing Database")
    if not initialize_database():
        return False
    
    # Success!
    print("\n🎉 Setup Complete!")
    print("=" * 60)
    print("✅ All components installed successfully")
    print("\n🚀 Next Steps:")
    print("1. Edit backend/.env with your API keys (optional)")
    print("2. Start the application:")
    print("   python run_app.py")
    print("\n📱 Access Points:")
    print("   Frontend: http://localhost:3000")
    print("   Backend:  http://localhost:5000")
    print("\n📚 Documentation: See INSTALLATION.md for detailed instructions")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🌟 KhetSetGo is ready to help farmers make smart decisions!")
            sys.exit(0)
        else:
            print("\n❌ Setup failed. Please check the errors above.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during setup: {e}")
        sys.exit(1)
