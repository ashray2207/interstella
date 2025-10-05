"""
Advanced recommendation engine for irrigation and farming decisions
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class RecommendationEngine:
    """Advanced recommendation engine for smart farming decisions"""
    
    def __init__(self):
        # Crop-specific parameters
        self.crop_parameters = {
            'wheat': {
                'optimal_soil_moisture': 0.45,
                'min_soil_moisture': 0.30,
                'max_soil_moisture': 0.60,
                'optimal_ndvi': 0.75,
                'irrigation_efficiency': 0.85,
                'critical_stages': ['germination', 'tillering', 'flowering', 'grain_filling']
            },
            'rice': {
                'optimal_soil_moisture': 0.55,
                'min_soil_moisture': 0.40,
                'max_soil_moisture': 0.70,
                'optimal_ndvi': 0.80,
                'irrigation_efficiency': 0.90,
                'critical_stages': ['transplanting', 'tillering', 'panicle_initiation', 'heading']
            },
            'cotton': {
                'optimal_soil_moisture': 0.40,
                'min_soil_moisture': 0.25,
                'max_soil_moisture': 0.55,
                'optimal_ndvi': 0.70,
                'irrigation_efficiency': 0.80,
                'critical_stages': ['squaring', 'flowering', 'boll_development']
            },
            'sugarcane': {
                'optimal_soil_moisture': 0.50,
                'min_soil_moisture': 0.35,
                'max_soil_moisture': 0.65,
                'optimal_ndvi': 0.75,
                'irrigation_efficiency': 0.85,
                'critical_stages': ['germination', 'tillering', 'grand_growth']
            },
            'maize': {
                'optimal_soil_moisture': 0.45,
                'min_soil_moisture': 0.30,
                'max_soil_moisture': 0.60,
                'optimal_ndvi': 0.75,
                'irrigation_efficiency': 0.80,
                'critical_stages': ['emergence', 'vegetative', 'reproductive']
            },
            'vegetables': {
                'optimal_soil_moisture': 0.50,
                'min_soil_moisture': 0.35,
                'max_soil_moisture': 0.65,
                'optimal_ndvi': 0.70,
                'irrigation_efficiency': 0.90,
                'critical_stages': ['establishment', 'vegetative_growth', 'flowering', 'fruiting']
            }
        }
    
    def generate_irrigation_recommendation(self, 
                                         soil_moisture: float,
                                         crop_type: str,
                                         temperature: float,
                                         humidity: float,
                                         precipitation_forecast: float,
                                         et0: float,
                                         ndvi: float = None,
                                         area_hectares: float = 1.0) -> Dict:
        """
        Generate irrigation recommendation based on multiple factors
        
        Args:
            soil_moisture: Current soil moisture (0.0 to 1.0)
            crop_type: Type of crop being grown
            temperature: Current temperature in Celsius
            humidity: Current humidity percentage
            precipitation_forecast: Forecasted precipitation in next 3 days (mm)
            et0: Reference evapotranspiration (mm/day)
            ndvi: Normalized Difference Vegetation Index
            area_hectares: Farm area in hectares
        
        Returns:
            Dictionary containing irrigation recommendation
        """
        try:
            # Get crop parameters
            crop_params = self.crop_parameters.get(crop_type.lower(), 
                                                 self.crop_parameters['wheat'])
            
            # Calculate water deficit
            water_deficit = et0 - precipitation_forecast
            
            # Determine irrigation need based on soil moisture
            optimal_moisture = crop_params['optimal_soil_moisture']
            min_moisture = crop_params['min_soil_moisture']
            
            # Calculate irrigation amount
            irrigation_amount = 0
            urgency = 'low'
            confidence = 0.8
            
            if soil_moisture < min_moisture:
                # Critical irrigation needed
                irrigation_amount = (optimal_moisture - soil_moisture) * 100  # Convert to mm
                urgency = 'high'
                confidence = 0.95
            elif soil_moisture < optimal_moisture and water_deficit > 2:
                # Moderate irrigation needed
                irrigation_amount = min((optimal_moisture - soil_moisture) * 80, water_deficit)
                urgency = 'medium'
                confidence = 0.85
            elif water_deficit > 5:
                # Light irrigation for water deficit
                irrigation_amount = min(water_deficit * 0.7, 15)  # Max 15mm
                urgency = 'low'
                confidence = 0.75
            
            # Adjust for crop efficiency
            irrigation_amount = irrigation_amount / crop_params['irrigation_efficiency']
            
            # Generate messages
            if irrigation_amount > 0:
                message_english = f"Irrigate now - apply {irrigation_amount:.1f}mm water"
                message_hindi = f"सिंचाई अभी करें - {irrigation_amount:.1f}mm पानी डालें"
            else:
                message_english = "No irrigation needed - soil moisture is adequate"
                message_hindi = "सिंचाई की आवश्यकता नहीं - मिट्टी में पर्याप्त नमी है"
            
            # Add contextual information
            if precipitation_forecast > 5:
                message_english += f" (Rain expected: {precipitation_forecast:.1f}mm)"
                message_hindi += f" (बारिश की संभावना: {precipitation_forecast:.1f}mm)"
            
            return {
                'recommendation_type': 'irrigation',
                'irrigation_amount_mm': round(irrigation_amount, 1),
                'urgency_level': urgency,
                'confidence_score': confidence,
                'message_english': message_english,
                'message_hindi': message_hindi,
                'reasoning': {
                    'soil_moisture': soil_moisture,
                    'optimal_moisture': optimal_moisture,
                    'water_deficit': water_deficit,
                    'crop_type': crop_type,
                    'irrigation_efficiency': crop_params['irrigation_efficiency']
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating irrigation recommendation: {str(e)}")
            return {
                'recommendation_type': 'irrigation',
                'irrigation_amount_mm': 0,
                'urgency_level': 'low',
                'confidence_score': 0.5,
                'message_english': 'Unable to generate irrigation recommendation',
                'message_hindi': 'सिंचाई सिफारिश उत्पन्न नहीं कर सकते',
                'error': str(e)
            }
    
    def generate_crop_recommendation(self,
                                   ndvi: float,
                                   ndvi_trend: str,
                                   soil_moisture: float,
                                   temperature: float,
                                   crop_type: str = None) -> Dict:
        """
        Generate crop management recommendations based on NDVI and other factors
        
        Args:
            ndvi: Current NDVI value (0.0 to 1.0)
            ndvi_trend: Trend in NDVI ('increasing', 'decreasing', 'stable')
            soil_moisture: Current soil moisture (0.0 to 1.0)
            temperature: Current temperature in Celsius
            crop_type: Type of crop (optional)
        
        Returns:
            Dictionary containing crop recommendation
        """
        try:
            recommendation_type = 'monitoring'
            urgency = 'low'
            confidence = 0.7
            message_english = "Continue monitoring crop - condition is normal"
            message_hindi = "फसल की निगरानी जारी रखें - स्थिति सामान्य है"
            
            # NDVI-based recommendations
            if ndvi > 0.7:
                if ndvi_trend == 'decreasing':
                    recommendation_type = 'harvest'
                    urgency = 'medium'
                    confidence = 0.85
                    message_english = "Crop is ready - time for harvesting"
                    message_hindi = "फसल तैयार है - कटाई का समय आ गया है"
                else:
                    recommendation_type = 'monitoring'
                    urgency = 'low'
                    confidence = 0.8
                    message_english = "Crop is healthy - continue monitoring"
                    message_hindi = "फसल स्वस्थ है - निगरानी जारी रखें"
            
            elif ndvi < 0.3:
                if soil_moisture > 0.4:
                    recommendation_type = 'sowing'
                    urgency = 'low'
                    confidence = 0.8
                    message_english = "Soil condition is good - time for sowing"
                    message_hindi = "मिट्टी की स्थिति सही है - बुवाई करें"
                else:
                    recommendation_type = 'irrigation'
                    urgency = 'high'
                    confidence = 0.9
                    message_english = "Soil too dry - irrigation needed before sowing"
                    message_hindi = "मिट्टी बहुत सूखी है - बुवाई से पहले सिंचाई आवश्यक"
            
            elif 0.3 <= ndvi <= 0.5:
                if ndvi_trend == 'decreasing':
                    recommendation_type = 'fertilizer'
                    urgency = 'medium'
                    confidence = 0.75
                    message_english = "Crop showing stress - consider fertilization"
                    message_hindi = "फसल में तनाव दिख रहा है - उर्वरक पर विचार करें"
                else:
                    recommendation_type = 'monitoring'
                    urgency = 'low'
                    confidence = 0.7
                    message_english = "Crop is developing - monitor growth"
                    message_hindi = "फसल विकसित हो रही है - वृद्धि पर नजर रखें"
            
            return {
                'recommendation_type': recommendation_type,
                'urgency_level': urgency,
                'confidence_score': confidence,
                'message_english': message_english,
                'message_hindi': message_hindi,
                'ndvi_value': ndvi,
                'ndvi_trend': ndvi_trend,
                'reasoning': {
                    'ndvi': ndvi,
                    'ndvi_trend': ndvi_trend,
                    'soil_moisture': soil_moisture,
                    'temperature': temperature,
                    'crop_type': crop_type
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating crop recommendation: {str(e)}")
            return {
                'recommendation_type': 'monitoring',
                'urgency_level': 'low',
                'confidence_score': 0.5,
                'message_english': 'Unable to generate crop recommendation',
                'message_hindi': 'फसल सिफारिश उत्पन्न नहीं कर सकते',
                'error': str(e)
            }
    
    def generate_comprehensive_recommendations(self, farm_data: Dict) -> List[Dict]:
        """
        Generate comprehensive recommendations for a farm
        
        Args:
            farm_data: Dictionary containing farm information and sensor data
        
        Returns:
            List of recommendation dictionaries
        """
        try:
            recommendations = []
            
            # Extract data
            soil_moisture = farm_data.get('soil_moisture', 0.4)
            crop_type = farm_data.get('crop_type', 'wheat')
            temperature = farm_data.get('temperature', 25)
            humidity = farm_data.get('humidity', 60)
            precipitation_forecast = farm_data.get('precipitation_forecast', 0)
            et0 = farm_data.get('et0', 4)
            ndvi = farm_data.get('ndvi', 0.6)
            ndvi_trend = farm_data.get('ndvi_trend', 'stable')
            
            # Generate irrigation recommendation
            irrigation_rec = self.generate_irrigation_recommendation(
                soil_moisture=soil_moisture,
                crop_type=crop_type,
                temperature=temperature,
                humidity=humidity,
                precipitation_forecast=precipitation_forecast,
                et0=et0,
                ndvi=ndvi,
                area_hectares=farm_data.get('area_hectares', 1.0)
            )
            
            if irrigation_rec['irrigation_amount_mm'] > 0:
                recommendations.append(irrigation_rec)
            
            # Generate crop recommendation
            crop_rec = self.generate_crop_recommendation(
                ndvi=ndvi,
                ndvi_trend=ndvi_trend,
                soil_moisture=soil_moisture,
                temperature=temperature,
                crop_type=crop_type
            )
            
            recommendations.append(crop_rec)
            
            # Add weather-based recommendations
            if temperature > 35:
                weather_rec = {
                    'recommendation_type': 'weather',
                    'urgency_level': 'medium',
                    'confidence_score': 0.8,
                    'message_english': 'High temperature alert - increase irrigation frequency',
                    'message_hindi': 'उच्च तापमान चेतावनी - सिंचाई की आवृत्ति बढ़ाएं',
                    'temperature': temperature,
                    'reasoning': {'high_temperature': True}
                }
                recommendations.append(weather_rec)
            
            if precipitation_forecast > 20:
                weather_rec = {
                    'recommendation_type': 'weather',
                    'urgency_level': 'low',
                    'confidence_score': 0.9,
                    'message_english': 'Heavy rain expected - reduce irrigation',
                    'message_hindi': 'भारी बारिश की संभावना - सिंचाई कम करें',
                    'precipitation_forecast': precipitation_forecast,
                    'reasoning': {'heavy_rain_expected': True}
                }
                recommendations.append(weather_rec)
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating comprehensive recommendations: {str(e)}")
            return []

# Example usage
if __name__ == "__main__":
    engine = RecommendationEngine()
    
    # Test irrigation recommendation
    irrigation_rec = engine.generate_irrigation_recommendation(
        soil_moisture=0.35,
        crop_type='wheat',
        temperature=28,
        humidity=65,
        precipitation_forecast=2,
        et0=5.2,
        ndvi=0.68
    )
    
    print("Irrigation Recommendation:", irrigation_rec)
    
    # Test crop recommendation
    crop_rec = engine.generate_crop_recommendation(
        ndvi=0.72,
        ndvi_trend='increasing',
        soil_moisture=0.45,
        temperature=26
    )
    
    print("Crop Recommendation:", crop_rec)
