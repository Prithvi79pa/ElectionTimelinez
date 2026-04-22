import os

class Config:
    """Application configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    ELECTIONS_DIR = os.path.join(DATA_DIR, 'elections')
    STATES_DIR = os.path.join(DATA_DIR, 'states')
    CONTENT_DIR = os.path.join(DATA_DIR, 'content')
    QUIZZES_DIR = os.path.join(DATA_DIR, 'quizzes')

    # Application settings
    DEFAULT_ELECTION = '2026_midterm'
    SUPPORTED_LANGUAGES = ['en', 'es']
    DEFAULT_LANGUAGE = 'en'
