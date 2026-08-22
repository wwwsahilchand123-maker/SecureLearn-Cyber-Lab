# backend/routes/dashboard.py
"""
Dashboard API Routes
Educational Phishing Detection Simulator
"""

from flask import Blueprint, jsonify, session
from backend.database.db_manager import DatabaseManager
import uuid

dashboard_bp = Blueprint('dashboard', __name__)
db = DatabaseManager()

def get_session_id():
    """Get or create session ID"""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
        db.create_user(session['session_id'])
    return session['session_id']

@dashboard_bp.route('/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        stats = db.get_dashboard_stats()
        
        return jsonify({
            'success': True,
            'stats': stats
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/dashboard/activity', methods=['GET'])
def get_recent_activity():
    """Get recent activity"""
    try:
        activity = db.get_recent_activity(limit=20)
        
        return jsonify({
            'success': True,
            'activity': activity
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/dashboard/user-stats', methods=['GET'])
def get_user_stats():
    """Get current user statistics"""
    try:
        session_id = get_session_id()
        
        # Get user's analyses
        analyses = db.get_analysis_results(session_id=session_id)
        
        # Get user's quiz results
        quiz_results = db.get_quiz_results(session_id=session_id)
        
        # Get user's simulation events
        events = db.get_simulation_events(session_id=session_id)
        
        # Calculate stats
        total_analyses = len(analyses)
        phishing_detected = sum(1 for a in analyses if a['is_phishing'])
        
        avg_quiz_score = 0
        if quiz_results:
            avg_quiz_score = sum(r['percentage'] for r in quiz_results) / len(quiz_results)
        
        stats = {
            'total_analyses': total_analyses,
            'phishing_detected': phishing_detected,
            'total_quizzes': len(quiz_results),
            'avg_quiz_score': round(avg_quiz_score, 2),
            'total_simulations': len(events),
            'session_id': session_id
        }
        
        return jsonify({
            'success': True,
            'stats': stats
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500