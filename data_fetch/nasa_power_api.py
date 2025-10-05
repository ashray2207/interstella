"""
NASA POWER API integration for weather and climate data
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import os
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class NASAPowerAPI:
    """NASA POWER API client for fetching weather and climate data"""
    
    def __init__(self):
        self.base_url = "https://power.larc.nasa.gov/api/temporal/daily"
        self.api_key = os.getenv('NASA_POWER_API_KEY')
    
    def get_weather_data(self, latitude: float, longitude: float, 
                        start_date: str, end_date: str = None) -> Dict:
        """
        Fetch weather data from NASA POWER API
        
        Args:
            latitude: Farm latitude
            longitude: Farm longitude
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format (default: today)
        
        Returns:
            Dictionary containing weather data
        """
        try:
            if not end_date:
                end_date = datetime.now().strftime('%Y-%m-%d')
            
            # NASA POWER API parameters
            params = {
                'parameters': 'T2M,T2M_MAX,T2M_MIN,RH2M,PRECTOTCORR,ET0',
                'community': 'AG',
                'longitude': longitude,
                'latitude': latitude,
                'start': start_date,
                'end': end_date,
                'format': 'JSON'
            }
            
            if self.api_key:
                params['user'] = self.api_key
            
            logger.info(f"Fetching NASA POWER data for {latitude}, {longitude}")
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Process the response
            if 'properties' in data and 'parameter' in data['properties']:
                return self._process_nasa_data(data['properties']['parameter'])
            else:
                logger.error("Invalid NASA POWER API response format")
                return {}
                
        except requests.exceptions.RequestException as e:
            logger.error(f"NASA POWER API request failed: {str(e)}")
            return {}
        except Exception as e:
            logger.error(f"Error processing NASA POWER data: {str(e)}")
            return {}
    
    def _process_nasa_data(self, parameters: Dict) -> Dict:
        """Process NASA POWER API response data"""
        try:
            processed_data = {
                'temperature': {},
                'humidity': {},
                'precipitation': {},
                'et0': {}
            }
            
            # Temperature data (T2M, T2M_MAX, T2M_MIN)
            if 'T2M' in parameters:
                processed_data['temperature']['average'] = parameters['T2M']
            if 'T2M_MAX' in parameters:
                processed_data['temperature']['max'] = parameters['T2M_MAX']
            if 'T2M_MIN' in parameters:
                processed_data['temperature']['min'] = parameters['T2M_MIN']
            
            # Humidity data (RH2M)
            if 'RH2M' in parameters:
                processed_data['humidity'] = parameters['RH2M']
            
            # Precipitation data (PRECTOTCORR)
            if 'PRECTOTCORR' in parameters:
                processed_data['precipitation'] = parameters['PRECTOTCORR']
            
            # Reference evapotranspiration (ET0)
            if 'ET0' in parameters:
                processed_data['et0'] = parameters['ET0']
            
            return processed_data
            
        except Exception as e:
            logger.error(f"Error processing NASA data: {str(e)}")
            return {}
    
    def get_forecast_data(self, latitude: float, longitude: float, 
                         days_ahead: int = 7) -> Dict:
        """
        Get weather forecast data
        
        Args:
            latitude: Farm latitude
            longitude: Farm longitude
            days_ahead: Number of days to forecast (max 15)
        
        Returns:
            Dictionary containing forecast data
        """
        try:
            start_date = datetime.now().strftime('%Y-%m-%d')
            end_date = (datetime.now() + timedelta(days=days_ahead)).strftime('%Y-%m-%d')
            
            # For forecast, we'll use historical data as proxy
            # In production, integrate with a proper weather forecast API
            return self.get_weather_data(latitude, longitude, start_date, end_date)
            
        except Exception as e:
            logger.error(f"Error getting forecast data: {str(e)}")
            return {}
    
    def calculate_irrigation_need(self, latitude: float, longitude: float, 
                                soil_moisture: float = None) -> Dict:
        """
        Calculate irrigation need based on weather data and soil moisture
        
        Args:
            latitude: Farm latitude
            longitude: Farm longitude
            soil_moisture: Current soil moisture percentage
        
        Returns:
            Dictionary with irrigation recommendations
        """
        try:
            # Get recent weather data (last 7 days)
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            
            weather_data = self.get_weather_data(latitude, longitude, start_date, end_date)
            
            if not weather_data:
                return {'error': 'Unable to fetch weather data'}
            
            # Calculate cumulative ET0 and precipitation
            total_et0 = 0
            total_precipitation = 0
            
            if 'et0' in weather_data and weather_data['et0']:
                for date, value in weather_data['et0'].items():
                    if value is not None:
                        total_et0 += float(value)
            
            if 'precipitation' in weather_data and weather_data['precipitation']:
                for date, value in weather_data['precipitation'].items():
                    if value is not None:
                        total_precipitation += float(value)
            
            # Simple irrigation calculation
            # Water deficit = ET0 - Precipitation
            water_deficit = total_et0 - total_precipitation
            
            # Soil moisture threshold (adjust based on crop type)
            soil_moisture_threshold = 50  # 50% as default threshold
            
            recommendation = {
                'water_deficit_mm': round(water_deficit, 2),
                'total_et0_mm': round(total_et0, 2),
                'total_precipitation_mm': round(total_precipitation, 2),
                'soil_moisture': soil_moisture,
                'irrigation_needed': water_deficit > 0 or (soil_moisture and soil_moisture < soil_moisture_threshold),
                'recommended_irrigation_mm': max(0, water_deficit) if water_deficit > 0 else 0
            }
            
            return recommendation
            
        except Exception as e:
            logger.error(f"Error calculating irrigation need: {str(e)}")
            return {'error': str(e)}

# Example usage and testing
if __name__ == "__main__":
    # Test the NASA POWER API
    api = NASAPowerAPI()
    
    # Test coordinates (example: Delhi, India)
    lat, lon = 28.6139, 77.2090
    
    # Get weather data
    weather = api.get_weather_data(lat, lon, "2024-01-01", "2024-01-07")
    print("Weather Data:", weather)
    
    # Calculate irrigation need
    irrigation = api.calculate_irrigation_need(lat, lon, 45)
    print("Irrigation Need:", irrigation)
