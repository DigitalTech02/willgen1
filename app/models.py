from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


def utc_now():
    """Get current UTC time."""
    return datetime.now(timezone.utc)


class User(UserMixin, db.Model):
    """User model for authentication and will ownership."""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    google_id = db.Column(db.String(100), unique=True, nullable=False)
    profile_pic = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=utc_now)
    
    # Relationship with wills
    wills = db.relationship('Will', backref='owner', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.email}>'


class Will(db.Model):
    """Will model to store will documents."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)

    # Step 1: Testator Information
    testator_name = db.Column(db.String(200))
    testator_date_of_birth = db.Column(db.Date)
    testator_address = db.Column(db.Text)
    testator_city = db.Column(db.String(100))
    testator_state = db.Column(db.String(50))
    testator_zip = db.Column(db.String(20))
    testator_country = db.Column(db.String(100))
    testator_phone = db.Column(db.String(20))
    testator_email = db.Column(db.String(100))
    marital_status = db.Column(db.String(50))
    spouse_name = db.Column(db.String(200))

    # Step 2: Beneficiaries (stored as JSON)
    beneficiaries = db.Column(db.Text)  # JSON string of beneficiaries

    # Step 3: Executors
    primary_executor_name = db.Column(db.String(200))
    primary_executor_address = db.Column(db.Text)
    primary_executor_relationship = db.Column(db.String(100))
    primary_executor_phone = db.Column(db.String(20))
    primary_executor_email = db.Column(db.String(100))

    alternate_executor_name = db.Column(db.String(200))
    alternate_executor_address = db.Column(db.Text)
    alternate_executor_relationship = db.Column(db.String(100))
    alternate_executor_phone = db.Column(db.String(20))
    alternate_executor_email = db.Column(db.String(100))

    # Step 4: Distribution of Assets
    real_estate_properties = db.Column(db.Text)  # JSON string
    bank_accounts = db.Column(db.Text)  # JSON string
    investments = db.Column(db.Text)  # JSON string
    personal_property = db.Column(db.Text)  # JSON string
    other_assets = db.Column(db.Text)  # JSON string
    specific_bequests = db.Column(db.Text)  # JSON string
    residuary_beneficiary = db.Column(db.String(200))

    # Step 5: Special Instructions
    funeral_wishes = db.Column(db.Text)
    burial_cremation_wishes = db.Column(db.Text)
    guardian_minor_children = db.Column(db.String(200))
    guardian_address = db.Column(db.Text)
    special_instructions = db.Column(db.Text)
    charitable_donations = db.Column(db.Text)  # JSON string

    # Wizard Progress Tracking
    current_step = db.Column(db.Integer, default=1)
    step_1_completed = db.Column(db.Boolean, default=False)
    step_2_completed = db.Column(db.Boolean, default=False)
    step_3_completed = db.Column(db.Boolean, default=False)
    step_4_completed = db.Column(db.Boolean, default=False)
    step_5_completed = db.Column(db.Boolean, default=False)

    # Metadata
    created_at = db.Column(db.DateTime, default=utc_now)
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now)
    is_completed = db.Column(db.Boolean, default=False)

    # Foreign key to User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f'<Will {self.title}>'
    
    def to_dict(self):
        """Convert will to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'title': self.title,
            'testator_name': self.testator_name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_completed': self.is_completed
        }
