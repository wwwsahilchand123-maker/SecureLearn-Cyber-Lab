# backend/models/database_models.py
"""
Database models and schema definitions
Educational Phishing Detection Simulator
"""

import sqlite3
from datetime import datetime
from typing import Dict, List, Optional

class DatabaseSchema:
    """Database schema definitions"""
    
    USERS_TABLE = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    
    SIMULATION_EVENTS_TABLE = """
    CREATE TABLE IF NOT EXISTS simulation_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        event_type TEXT NOT NULL,
        event_data TEXT,
        risk_level TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (session_id) REFERENCES users(session_id)
    )
    """
    
    ANALYSIS_RESULTS_TABLE = """
    CREATE TABLE IF NOT EXISTS analysis_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        analysis_type TEXT NOT NULL,
        input_data TEXT NOT NULL,
        result_data TEXT NOT NULL,
        risk_score REAL,
        is_phishing BOOLEAN,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (session_id) REFERENCES users(session_id)
    )
    """
    
    QUIZ_RESULTS_TABLE = """
    CREATE TABLE IF NOT EXISTS quiz_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        score INTEGER NOT NULL,
        total_questions INTEGER NOT NULL,
        percentage REAL NOT NULL,
        answers_data TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (session_id) REFERENCES users(session_id)
    )
    """
    
    URL_ANALYSIS_TABLE = """
    CREATE TABLE IF NOT EXISTS url_analysis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        url TEXT NOT NULL,
        features TEXT NOT NULL,
        prediction TEXT NOT NULL,
        confidence REAL NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (session_id) REFERENCES users(session_id)
    )
    """
    
    EMAIL_ANALYSIS_TABLE = """
    CREATE TABLE IF NOT EXISTS email_analysis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        sender TEXT NOT NULL,
        subject TEXT NOT NULL,
        body TEXT NOT NULL,
        prediction TEXT NOT NULL,
        confidence REAL NOT NULL,
        indicators TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (session_id) REFERENCES users(session_id)
    )
    """
    
    @classmethod
    def get_all_schemas(cls) -> List[str]:
        """Return all table schemas"""
        return [
            cls.USERS_TABLE,
            cls.SIMULATION_EVENTS_TABLE,
            cls.ANALYSIS_RESULTS_TABLE,
            cls.QUIZ_RESULTS_TABLE,
            cls.URL_ANALYSIS_TABLE,
            cls.EMAIL_ANALYSIS_TABLE
        ]