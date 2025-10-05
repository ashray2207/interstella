"""
KhetSetGo - Smart Crop & Water Advisor
Main Flask application for the smart farming irrigation system
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///khetsetgo.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app, origins=[os.getenv('FRONTEND_URL', 'http://localhost:3000')])

# Import models
from models import Farm, Recommendation, Notification

# Import API routes
from routes.farm_routes import farm_bp
from routes.data_routes import data_bp
from routes.recommendation_routes import recommendation_bp
from routes.notification_routes import notification_bp

# Register blueprints
app.register_blueprint(farm_bp, url_prefix='/api/farm')
app.register_blueprint(data_bp, url_prefix='/api/data')
app.register_blueprint(recommendation_bp, url_prefix='/api/recommendations')
app.register_blueprint(notification_bp, url_prefix='/api/notifications')

@app.route('/')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'KhetSetGo API is running',
        'version': '1.0.0'
    })

@app.route('/api/status')
def api_status():
    """API status endpoint"""
    return jsonify({
        'api_version': '1.0.0',
        'endpoints': {
            'farm': '/api/farm',
            'data': '/api/data',
            'recommendations': '/api/recommendations',
            'notifications': '/api/notifications'
        }
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=os.getenv('FLASK_DEBUG', 'True').lower() == 'true', port=5000)
