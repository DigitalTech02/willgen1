import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    # Force SQLite for development - override any system DATABASE_URL
    database_url = os.environ.get('DATABASE_URL', '')
    if database_url.startswith('postgres'):
        # Override PostgreSQL with SQLite for development
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    else:
        SQLALCHEMY_DATABASE_URI = database_url or 'sqlite:///' + os.path.join(basedir, 'app.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Google OAuth Configuration
    GOOGLE_OAUTH_CLIENT_ID = os.environ.get('GOOGLE_OAUTH_CLIENT_ID')
    GOOGLE_OAUTH_CLIENT_SECRET = os.environ.get('GOOGLE_OAUTH_CLIENT_SECRET')
    
    # Flask-Dance Configuration
    OAUTHLIB_INSECURE_TRANSPORT = os.environ.get('OAUTHLIB_INSECURE_TRANSPORT', 'False').lower() == 'true'
    OAUTHLIB_RELAX_TOKEN_SCOPE = True

    # Suppress OAuth scope warnings
    import warnings
    warnings.filterwarnings('ignore', message='.*Scope has changed.*')


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    OAUTHLIB_INSECURE_TRANSPORT = True  # Allow HTTP for development


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    OAUTHLIB_INSECURE_TRANSPORT = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
