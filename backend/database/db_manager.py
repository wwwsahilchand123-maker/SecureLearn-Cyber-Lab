# backend/database/db_manager.py
"""
Database manager for SQLite operations
Educational Phishing Detection Simulator
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from contextlib import contextmanager
from backend.models.database_models import DatabaseSchema

class DatabaseManager:
    """Manages all database operations"""
    
    def __init__(self, db_path: str = "database/phishing_simulator.db"):
        """Initialize database manager"""
        self.db_path = db_path
        self._ensure_database_directory()
        self.initialize_database()
    
    def _ensure_database_directory(self):
        """Ensure database directory exists"""
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def initialize_database(self):
        """Create all tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            for schema in DatabaseSchema.get_all_schemas():
                cursor.execute(schema)
            print(f"[OK] Database initialized: {self.db_path}")
    
    # ==================== USER OPERATIONS ====================
    
    def create_user(self, session_id: str) -> int:
        """Create a new user session"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR IGNORE INTO users (session_id) VALUES (?)",
                (session_id,)
            )
            return cursor.lastrowid
    
    def get_user(self, session_id: str) -> Optional[Dict]:
        """Get user by session ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE session_id = ?",
                (session_id,)
            )
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def update_user_activity(self, session_id: str):
        """Update user's last active timestamp"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET last_active = CURRENT_TIMESTAMP WHERE session_id = ?",
                (session_id,)
            )
    
    # ==================== SIMULATION EVENTS ====================
    
    def log_simulation_event(self, session_id: str, event_type: str, 
                            event_data: Dict, risk_level: str = "UNKNOWN") -> int:
        """Log a simulation event"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO simulation_events 
                   (session_id, event_type, event_data, risk_level) 
                   VALUES (?, ?, ?, ?)""",
                (session_id, event_type, json.dumps(event_data), risk_level)
            )
            return cursor.lastrowid
    
    def get_simulation_events(self, session_id: Optional[str] = None, 
                             limit: int = 100) -> List[Dict]:
        """Get simulation events"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if session_id:
                cursor.execute(
                    """SELECT * FROM simulation_events 
                       WHERE session_id = ? 
                       ORDER BY timestamp DESC LIMIT ?""",
                    (session_id, limit)
                )
            else:
                cursor.execute(
                    """SELECT * FROM simulation_events 
                       ORDER BY timestamp DESC LIMIT ?""",
                    (limit,)
                )
            return [dict(row) for row in cursor.fetchall()]
    
    # ==================== ANALYSIS RESULTS ====================
    
    def save_analysis_result(self, session_id: str, analysis_type: str,
                            input_data: Dict, result_data: Dict,
                            risk_score: float, is_phishing: bool) -> int:
        """Save analysis result"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO analysis_results 
                   (session_id, analysis_type, input_data, result_data, risk_score, is_phishing) 
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (session_id, analysis_type, json.dumps(input_data), 
                 json.dumps(result_data), risk_score, is_phishing)
            )
            return cursor.lastrowid
    
    def get_analysis_results(self, session_id: Optional[str] = None,
                            analysis_type: Optional[str] = None,
                            limit: int = 100) -> List[Dict]:
        """Get analysis results"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM analysis_results WHERE 1=1"
            params = []
            
            if session_id:
                query += " AND session_id = ?"
                params.append(session_id)
            
            if analysis_type:
                query += " AND analysis_type = ?"
                params.append(analysis_type)
            
            query += " ORDER BY timestamp DESC LIMIT ?"
            params.append(limit)
            
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    # ==================== QUIZ RESULTS ====================
    
    def save_quiz_result(self, session_id: str, score: int, 
                        total_questions: int, answers_data: Dict) -> int:
        """Save quiz result"""
        percentage = (score / total_questions) * 100 if total_questions > 0 else 0
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO quiz_results 
                   (session_id, score, total_questions, percentage, answers_data) 
                   VALUES (?, ?, ?, ?, ?)""",
                (session_id, score, total_questions, percentage, json.dumps(answers_data))
            )
            return cursor.lastrowid
    
    def get_quiz_results(self, session_id: Optional[str] = None,
                        limit: int = 100) -> List[Dict]:
        """Get quiz results"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if session_id:
                cursor.execute(
                    """SELECT * FROM quiz_results 
                       WHERE session_id = ? 
                       ORDER BY timestamp DESC LIMIT ?""",
                    (session_id, limit)
                )
            else:
                cursor.execute(
                    """SELECT * FROM quiz_results 
                       ORDER BY timestamp DESC LIMIT ?""",
                    (limit,)
                )
            return [dict(row) for row in cursor.fetchall()]
    
    # ==================== URL ANALYSIS ====================
    
    def save_url_analysis(self, session_id: str, url: str, 
                         features: Dict, prediction: str, confidence: float) -> int:
        """Save URL analysis result"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO url_analysis 
                   (session_id, url, features, prediction, confidence) 
                   VALUES (?, ?, ?, ?, ?)""",
                (session_id, url, json.dumps(features), prediction, confidence)
            )
            return cursor.lastrowid
    
    # ==================== EMAIL ANALYSIS ====================
    
    def save_email_analysis(self, session_id: str, sender: str, subject: str,
                           body: str, prediction: str, confidence: float,
                           indicators: List[str]) -> int:
        """Save email analysis result"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO email_analysis 
                   (session_id, sender, subject, body, prediction, confidence, indicators) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (session_id, sender, subject, body, prediction, confidence, 
                 json.dumps(indicators))
            )
            return cursor.lastrowid
    
    # ==================== DASHBOARD STATISTICS ====================
    
    def get_dashboard_stats(self) -> Dict:
        """Get dashboard statistics"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Total users
            cursor.execute("SELECT COUNT(*) as count FROM users")
            total_users = cursor.fetchone()['count']
            
            # Total simulations
            cursor.execute("SELECT COUNT(*) as count FROM simulation_events")
            total_simulations = cursor.fetchone()['count']
            
            # Total analyses
            cursor.execute("SELECT COUNT(*) as count FROM analysis_results")
            total_analyses = cursor.fetchone()['count']
            
            # Total quizzes
            cursor.execute("SELECT COUNT(*) as count FROM quiz_results")
            total_quizzes = cursor.fetchone()['count']
            
            # Average quiz score
            cursor.execute("SELECT AVG(percentage) as avg_score FROM quiz_results")
            avg_quiz_score = cursor.fetchone()['avg_score'] or 0
            
            # Phishing detection rate
            cursor.execute(
                "SELECT COUNT(*) as count FROM analysis_results WHERE is_phishing = 1"
            )
            phishing_detected = cursor.fetchone()['count']
            
            # Risk distribution
            cursor.execute(
                """SELECT risk_level, COUNT(*) as count 
                   FROM simulation_events 
                   GROUP BY risk_level"""
            )
            risk_distribution = {row['risk_level']: row['count'] 
                               for row in cursor.fetchall()}
            
            return {
                'total_users': total_users,
                'total_simulations': total_simulations,
                'total_analyses': total_analyses,
                'total_quizzes': total_quizzes,
                'avg_quiz_score': round(avg_quiz_score, 2),
                'phishing_detected': phishing_detected,
                'risk_distribution': risk_distribution
            }
    
    def get_recent_activity(self, limit: int = 20) -> List[Dict]:
        """Get recent activity across all tables"""
        activities = []
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Recent simulations
            cursor.execute(
                """SELECT 'simulation' as type, session_id, event_type as detail, 
                   timestamp FROM simulation_events 
                   ORDER BY timestamp DESC LIMIT ?""",
                (limit,)
            )
            activities.extend([dict(row) for row in cursor.fetchall()])
            
            # Recent analyses
            cursor.execute(
                """SELECT 'analysis' as type, session_id, analysis_type as detail, 
                   timestamp FROM analysis_results 
                   ORDER BY timestamp DESC LIMIT ?""",
                (limit,)
            )
            activities.extend([dict(row) for row in cursor.fetchall()])
            
            # Recent quizzes
            cursor.execute(
                """SELECT 'quiz' as type, session_id, 
                   (CAST(score AS TEXT) || '/' || CAST(total_questions AS TEXT)) as detail, 
                   timestamp FROM quiz_results 
                   ORDER BY timestamp DESC LIMIT ?""",
                (limit,)
            )
            activities.extend([dict(row) for row in cursor.fetchall()])
        
        # Sort by timestamp
        activities.sort(key=lambda x: x['timestamp'], reverse=True)
        return activities[:limit]

# Initialize database on module import
if __name__ == '__main__':
    db = DatabaseManager()
    print("Database initialized successfully!")
    stats = db.get_dashboard_stats()
    print(f"Dashboard Stats: {stats}")