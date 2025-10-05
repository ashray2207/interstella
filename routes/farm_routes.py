"""
Farm management routes for KhetSetGo application
"""

from flask import Blueprint, request, jsonify
from models import db, Farm
import json
import geojson
from shapely.geometry import shape
import math

farm_bp = Blueprint('farm', __name__)

@farm_bp.route('/location', methods=['GET'])
def get_farm_locations():
    """Get all farm locations"""
    try:
        farms = Farm.query.all()
        return jsonify({
            'success': True,
            'farms': [farm.to_dict() for farm in farms]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@farm_bp.route('/location', methods=['POST'])
def create_farm_location():
    """Create a new farm location"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'district', 'latitude', 'longitude']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Create new farm
        farm = Farm(
            name=data['name'],
            district=data['district'],
            village=data.get('village'),
            latitude=data['latitude'],
            longitude=data['longitude'],
            crop_type=data.get('crop_type')
        )
        
        db.session.add(farm)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'farm': farm.to_dict(),
            'message': 'Farm location created successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@farm_bp.route('/boundary', methods=['POST'])
def upload_farm_boundary():
    """Upload farm boundary as GeoJSON"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'farm_id' not in data or 'geojson' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing farm_id or geojson data'
            }), 400
        
        farm = Farm.query.get(data['farm_id'])
        if not farm:
            return jsonify({
                'success': False,
                'error': 'Farm not found'
            }), 404
        
        # Validate GeoJSON
        try:
            geojson_obj = geojson.loads(json.dumps(data['geojson']))
            geom = shape(data['geojson'])
            
            # Calculate area in hectares (assuming WGS84 coordinates)
            area_hectares = geom.area * 111000 * 111000 / 10000  # Rough conversion
            
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Invalid GeoJSON: {str(e)}'
            }), 400
        
        # Update farm with boundary data
        farm.boundary_geojson = json.dumps(data['geojson'])
        farm.area_hectares = area_hectares
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'farm': farm.to_dict(),
            'message': 'Farm boundary uploaded successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@farm_bp.route('/search', methods=['GET'])
def search_farms():
    """Search farms by district or village"""
    try:
        district = request.args.get('district', '').strip()
        village = request.args.get('village', '').strip()
        
        query = Farm.query
        
        if district:
            query = query.filter(Farm.district.ilike(f'%{district}%'))
        
        if village:
            query = query.filter(Farm.village.ilike(f'%{village}%'))
        
        farms = query.all()
        
        return jsonify({
            'success': True,
            'farms': [farm.to_dict() for farm in farms],
            'count': len(farms)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@farm_bp.route('/<int:farm_id>', methods=['GET'])
def get_farm_details(farm_id):
    """Get detailed information about a specific farm"""
    try:
        farm = Farm.query.get(farm_id)
        if not farm:
            return jsonify({
                'success': False,
                'error': 'Farm not found'
            }), 404
        
        return jsonify({
            'success': True,
            'farm': farm.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@farm_bp.route('/<int:farm_id>', methods=['PUT'])
def update_farm(farm_id):
    """Update farm information"""
    try:
        farm = Farm.query.get(farm_id)
        if not farm:
            return jsonify({
                'success': False,
                'error': 'Farm not found'
            }), 404
        
        data = request.get_json()
        
        # Update fields if provided
        if 'name' in data:
            farm.name = data['name']
        if 'district' in data:
            farm.district = data['district']
        if 'village' in data:
            farm.village = data['village']
        if 'latitude' in data:
            farm.latitude = data['latitude']
        if 'longitude' in data:
            farm.longitude = data['longitude']
        if 'crop_type' in data:
            farm.crop_type = data['crop_type']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'farm': farm.to_dict(),
            'message': 'Farm updated successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@farm_bp.route('/<int:farm_id>', methods=['DELETE'])
def delete_farm(farm_id):
    """Delete a farm"""
    try:
        farm = Farm.query.get(farm_id)
        if not farm:
            return jsonify({
                'success': False,
                'error': 'Farm not found'
            }), 404
        
        db.session.delete(farm)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Farm deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
