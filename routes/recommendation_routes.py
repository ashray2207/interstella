"""
Recommendation generation routes
"""

from flask import Blueprint, request, jsonify
from models import db, Farm, Recommendation
from data_fetch.nasa_power_api import NASAPowerAPI
from data_fetch.satellite_data import SatelliteDataFetcher
import logging
from datetime import datetime, timedelta

recommendation_bp = Blueprint('recommendations', __name__)
logger = logging.getLogger(__name__)

@recommendation_bp.route('/', methods=['GET'])
def get_recommendations():
    """Get recommendations for a specific farm"""
    try:
        farm_id = request.args.get('farm_id', type=int)
        
        if not farm_id:
            return jsonify({
                'success': False,
                'error': 'Farm ID is required'
            }), 400
        
        farm = Farm.query.get(farm_id)
        if not farm:
            return jsonify({
                'success': False,
                'error': 'Farm not found'
            }), 404
        
        # Get recent recommendations
        recommendations = Recommendation.query.filter_by(farm_id=farm_id).order_by(Recommendation.created_at.desc()).limit(10).all()
        
        return jsonify({
            'success': True,
            'farm': farm.to_dict(),
            'recommendations': [rec.to_dict() for rec in recommendations]
        })
        
    except Exception as e:
        logger.error(f"Error getting recommendations: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@recommendation_bp.route('/generate', methods=['POST'])
def generate_recommendations():
    """Generate new recommendations for a farm"""
    try:
        data = request.get_json()
        farm_id = data.get('farm_id')
        
        if not farm_id:
            return jsonify({
                'success': False,
                'error': 'Farm ID is required'
            }), 400
        
        farm = Farm.query.get(farm_id)
        if not farm:
            return jsonify({
                'success': False,
                'error': 'Farm not found'
            }), 404
        
        # Generate recommendations
        recommendations = _generate_farm_recommendations(farm)
        
        return jsonify({
            'success': True,
            'farm': farm.to_dict(),
            'recommendations': recommendations
        })
        
    except Exception as e:
        logger.error(f"Error generating recommendations: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def _generate_farm_recommendations(farm):
    """Generate recommendations for a specific farm"""
    try:
        # Initialize APIs
        nasa_api = NASAPowerAPI()
        fetcher = SatelliteDataFetcher()
        
        # Get recent data
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        
        # Get irrigation analysis
        irrigation_analysis = nasa_api.calculate_irrigation_need(
            farm.latitude, farm.longitude
        )
        
        # Get satellite data
        satellite_data = fetcher.get_comprehensive_data(
            farm.latitude, farm.longitude, start_date, end_date
        )
        
        recommendations = []
        
        # Generate irrigation recommendation
        if irrigation_analysis.get('irrigation_needed', False):
            irrigation_amount = irrigation_analysis.get('recommended_irrigation_mm', 0)
            
            recommendation = Recommendation(
                farm_id=farm.id,
                recommendation_type='irrigation',
                message_hindi=f'सिंचाई अभी करें - {irrigation_amount:.1f}mm पानी डालें',
                message_english=f'Irrigate now - apply {irrigation_amount:.1f}mm water',
                irrigation_amount_mm=irrigation_amount,
                urgency_level='high' if irrigation_amount > 20 else 'medium',
                confidence_score=0.85,
                soil_moisture=irrigation_analysis.get('soil_moisture'),
                created_at=datetime.now(),
                expires_at=datetime.now() + timedelta(days=2)
            )
            
            db.session.add(recommendation)
            recommendations.append(recommendation.to_dict())
        
        # Generate crop recommendation based on NDVI
        if satellite_data.get('success') and satellite_data.get('ndvi', {}).get('success'):
            ndvi_data = satellite_data['ndvi']['data']
            if ndvi_data.get('statistics'):
                mean_ndvi = ndvi_data['statistics']['mean']
                
                if mean_ndvi > 0.7:
                    crop_rec = Recommendation(
                        farm_id=farm.id,
                        recommendation_type='harvest',
                        message_hindi='फसल तैयार है - कटाई का समय आ गया है',
                        message_english='Crop is ready - time for harvesting',
                        urgency_level='medium',
                        confidence_score=0.9,
                        ndvi_value=mean_ndvi,
                        created_at=datetime.now(),
                        expires_at=datetime.now() + timedelta(days=7)
                    )
                elif mean_ndvi < 0.3:
                    crop_rec = Recommendation(
                        farm_id=farm.id,
                        recommendation_type='sowing',
                        message_hindi='मिट्टी की स्थिति सही है - बुवाई करें',
                        message_english='Soil condition is good - time for sowing',
                        urgency_level='low',
                        confidence_score=0.8,
                        ndvi_value=mean_ndvi,
                        created_at=datetime.now(),
                        expires_at=datetime.now() + timedelta(days=10)
                    )
                else:
                    crop_rec = Recommendation(
                        farm_id=farm.id,
                        recommendation_type='monitoring',
                        message_hindi='फसल की निगरानी जारी रखें - स्थिति सामान्य है',
                        message_english='Continue monitoring crop - condition is normal',
                        urgency_level='low',
                        confidence_score=0.7,
                        ndvi_value=mean_ndvi,
                        created_at=datetime.now(),
                        expires_at=datetime.now() + timedelta(days=5)
                    )
                
                db.session.add(crop_rec)
                recommendations.append(crop_rec.to_dict())
        
        # Save to database
        db.session.commit()
        
        return recommendations
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error generating farm recommendations: {str(e)}")
        return []

@recommendation_bp.route('/<int:recommendation_id>', methods=['GET'])
def get_recommendation_details(recommendation_id):
    """Get detailed information about a specific recommendation"""
    try:
        recommendation = Recommendation.query.get(recommendation_id)
        if not recommendation:
            return jsonify({
                'success': False,
                'error': 'Recommendation not found'
            }), 404
        
        return jsonify({
            'success': True,
            'recommendation': recommendation.to_dict()
        })
        
    except Exception as e:
        logger.error(f"Error getting recommendation details: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
