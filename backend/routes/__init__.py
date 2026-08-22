# backend/routes/__init__.py
"""
Initialize API routes
"""

from backend.routes.analysis import analysis_bp
from backend.routes.simulation import simulation_bp
from backend.routes.quiz import quiz_bp
from backend.routes.dashboard import dashboard_bp


def register_routes(app):
    """Register all API route blueprints"""

    app.register_blueprint(
        analysis_bp,
        url_prefix='/api'
    )

    app.register_blueprint(
        simulation_bp,
        url_prefix='/api'
    )

    app.register_blueprint(
        quiz_bp,
        url_prefix='/api'
    )

    app.register_blueprint(
        dashboard_bp,
        url_prefix='/api'
    )