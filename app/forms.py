from flask_wtf import FlaskForm
from wtforms import (
    StringField, TextAreaField, DateField, SelectField, 
    FieldList, FormField, BooleanField, EmailField, TelField
)
from wtforms.validators import (
    DataRequired, Email, Optional, Length, ValidationError
)
from datetime import date


class TestatorInfoForm(FlaskForm):
    """Step 1: Testator Information Form"""
    title = StringField('Will Title', validators=[
        DataRequired(message="Please provide a title for your will"),
        Length(min=5, max=200, message="Title must be between 5 and 200 characters")
    ], render_kw={"placeholder": "e.g., John Doe's Last Will and Testament"})
    
    testator_name = StringField('Full Legal Name', validators=[
        DataRequired(message="Please enter your full legal name"),
        Length(min=2, max=200, message="Name must be between 2 and 200 characters")
    ], render_kw={"placeholder": "Enter your full legal name as it appears on official documents"})
    
    testator_date_of_birth = DateField('Date of Birth', validators=[
        DataRequired(message="Please enter your date of birth")
    ])
    
    testator_address = TextAreaField('Street Address', validators=[
        DataRequired(message="Please enter your address"),
        Length(min=5, max=500, message="Address must be between 5 and 500 characters")
    ], render_kw={"rows": 2, "placeholder": "Enter your complete street address"})
    
    testator_city = StringField('City', validators=[
        DataRequired(message="Please enter your city"),
        Length(min=2, max=100, message="City must be between 2 and 100 characters")
    ])
    
    testator_state = StringField('State/Province', validators=[
        DataRequired(message="Please enter your state or province"),
        Length(min=2, max=50, message="State must be between 2 and 50 characters")
    ])
    
    testator_zip = StringField('ZIP/Postal Code', validators=[
        DataRequired(message="Please enter your ZIP or postal code"),
        Length(min=3, max=20, message="ZIP code must be between 3 and 20 characters")
    ])
    
    testator_country = StringField('Country', validators=[
        DataRequired(message="Please enter your country"),
        Length(min=2, max=100, message="Country must be between 2 and 100 characters")
    ], default="United States")
    
    testator_phone = TelField('Phone Number', validators=[
        Optional(),
        Length(max=20, message="Phone number must be less than 20 characters")
    ], render_kw={"placeholder": "e.g., (555) 123-4567"})
    
    testator_email = EmailField('Email Address', validators=[
        Optional(),
        Email(message="Please enter a valid email address"),
        Length(max=100, message="Email must be less than 100 characters")
    ])
    
    marital_status = SelectField('Marital Status', choices=[
        ('', 'Select marital status'),
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
        ('separated', 'Separated'),
        ('domestic_partnership', 'Domestic Partnership')
    ], validators=[DataRequired(message="Please select your marital status")])
    
    spouse_name = StringField('Spouse/Partner Name', validators=[
        Optional(),
        Length(max=200, message="Spouse name must be less than 200 characters")
    ], render_kw={"placeholder": "Enter spouse or partner's full name (if applicable)"})
    
    def validate_testator_date_of_birth(self, field):
        if field.data and field.data >= date.today():
            raise ValidationError("Date of birth must be in the past")
        if field.data and (date.today() - field.data).days < 6570:  # 18 years
            raise ValidationError("You must be at least 18 years old to create a will")


class BeneficiaryForm(FlaskForm):
    """Individual Beneficiary Form"""
    name = StringField('Full Name', validators=[
        DataRequired(message="Please enter beneficiary's full name"),
        Length(min=2, max=200, message="Name must be between 2 and 200 characters")
    ])
    
    relationship = StringField('Relationship to You', validators=[
        DataRequired(message="Please specify your relationship to this beneficiary"),
        Length(min=2, max=100, message="Relationship must be between 2 and 100 characters")
    ], render_kw={"placeholder": "e.g., Son, Daughter, Friend, Charity"})
    
    address = TextAreaField('Address', validators=[
        Optional(),
        Length(max=500, message="Address must be less than 500 characters")
    ], render_kw={"rows": 2, "placeholder": "Beneficiary's address (optional)"})
    
    percentage = StringField('Percentage of Estate', validators=[
        Optional(),
        Length(max=10, message="Percentage must be less than 10 characters")
    ], render_kw={"placeholder": "e.g., 25% or $10,000"})
    
    specific_bequest = TextAreaField('Specific Items/Instructions', validators=[
        Optional(),
        Length(max=1000, message="Specific bequest must be less than 1000 characters")
    ], render_kw={"rows": 3, "placeholder": "Specific items or instructions for this beneficiary"})
    
    contingent = BooleanField('Contingent Beneficiary', 
                             render_kw={"title": "Check if this is a backup beneficiary"})


class BeneficiariesForm(FlaskForm):
    """Step 2: Beneficiaries Form"""
    beneficiaries = FieldList(FormField(BeneficiaryForm), min_entries=0)


class ExecutorsForm(FlaskForm):
    """Step 3: Executors Form"""
    # Primary Executor
    primary_executor_name = StringField('Primary Executor Full Name', validators=[
        DataRequired(message="Please enter the primary executor's full name"),
        Length(min=2, max=200, message="Name must be between 2 and 200 characters")
    ])
    
    primary_executor_address = TextAreaField('Primary Executor Address', validators=[
        DataRequired(message="Please enter the primary executor's address"),
        Length(min=5, max=500, message="Address must be between 5 and 500 characters")
    ], render_kw={"rows": 2})
    
    primary_executor_relationship = StringField('Relationship to You', validators=[
        DataRequired(message="Please specify your relationship to the primary executor"),
        Length(min=2, max=100, message="Relationship must be between 2 and 100 characters")
    ], render_kw={"placeholder": "e.g., Spouse, Child, Friend, Attorney"})
    
    primary_executor_phone = TelField('Primary Executor Phone', validators=[
        Optional(),
        Length(max=20, message="Phone number must be less than 20 characters")
    ])
    
    primary_executor_email = EmailField('Primary Executor Email', validators=[
        Optional(),
        Email(message="Please enter a valid email address"),
        Length(max=100, message="Email must be less than 100 characters")
    ])
    
    # Alternate Executor
    alternate_executor_name = StringField('Alternate Executor Full Name', validators=[
        Optional(),
        Length(max=200, message="Name must be less than 200 characters")
    ])
    
    alternate_executor_address = TextAreaField('Alternate Executor Address', validators=[
        Optional(),
        Length(max=500, message="Address must be less than 500 characters")
    ], render_kw={"rows": 2})
    
    alternate_executor_relationship = StringField('Relationship to You', validators=[
        Optional(),
        Length(max=100, message="Relationship must be less than 100 characters")
    ])
    
    alternate_executor_phone = TelField('Alternate Executor Phone', validators=[
        Optional(),
        Length(max=20, message="Phone number must be less than 20 characters")
    ])
    
    alternate_executor_email = EmailField('Alternate Executor Email', validators=[
        Optional(),
        Email(message="Please enter a valid email address"),
        Length(max=100, message="Email must be less than 100 characters")
    ])


class AssetForm(FlaskForm):
    """Individual Asset Form"""
    description = StringField('Asset Description', validators=[
        DataRequired(message="Please describe the asset"),
        Length(min=2, max=500, message="Description must be between 2 and 500 characters")
    ])

    value = StringField('Estimated Value', validators=[
        Optional(),
        Length(max=50, message="Value must be less than 50 characters")
    ], render_kw={"placeholder": "e.g., $50,000 or Appraised value"})

    location = StringField('Location/Details', validators=[
        Optional(),
        Length(max=200, message="Location must be less than 200 characters")
    ], render_kw={"placeholder": "Address, account number, or other identifying details"})


class SpecificBequestForm(FlaskForm):
    """Individual Specific Bequest Form"""
    item_description = StringField('Item/Asset Description', validators=[
        DataRequired(message="Please describe the item or asset"),
        Length(min=2, max=500, message="Description must be between 2 and 500 characters")
    ])

    beneficiary_name = StringField('Beneficiary Name', validators=[
        DataRequired(message="Please enter the beneficiary's name"),
        Length(min=2, max=200, message="Name must be between 2 and 200 characters")
    ])

    instructions = TextAreaField('Special Instructions', validators=[
        Optional(),
        Length(max=1000, message="Instructions must be less than 1000 characters")
    ], render_kw={"rows": 2, "placeholder": "Any special conditions or instructions"})


class AssetsDistributionForm(FlaskForm):
    """Step 4: Distribution of Assets Form"""
    # Real Estate
    real_estate_properties = FieldList(FormField(AssetForm), min_entries=0)

    # Bank Accounts
    bank_accounts = FieldList(FormField(AssetForm), min_entries=0)

    # Investments
    investments = FieldList(FormField(AssetForm), min_entries=0)

    # Personal Property
    personal_property = FieldList(FormField(AssetForm), min_entries=0)

    # Other Assets
    other_assets = FieldList(FormField(AssetForm), min_entries=0)

    # Specific Bequests
    specific_bequests = FieldList(FormField(SpecificBequestForm), min_entries=0)

    # Residuary Beneficiary
    residuary_beneficiary = StringField('Residuary Beneficiary', validators=[
        Optional(),
        Length(max=200, message="Beneficiary name must be less than 200 characters")
    ], render_kw={"placeholder": "Who receives the remainder of your estate"})


class CharitableDonationForm(FlaskForm):
    """Individual Charitable Donation Form"""
    charity_name = StringField('Charity/Organization Name', validators=[
        DataRequired(message="Please enter the charity name"),
        Length(min=2, max=200, message="Name must be between 2 and 200 characters")
    ])

    charity_address = TextAreaField('Charity Address', validators=[
        Optional(),
        Length(max=500, message="Address must be less than 500 characters")
    ], render_kw={"rows": 2})

    donation_amount = StringField('Donation Amount/Percentage', validators=[
        Optional(),
        Length(max=50, message="Amount must be less than 50 characters")
    ], render_kw={"placeholder": "e.g., $5,000 or 10% of estate"})

    purpose = TextAreaField('Purpose/Instructions', validators=[
        Optional(),
        Length(max=500, message="Purpose must be less than 500 characters")
    ], render_kw={"rows": 2, "placeholder": "Specific purpose for the donation (optional)"})


class SpecialInstructionsForm(FlaskForm):
    """Step 5: Special Instructions Form"""
    # Funeral and Burial Wishes
    funeral_wishes = TextAreaField('Funeral Service Wishes', validators=[
        Optional(),
        Length(max=1000, message="Funeral wishes must be less than 1000 characters")
    ], render_kw={"rows": 3, "placeholder": "Your preferences for funeral services"})

    burial_cremation_wishes = SelectField('Burial/Cremation Preference', choices=[
        ('', 'Select preference'),
        ('burial', 'Burial'),
        ('cremation', 'Cremation'),
        ('donation', 'Body Donation'),
        ('no_preference', 'No Preference')
    ], validators=[Optional()])

    burial_cremation_details = TextAreaField('Burial/Cremation Details', validators=[
        Optional(),
        Length(max=1000, message="Details must be less than 1000 characters")
    ], render_kw={"rows": 3, "placeholder": "Specific instructions for burial, cremation, or body donation"})

    # Guardian for Minor Children
    guardian_minor_children = StringField('Guardian for Minor Children', validators=[
        Optional(),
        Length(max=200, message="Guardian name must be less than 200 characters")
    ], render_kw={"placeholder": "Full name of proposed guardian"})

    guardian_address = TextAreaField('Guardian Address', validators=[
        Optional(),
        Length(max=500, message="Address must be less than 500 characters")
    ], render_kw={"rows": 2})

    # Special Instructions
    special_instructions = TextAreaField('Additional Special Instructions', validators=[
        Optional(),
        Length(max=2000, message="Special instructions must be less than 2000 characters")
    ], render_kw={"rows": 4, "placeholder": "Any other special instructions or wishes"})

    # Charitable Donations
    charitable_donations = FieldList(FormField(CharitableDonationForm), min_entries=0)


class WillConfirmationForm(FlaskForm):
    """Final confirmation form"""
    confirm_accuracy = BooleanField('I confirm that all information is accurate', validators=[
        DataRequired(message="Please confirm the accuracy of your information")
    ])

    confirm_legal_capacity = BooleanField('I confirm I am of sound mind and legal capacity', validators=[
        DataRequired(message="Please confirm your legal capacity")
    ])

    confirm_understanding = BooleanField('I understand this will revokes all previous wills', validators=[
        DataRequired(message="Please confirm your understanding")
    ])
