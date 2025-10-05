"""
Data fetching routes for weather and satellite data
"""
# data_routes.py

import sys
import os

# Get the path to the backend directory
backend_dir = os.path.join(os.path.dirname(__file__), '..')
# Add the backend directory to the system path
sys.path.append(backend_dir)

# Now your import should work
from data_fetch.nasa_power_api import NASAPowerAPI
# ... rest of your code
from flask import Blueprint, request, jsonify
from data_fetch.nasa_power_api import NASAPowerAPI
from data_fetch.satellite_data import SatelliteDataFetcher
import logging

data_bp = Blueprint('data', __name__)
logger = logging.getLogger(__name__)

@data_bp.route('/weather', methods=['GET'])
def get_weather_data():
    """Fetch weather data for a specific location"""
    try:
        latitude = request.args.get('latitude', type=float)
        longitude = request.args.get('longitude', type=float)
        start_date = request.args.get('start_date', '2024-01-01')
        end_date = request.args.get('end_date')
        
        if not latitude or not longitude:
            return jsonify({
                'success': False,
                'error': 'Latitude and longitude are required'
            }), 400
        
        # Initialize NASA POWER API
        nasa_api = NASAPowerAPI()
        weather_data = nasa_api.get_weather_data(latitude, longitude, start_date, end_date)
        
        return jsonify({
            'success': True,
            'data': weather_data,
            'coordinates': {'latitude': latitude, 'longitude': longitude},
            'date_range': {'start': start_date, 'end': end_date}
        })
        
    except Exception as e:
        logger.error(f"Error fetching weather data: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@data_bp.route('/satellite', methods=['GET'])
def get_satellite_data():
    """Fetch satellite data (NDVI, soil moisture, precipitation)"""
    try:
        latitude = request.args.get('latitude', type=float)
        longitude = request.args.get('longitude', type=float)
        start_date = request.args.get('start_date', '2024-01-01')
        end_date = request.args.get('end_date')
        data_type = request.args.get('type', 'all')  # 'ndvi', 'soil_moisture', 'precipitation', 'all'
        
        if not latitude or not longitude:
            return jsonify({
                'success': False,
                'error': 'Latitude and longitude are required'
            }), 400
        
        # Initialize satellite data fetcher
        fetcher = SatelliteDataFetcher()
        
        if data_type == 'all':
            data = fetcher.get_comprehensive_data(latitude, longitude, start_date, end_date)
        elif data_type == 'ndvi':
            data = fetcher.get_modis_ndvi(latitude, longitude, start_date, end_date)
        elif data_type == 'soil_moisture':
            data = fetcher.get_smap_soil_moisture(latitude, longitude, start_date, end_date)
        elif data_type == 'precipitation':
            data = fetcher.get_gpm_precipitation(latitude, longitude, start_date, end_date)
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid data type. Use: ndvi, soil_moisture, precipitation, or all'
            }), 400
        
        return jsonify(data)
        
    except Exception as e:
        logger.error(f"Error fetching satellite data: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@data_bp.route('/irrigation-analysis', methods=['GET'])
def get_irrigation_analysis():
    """Get comprehensive irrigation analysis for a farm"""
    try:
        latitude = request.args.get('latitude', type=float)
        longitude = request.args.get('longitude', type=float)
        soil_moisture = request.args.get('soil_moisture', type=float)
        
        if not latitude or not longitude:
            return jsonify({
                'success': False,
                'error': 'Latitude and longitude are required'
            }), 400
        
        # Initialize APIs
        nasa_api = NASAPowerAPI()
        fetcher = SatelliteDataFetcher()
        
        # Get irrigation recommendation from NASA POWER
        irrigation_need = nasa_api.calculate_irrigation_need(latitude, longitude, soil_moisture)
        
        # Get recent satellite data
        end_date = '2024-01-15'  # Current date
        start_date = '2024-01-01'  # 2 weeks ago
        
        satellite_data = fetcher.get_comprehensive_data(latitude, longitude, start_date, end_date)
        
        # Combine analysis
        analysis = {
            'coordinates': {'latitude': latitude, 'longitude': longitude},
            'irrigation_recommendation': irrigation_need,
            'satellite_data': satellite_data,
            'analysis_date': '2024-01-15T00:00:00Z'
        }
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
        
    except Exception as e:
        logger.error(f"Error getting irrigation analysis: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@data_bp.route('/forecast', methods=['GET'])
def get_weather_forecast():
    """Get weather forecast for irrigation planning"""
    try:
        latitude = request.args.get('latitude', type=float)
        longitude = request.args.get('longitude', type=float)
        days_ahead = request.args.get('days', 7, type=int)
        
        if not latitude or not longitude:
            return jsonify({
                'success': False,
                'error': 'Latitude and longitude are required'
            }), 400
        
        # Initialize NASA POWER API
        nasa_api = NASAPowerAPI()
        forecast_data = nasa_api.get_forecast_data(latitude, longitude, days_ahead)
        
        return jsonify({
            'success': True,
            'forecast': forecast_data,
            'coordinates': {'latitude': latitude, 'longitude': longitude},
            'forecast_days': days_ahead
        })
        
    except Exception as e:
        logger.error(f"Error getting weather forecast: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
