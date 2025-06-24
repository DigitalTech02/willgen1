import json
from flask import Flask
from flask_login import LoginManager
from flask_dance.contrib.google import make_google_blueprint
from flask_wtf.csrf import CSRFProtect
from config import config
from app.models import db, User


def create_app(config_name='default'):
    """Application factory pattern."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)

    # Initialize CSRF protection
    csrf = CSRFProtect(app)
    
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Create Google OAuth blueprint
    google_bp = make_google_blueprint(
        client_id=app.config.get('GOOGLE_OAUTH_CLIENT_ID'),
        client_secret=app.config.get('GOOGLE_OAUTH_CLIENT_SECRET'),
        scope=[
            'openid',
            'https://www.googleapis.com/auth/userinfo.email',
            'https://www.googleapis.com/auth/userinfo.profile'
        ]
    )
    app.register_blueprint(google_bp, url_prefix='/auth')

    # Register blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    # Add custom Jinja2 filters
    @app.template_filter('from_json')
    def from_json_filter(value):
        """Convert JSON string to Python object."""
        if not value:
            return []
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return []

    # Create database tables
    with app.app_context():
        db.create_all()

    return app
