"""
Database models for KhetSetGo application
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Farm(db.Model):
    """Farm location and boundary data"""
    __tablename__ = 'farms'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    district = db.Column(db.String(100), nullable=False)
    village = db.Column(db.String(100), nullable=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    boundary_geojson = db.Column(db.Text, nullable=True)  # Store GeoJSON as text
    area_hectares = db.Column(db.Float, nullable=True)
    crop_type = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    recommendations = db.relationship('Recommendation', backref='farm', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'district': self.district,
            'village': self.village,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'boundary_geojson': json.loads(self.boundary_geojson) if self.boundary_geojson else None,
            'area_hectares': self.area_hectares,
            'crop_type': self.crop_type,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Recommendation(db.Model):
    """Irrigation and farming recommendations"""
    __tablename__ = 'recommendations'
    
    id = db.Column(db.Integer, primary_key=True)
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id'), nullable=False)
    recommendation_type = db.Column(db.String(50), nullable=False)  # 'irrigation', 'sowing', 'harvest'
    message_hindi = db.Column(db.Text, nullable=False)
    message_english = db.Column(db.Text, nullable=False)
    irrigation_amount_mm = db.Column(db.Float, nullable=True)
    urgency_level = db.Column(db.String(20), nullable=False)  # 'low', 'medium', 'high'
    confidence_score = db.Column(db.Float, nullable=False)  # 0.0 to 1.0
    soil_moisture = db.Column(db.Float, nullable=True)
    ndvi_value = db.Column(db.Float, nullable=True)
    rainfall_forecast = db.Column(db.Float, nullable=True)
    temperature = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'farm_id': self.farm_id,
            'recommendation_type': self.recommendation_type,
            'message_hindi': self.message_hindi,
            'message_english': self.message_english,
            'irrigation_amount_mm': self.irrigation_amount_mm,
            'urgency_level': self.urgency_level,
            'confidence_score': self.confidence_score,
            'soil_moisture': self.soil_moisture,
            'ndvi_value': self.ndvi_value,
            'rainfall_forecast': self.rainfall_forecast,
            'temperature': self.temperature,
            'created_at': self.created_at.isoformat(),
            'expires_at': self.expires_at.isoformat() if self.expires_at else None
        }

class Notification(db.Model):
    """SMS and voice notifications sent to farmers"""
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id'), nullable=False)
    recommendation_id = db.Column(db.Integer, db.ForeignKey('recommendations.id'), nullable=True)
    notification_type = db.Column(db.String(20), nullable=False)  # 'sms', 'voice'
    phone_number = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # 'pending', 'sent', 'delivered', 'failed'
    twilio_sid = db.Column(db.String(100), nullable=True)  # Twilio message SID
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    sent_at = db.Column(db.DateTime, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'farm_id': self.farm_id,
            'recommendation_id': self.recommendation_id,
            'notification_type': self.notification_type,
            'phone_number': self.phone_number,
            'message': self.message,
            'status': self.status,
            'twilio_sid': self.twilio_sid,
            'created_at': self.created_at.isoformat(),
            'sent_at': self.sent_at.isoformat() if self.sent_at else None
        }

class WeatherData(db.Model):
    """Historical weather data cache"""
    __tablename__ = 'weather_data'
    
    id = db.Column(db.Integer, primary_key=True)
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    temperature = db.Column(db.Float, nullable=True)
    humidity = db.Column(db.Float, nullable=True)
    precipitation = db.Column(db.Float, nullable=True)
    et0 = db.Column(db.Float, nullable=True)  # Reference evapotranspiration
    soil_moisture = db.Column(db.Float, nullable=True)
    ndvi = db.Column(db.Float, nullable=True)
    data_source = db.Column(db.String(50), nullable=False)  # 'nasa_power', 'modis', 'smap'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'farm_id': self.farm_id,
            'date': self.date.isoformat(),
            'temperature': self.temperature,
            'humidity': self.humidity,
            'precipitation': self.precipitation,
            'et0': self.et0,
            'soil_moisture': self.soil_moisture,
            'ndvi': self.ndvi,
            'data_source': self.data_source,
            'created_at': self.created_at.isoformat()
        }
