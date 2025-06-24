#!/usr/bin/env python3
"""
WillGen - Digital Will Generator
Main application entry point
"""

import os
from app import create_app

# Create Flask application
app = create_app(os.getenv('FLASK_CONFIG', 'development'))

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    
    # Get debug mode from environment
    debug = os.getenv('FLASK_ENV') == 'development'
    
    print("🚀 Starting WillGen Application...")
    print(f"📍 Running on http://localhost:{port}")
    print(f"🔧 Debug mode: {'ON' if debug else 'OFF'}")
    print("📝 Digital Will Generator - Secure, Simple, Professional")
    print("-" * 60)
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
