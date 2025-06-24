#!/usr/bin/env python3
"""
Script to recreate the database with the new schema
"""

import os
import sys
from app import create_app
from app.models import db

def recreate_database():
    """Recreate the database with the new schema."""
    
    # Force SQLite database URL
    os.environ['DATABASE_URL'] = 'sqlite:///app.db'
    
    # Remove existing database file
    db_file = 'app.db'
    if os.path.exists(db_file):
        os.remove(db_file)
        print(f"✅ Removed existing database file: {db_file}")
    
    # Create Flask app with development config
    app = create_app('development')
    
    with app.app_context():
        # Drop all tables (in case any exist)
        try:
            db.drop_all()
            print("✅ Dropped all existing tables")
        except Exception as e:
            print(f"⚠️  No existing tables to drop: {e}")
        
        # Create all tables with new schema
        db.create_all()
        print("✅ Created all tables with new schema")
        
        # Verify tables were created
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"✅ Created tables: {tables}")
        
        # Check Will table columns
        if 'will' in tables:
            columns = [col['name'] for col in inspector.get_columns('will')]
            print(f"✅ Will table columns: {len(columns)} columns")
            print("   Key columns:", [col for col in columns if 'testator' in col or 'executor' in col][:5])
    
    print("\n🎉 Database recreation completed successfully!")
    print("You can now start the application with: python run.py")

if __name__ == '__main__':
    recreate_database()
