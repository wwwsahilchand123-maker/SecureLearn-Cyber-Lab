# backend/routes/analysis.py
"""
Analysis API Routes
Educational Phishing Detection Simulator
"""

from flask import Blueprint, request, jsonify, session
from backend.services.url_analyzer import URLAnalyzer
from backend.services.email_analyzer import EmailAnalyzer
from backend.services.ml_predictor import PhishingPredictor
from backend.database.db_manager import DatabaseManager
import uuid

analysis_bp = Blueprint('analysis', __name__)

db = DatabaseManager()
url_analyzer = URLAnalyzer()
email_analyzer = EmailAnalyzer()
ml_predictor = PhishingPredictor()


def get_session_id():
    """Get or create session ID"""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
        db.create_user(session['session_id'])

    return session['session_id']


@analysis_bp.route('/analyze-url', methods=['POST'])
def analyze_url():
    """Analyze URL for phishing indicators"""

    try:
        data = request.get_json()

        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required'}), 400

        url = data['url'].strip()

        if not url:
            return jsonify({'error': 'URL cannot be empty'}), 400

        session_id = get_session_id()

        result = url_analyzer.analyze(url)

        features = result['features']

        prediction, confidence, explanation = ml_predictor.predict(features)

        result['ml_prediction'] = prediction
        result['ml_confidence'] = confidence
        result['ml_explanation'] = explanation

        db.save_url_analysis(
            session_id=session_id,
            url=url,
            features=features,
            prediction=prediction,
            confidence=confidence
        )

        db.save_analysis_result(
            session_id=session_id,
            analysis_type='url',
            input_data={'url': url},
            result_data=result,
            risk_score=result['risk_score'],
            is_phishing=(result['risk_level'] == 'HIGH')
        )

        return jsonify({
            'success': True,
            'result': result
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@analysis_bp.route('/analyze-email', methods=['POST'])
def analyze_email():
    """Analyze email for phishing indicators"""

    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Email data is required'}), 400

        sender = data.get('sender', '').strip()
        subject = data.get('subject', '').strip()
        body = data.get('body', '').strip()

        if not sender or not subject or not body:
            return jsonify({
                'error': 'Sender, subject, and body are required'
            }), 400

        session_id = get_session_id()

        result = email_analyzer.analyze(
            sender,
            subject,
            body
        )

        db.save_email_analysis(
            session_id=session_id,
            sender=sender,
            subject=subject,
            body=body,
            prediction=result['risk_level'],
            confidence=result['risk_score'] / 100,
            indicators=result['indicators']
        )

        db.save_analysis_result(
            session_id=session_id,
            analysis_type='email',
            input_data={
                'sender': sender,
                'subject': subject,
                'body': body[:100]
            },
            result_data=result,
            risk_score=result['risk_score'],
            is_phishing=(result['risk_level'] == 'HIGH')
        )

        return jsonify({
            'success': True,
            'result': result
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@analysis_bp.route('/history', methods=['GET'])
def get_history():
    """Get analysis history"""

    try:
        session_id = get_session_id()

        analyses = db.get_analysis_results(
            session_id=session_id,
            limit=50
        )

        return jsonify({
            'success': True,
            'analyses': analyses
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500