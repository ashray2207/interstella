"""
Notification routes for SMS and voice alerts
"""

from flask import Blueprint, request, jsonify
from models import db, Notification, Recommendation, Farm
import os
import logging
from datetime import datetime

notification_bp = Blueprint('notifications', __name__)
logger = logging.getLogger(__name__)

# Mock SMS service for demo (replace with actual Twilio integration)
class MockSMSService:
    def send_sms(self, phone_number, message):
        """Mock SMS service for demonstration"""
        logger.info(f"Sending SMS to {phone_number}: {message}")
        return {
            'success': True,
            'message_sid': f'mock_sid_{datetime.now().timestamp()}',
            'status': 'sent'
        }

sms_service = MockSMSService()

@notification_bp.route('/sms', methods=['POST'])
def send_sms_notification():
    """Send SMS notification to farmer"""
    try:
        data = request.get_json()
        
        farm_id = data.get('farm_id')
        phone_number = data.get('phone_number')
        message = data.get('message')
        recommendation_id = data.get('recommendation_id')
        
        if not all([farm_id, phone_number, message]):
            return jsonify({
                'success': False,
                'error': 'Farm ID, phone number, and message are required'
            }), 400
        
        # Verify farm exists
        farm = Farm.query.get(farm_id)
        if not farm:
            return jsonify({
                'success': False,
                'error': 'Farm not found'
            }), 404
        
        # Send SMS
        sms_result = sms_service.send_sms(phone_number, message)
        
        if sms_result['success']:
            # Create notification record
            notification = Notification(
                farm_id=farm_id,
                recommendation_id=recommendation_id,
                notification_type='sms',
                phone_number=phone_number,
                message=message,
                status='sent',
                twilio_sid=sms_result['message_sid'],
                sent_at=datetime.now()
            )
            
            db.session.add(notification)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'notification': notification.to_dict(),
                'message': 'SMS sent successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to send SMS'
            }), 500
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error sending SMS notification: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@notification_bp.route('/voice', methods=['POST'])
def send_voice_notification():
    """Send voice notification to farmer"""
    try:
        data = request.get_json()
        
        farm_id = data.get('farm_id')
        phone_number = data.get('phone_number')
        message = data.get('message')
        recommendation_id = data.get('recommendation_id')
        
        if not all([farm_id, phone_number, message]):
            return jsonify({
                'success': False,
                'error': 'Farm ID, phone number, and message are required'
            }), 400
        
        # Verify farm exists
        farm = Farm.query.get(farm_id)
        if not farm:
            return jsonify({
                'success': False,
                'error': 'Farm not found'
            }), 404
        
        # For demo, we'll just log the voice message
        logger.info(f"Sending voice call to {phone_number}: {message}")
        
        # Create notification record
        notification = Notification(
            farm_id=farm_id,
            recommendation_id=recommendation_id,
            notification_type='voice',
            phone_number=phone_number,
            message=message,
            status='sent',
            sent_at=datetime.now()
        )
        
        db.session.add(notification)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'notification': notification.to_dict(),
            'message': 'Voice notification sent successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error sending voice notification: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@notification_bp.route('/history', methods=['GET'])
def get_notification_history():
    """Get notification history for a farm"""
    try:
        farm_id = request.args.get('farm_id', type=int)
        
        if not farm_id:
            return jsonify({
                'success': False,
                'error': 'Farm ID is required'
            }), 400
        
        # Get notifications for the farm
        notifications = Notification.query.filter_by(farm_id=farm_id).order_by(Notification.created_at.desc()).limit(50).all()
        
        return jsonify({
            'success': True,
            'notifications': [notif.to_dict() for notif in notifications]
        })
        
    except Exception as e:
        logger.error(f"Error getting notification history: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@notification_bp.route('/send-recommendation', methods=['POST'])
def send_recommendation_notification():
    """Send a recommendation as SMS or voice notification"""
    try:
        data = request.get_json()
        
        recommendation_id = data.get('recommendation_id')
        notification_type = data.get('type', 'sms')  # 'sms' or 'voice'
        phone_number = data.get('phone_number')
        
        if not all([recommendation_id, phone_number]):
            return jsonify({
                'success': False,
                'error': 'Recommendation ID and phone number are required'
            }), 400
        
        # Get recommendation
        recommendation = Recommendation.query.get(recommendation_id)
        if not recommendation:
            return jsonify({
                'success': False,
                'error': 'Recommendation not found'
            }), 404
        
        # Prepare message based on notification type
        if notification_type == 'sms':
            message = recommendation.message_hindi
        else:
            message = f"कृषि सलाह: {recommendation.message_hindi}"
        
        # Send notification
        if notification_type == 'sms':
            return send_sms_notification()
        else:
            return send_voice_notification()
        
    except Exception as e:
        logger.error(f"Error sending recommendation notification: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
