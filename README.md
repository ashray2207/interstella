# KhetSetGo - Smart Crop & Water Advisor

A comprehensive smart farming system that helps farmers make data-driven irrigation decisions using satellite data, weather APIs, and machine learning analytics.

## 🌟 Features

- **Smart Irrigation Recommendations**: Get precise irrigation advice based on soil moisture, weather forecasts, and crop health
- **Multi-Source Data Integration**: NASA POWER API, MODIS NDVI, SMAP Soil Moisture, GPM Precipitation
- **Interactive Dashboard**: Visualize farm data with maps, charts, and trend analysis
- **Farmer-Friendly Notifications**: SMS and voice alerts in local language
- **Farm Boundary Support**: Upload GeoJSON boundaries or drop pins on map

## 🚀 Quick Start

### Super Quick Setup (5 minutes)
```bash
# 1. Clone the repository
git clone <repository-url>
cd KhetSetGo

# 2. Run automated setup
python setup.py

# 3. Start the application
python run_app.py
```

**That's it!** Access your app at http://localhost:3000

### Manual Setup

#### Prerequisites
- Python 3.8+
- Node.js 16+

#### Installation Steps

1. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python app.py
   ```

2. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm start
   ```

3. **Environment Variables**
   ```bash
   cp env.example .env
   # Edit .env with your API keys
   ```

### Detailed Installation
For complete step-by-step instructions, see [INSTALLATION.md](INSTALLATION.md)

## 📁 Project Structure

```
KhetSetGo/
├── backend/                 # Flask/FastAPI backend
│   ├── app.py              # Main application
│   ├── data_fetch/         # Data fetching modules
│   ├── analytics/          # Data processing engine
│   ├── recommendations/    # Recommendation generation
│   └── notifications/      # SMS/Voice notifications
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/         # Page components
│   │   └── utils/         # Utility functions
│   └── public/
├── data/                   # Data storage
└── docs/                   # Documentation
```

## 🔧 API Endpoints

- `GET /api/farm/location` - Get farm location data
- `POST /api/farm/boundary` - Upload farm boundary
- `GET /api/data/weather` - Fetch weather data
- `GET /api/recommendations` - Get irrigation recommendations
- `POST /api/notifications/sms` - Send SMS notification

## 🌐 Data Sources

- **NASA POWER API**: Temperature and ET0 data
- **MODIS**: NDVI crop health data
- **SMAP**: Soil moisture data
- **GPM/IMERG**: Precipitation data

## 📱 Supported Languages

- Hindi (Primary)
- English
- Local regional languages (planned)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions, please open an issue or contact the development team.
