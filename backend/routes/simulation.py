# backend/routes/simulation.py
"""
Simulation API Routes
Educational Phishing Detection Simulator
"""

from flask import Blueprint, request, jsonify, session
from backend.database.db_manager import DatabaseManager
import uuid

simulation_bp = Blueprint('simulation', __name__)
db = DatabaseManager()

def get_session_id():
    """Get or create session ID"""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
        db.create_user(session['session_id'])
    return session['session_id']

@simulation_bp.route('/simulation-event', methods=['POST'])
def log_simulation_event():
    """Log simulation event (NO PASSWORDS STORED)"""
    try:
        data = request.get_json()
        
        if not data or 'event_type' not in data:
            return jsonify({'error': 'Event type is required'}), 400
        
        session_id = get_session_id()
        event_type = data['event_type']
        
        # SECURITY: Never store passwords or sensitive data
        # Only store event metadata
        safe_event_data = {
            'page': data.get('page', 'unknown'),
            'timestamp': data.get('timestamp'),
            'interaction': data.get('interaction', 'unknown')
        }
        
        risk_level = data.get('risk_level', 'UNKNOWN')
        
        # Log event
        event_id = db.log_simulation_event(
            session_id=session_id,
            event_type=event_type,
            event_data=safe_event_data,
            risk_level=risk_level
        )
        
        # Update user activity
        db.update_user_activity(session_id)
        
        return jsonify({
            'success': True,
            'event_id': event_id,
            'message': 'Event logged successfully'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@simulation_bp.route('/simulation-warning', methods=['POST'])
def show_simulation_warning():
    """Return educational warning for simulation"""
    try:
        data = request.get_json()
        simulation_type = data.get('type', 'generic')
        
        warnings = {
            'phishing_page': {
                'title': '⚠️ PHISHING SIMULATION DETECTED',
                'message': 'You just interacted with a simulated phishing page!',
                'indicators': [
                    'This page was designed to look like a legitimate login',
                    'In a real attack, your credentials would be stolen',
                    'Always verify the URL before entering credentials',
                    'Look for HTTPS and the correct domain name',
                    'Be suspicious of urgent or threatening messages'
                ],
                'education': 'Never enter your real password on unfamiliar websites. Always verify the legitimacy through official channels.'
            },
            'suspicious_link': {
                'title': '⚠️ SUSPICIOUS LINK DETECTED',
                'message': 'This link shows signs of phishing!',
                'indicators': [
                    'Mismatched or suspicious domain',
                    'Urgency-creating language',
                    'Requests for personal information',
                    'Unusual URL structure'
                ],
                'education': 'Hover over links to preview the destination. Contact the organization directly if unsure.'
            }
        }
        
        warning = warnings.get(simulation_type, warnings['phishing_page'])
        
        return jsonify({
            'success': True,
            'warning': warning
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@simulation_bp.route('/simulation-stats', methods=['GET'])
def get_simulation_stats():
    """Get simulation statistics"""
    try:
        session_id = get_session_id()
        
        # Get user's simulation events
        events = db.get_simulation_events(session_id=session_id, limit=100)
        
        stats = {
            'total_events': len(events),
            'event_types': {},
            'risk_levels': {}
        }
        
        for event in events:
            event_type = event['event_type']
            risk_level = event['risk_level']
            
            stats['event_types'][event_type] = stats['event_types'].get(event_type, 0) + 1
            stats['risk_levels'][risk_level] = stats['risk_levels'].get(risk_level, 0) + 1
        
        return jsonify({
            'success': True,
            'stats': stats
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500