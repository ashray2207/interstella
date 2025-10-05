#!/usr/bin/env python3
"""
KhetSetGo Application Launcher
Starts both backend and frontend servers
"""

import subprocess
import sys
import os
import time
import signal
from threading import Thread

def run_backend():
    """Run the Flask backend server"""
    os.chdir('backend')
    try:
        subprocess.run([sys.executable, 'app.py'], check=True)
    except KeyboardInterrupt:
        print("Backend server stopped")
    except Exception as e:
        print(f"Backend error: {e}")

def run_frontend():
    """Run the React frontend server"""
    os.chdir('frontend')
    try:
        subprocess.run(['npm', 'start'], check=True)
    except KeyboardInterrupt:
        print("Frontend server stopped")
    except Exception as e:
        print(f"Frontend error: {e}")

def main():
    """Main function to start both servers"""
    print("🌱 Starting KhetSetGo - Smart Crop & Water Advisor")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists('backend') or not os.path.exists('frontend'):
        print("❌ Error: Please run this script from the project root directory")
        print("   Expected structure:")
        print("   KhetSetGo/")
        print("   ├── backend/")
        print("   ├── frontend/")
        print("   └── run_app.py")
        sys.exit(1)
    
    # Start backend server
    print("🚀 Starting backend server on http://localhost:5000")
    backend_thread = Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    # Wait a moment for backend to start
    time.sleep(3)
    
    # Start frontend server
    print("🎨 Starting frontend server on http://localhost:3000")
    frontend_thread = Thread(target=run_frontend, daemon=True)
    frontend_thread.start()
    
    print("\n✅ Servers started successfully!")
    print("📱 Frontend: http://localhost:3000")
    print("🔧 Backend API: http://localhost:5000")
    print("\nPress Ctrl+C to stop both servers")
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down servers...")
        print("Thank you for using KhetSetGo!")

if __name__ == "__main__":
    main()
