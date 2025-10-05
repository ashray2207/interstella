"""
Satellite data integration for MODIS NDVI, SMAP Soil Moisture, and GPM Precipitation
"""

import requests
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os
import logging
from typing import Dict, List, Optional, Tuple
import json

logger = logging.getLogger(__name__)

class SatelliteDataFetcher:
    """Fetcher for various satellite data sources"""
    
    def __init__(self):
        self.moderate_api_key = os.getenv('MODERATE_API_KEY')
        self.earthdata_username = os.getenv('EARTHDATA_USERNAME')
        self.earthdata_password = os.getenv('EARTHDATA_PASSWORD')
    
    def get_modis_ndvi(self, latitude: float, longitude: float, 
                      start_date: str, end_date: str = None) -> Dict:
        """
        Fetch MODIS NDVI data for crop health monitoring
        
        Args:
            latitude: Farm latitude
            longitude: Farm longitude
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
        
        Returns:
            Dictionary containing NDVI data
        """
        try:
            if not end_date:
                end_date = datetime.now().strftime('%Y-%m-%d')
            
            # For demo purposes, generate synthetic NDVI data
            # In production, integrate with NASA Earthdata or similar service
            ndvi_data = self._generate_synthetic_ndvi(latitude, longitude, start_date, end_date)
            
            return {
                'success': True,
                'data': ndvi_data,
                'source': 'MODIS',
                'parameter': 'NDVI',
                'unit': 'index',
                'description': 'Normalized Difference Vegetation Index'
            }
            
        except Exception as e:
            logger.error(f"Error fetching MODIS NDVI data: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def get_smap_soil_moisture(self, latitude: float, longitude: float, 
                              start_date: str, end_date: str = None) -> Dict:
        """
        Fetch SMAP soil moisture data
        
        Args:
            latitude: Farm latitude
            longitude: Farm longitude
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
        
        Returns:
            Dictionary containing soil moisture data
        """
        try:
            if not end_date:
                end_date = datetime.now().strftime('%Y-%m-%d')
            
            # For demo purposes, generate synthetic soil moisture data
            # In production, integrate with NASA SMAP data portal
            soil_moisture_data = self._generate_synthetic_soil_moisture(latitude, longitude, start_date, end_date)
            
            return {
                'success': True,
                'data': soil_moisture_data,
                'source': 'SMAP',
                'parameter': 'Soil_Moisture',
                'unit': 'cm³/cm³',
                'description': 'Soil moisture content'
            }
            
        except Exception as e:
            logger.error(f"Error fetching SMAP soil moisture data: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def get_gpm_precipitation(self, latitude: float, longitude: float, 
                            start_date: str, end_date: str = None) -> Dict:
        """
        Fetch GPM/IMERG precipitation data
        
        Args:
            latitude: Farm latitude
            longitude: Farm longitude
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
        
        Returns:
            Dictionary containing precipitation data
        """
        try:
            if not end_date:
                end_date = datetime.now().strftime('%Y-%m-%d')
            
            # For demo purposes, generate synthetic precipitation data
            # In production, integrate with NASA GPM data portal
            precipitation_data = self._generate_synthetic_precipitation(latitude, longitude, start_date, end_date)
            
            return {
                'success': True,
                'data': precipitation_data,
                'source': 'GPM/IMERG',
                'parameter': 'Precipitation',
                'unit': 'mm',
                'description': 'Precipitation rate'
            }
            
        except Exception as e:
            logger.error(f"Error fetching GPM precipitation data: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _generate_synthetic_ndvi(self, latitude: float, longitude: float, 
                               start_date: str, end_date: str) -> Dict:
        """Generate synthetic NDVI data for demonstration"""
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            
            dates = []
            ndvi_values = []
            
            current_date = start
            while current_date <= end:
                dates.append(current_date.strftime('%Y-%m-%d'))
                
                # Generate realistic NDVI values (0.0 to 1.0)
                # Add seasonal variation and some randomness
                base_ndvi = 0.6 + 0.3 * np.sin(2 * np.pi * current_date.timetuple().tm_yday / 365)
                noise = np.random.normal(0, 0.05)
                ndvi = max(0.0, min(1.0, base_ndvi + noise))
                
                ndvi_values.append(round(ndvi, 3))
                current_date += timedelta(days=1)
            
            return {
                'dates': dates,
                'values': ndvi_values,
                'statistics': {
                    'mean': round(np.mean(ndvi_values), 3),
                    'min': round(min(ndvi_values), 3),
                    'max': round(max(ndvi_values), 3),
                    'trend': self._calculate_trend(ndvi_values)
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating synthetic NDVI: {str(e)}")
            return {}
    
    def _generate_synthetic_soil_moisture(self, latitude: float, longitude: float, 
                                        start_date: str, end_date: str) -> Dict:
        """Generate synthetic soil moisture data for demonstration"""
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            
            dates = []
            moisture_values = []
            
            current_date = start
            while current_date <= end:
                dates.append(current_date.strftime('%Y-%m-%d'))
                
                # Generate realistic soil moisture values (0.0 to 0.6 cm³/cm³)
                # Add seasonal variation and some randomness
                base_moisture = 0.3 + 0.2 * np.sin(2 * np.pi * current_date.timetuple().tm_yday / 365)
                noise = np.random.normal(0, 0.02)
                moisture = max(0.0, min(0.6, base_moisture + noise))
                
                moisture_values.append(round(moisture, 3))
                current_date += timedelta(days=1)
            
            return {
                'dates': dates,
                'values': moisture_values,
                'statistics': {
                    'mean': round(np.mean(moisture_values), 3),
                    'min': round(min(moisture_values), 3),
                    'max': round(max(moisture_values), 3),
                    'trend': self._calculate_trend(moisture_values)
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating synthetic soil moisture: {str(e)}")
            return {}
    
    def _generate_synthetic_precipitation(self, latitude: float, longitude: float, 
                                        start_date: str, end_date: str) -> Dict:
        """Generate synthetic precipitation data for demonstration"""
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            
            dates = []
            precipitation_values = []
            
            current_date = start
            while current_date <= end:
                dates.append(current_date.strftime('%Y-%m-%d'))
                
                # Generate realistic precipitation values
                # Higher probability of rain during monsoon season
                is_monsoon = 6 <= current_date.month <= 9
                rain_probability = 0.3 if is_monsoon else 0.1
                
                if np.random.random() < rain_probability:
                    # Generate rainfall amount (0-50mm)
                    rainfall = np.random.exponential(5)
                    rainfall = min(50, rainfall)
                else:
                    rainfall = 0
                
                precipitation_values.append(round(rainfall, 2))
                current_date += timedelta(days=1)
            
            return {
                'dates': dates,
                'values': precipitation_values,
                'statistics': {
                    'total': round(sum(precipitation_values), 2),
                    'mean': round(np.mean(precipitation_values), 2),
                    'max': round(max(precipitation_values), 2),
                    'rainy_days': sum(1 for x in precipitation_values if x > 0)
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating synthetic precipitation: {str(e)}")
            return {}
    
    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend direction for time series data"""
        if len(values) < 2:
            return 'insufficient_data'
        
        # Simple linear trend calculation
        x = np.arange(len(values))
        y = np.array(values)
        
        # Calculate slope
        slope = np.polyfit(x, y, 1)[0]
        
        if slope > 0.001:
            return 'increasing'
        elif slope < -0.001:
            return 'decreasing'
        else:
            return 'stable'
    
    def get_comprehensive_data(self, latitude: float, longitude: float, 
                             start_date: str, end_date: str = None) -> Dict:
        """
        Fetch all satellite data sources for comprehensive analysis
        
        Args:
            latitude: Farm latitude
            longitude: Farm longitude
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
        
        Returns:
            Dictionary containing all satellite data
        """
        try:
            if not end_date:
                end_date = datetime.now().strftime('%Y-%m-%d')
            
            # Fetch all data sources
            ndvi_data = self.get_modis_ndvi(latitude, longitude, start_date, end_date)
            soil_moisture_data = self.get_smap_soil_moisture(latitude, longitude, start_date, end_date)
            precipitation_data = self.get_gpm_precipitation(latitude, longitude, start_date, end_date)
            
            return {
                'success': True,
                'coordinates': {'latitude': latitude, 'longitude': longitude},
                'date_range': {'start': start_date, 'end': end_date},
                'ndvi': ndvi_data,
                'soil_moisture': soil_moisture_data,
                'precipitation': precipitation_data,
                'fetched_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error fetching comprehensive satellite data: {str(e)}")
            return {'success': False, 'error': str(e)}

# Example usage and testing
if __name__ == "__main__":
    # Test the satellite data fetcher
    fetcher = SatelliteDataFetcher()
    
    # Test coordinates (example: Delhi, India)
    lat, lon = 28.6139, 77.2090
    
    # Get comprehensive data
    data = fetcher.get_comprehensive_data(lat, lon, "2024-01-01", "2024-01-07")
    print("Comprehensive Satellite Data:", json.dumps(data, indent=2))
