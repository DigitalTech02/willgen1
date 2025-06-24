import json
from datetime import datetime, timezone
from flask import render_template, redirect, url_for, flash, request, jsonify, make_response
from flask_login import login_required, current_user
from app.main import bp
from app.models import db, Will
from app.forms import (
    TestatorInfoForm, BeneficiariesForm, ExecutorsForm,
    AssetsDistributionForm, SpecialInstructionsForm, WillConfirmationForm
)


@bp.route('/')
def index():
    """Home page with hero section."""
    return render_template('index.html')


@bp.route('/debug/oauth')
def debug_oauth():
    """Debug route to check OAuth configuration."""
    from flask import current_app
    client_id = current_app.config.get('GOOGLE_OAUTH_CLIENT_ID', 'NOT_SET')
    client_secret = current_app.config.get('GOOGLE_OAUTH_CLIENT_SECRET', 'NOT_SET')

    # Mask the secret for security
    masked_secret = client_secret[:10] + '...' if len(client_secret) > 10 else 'NOT_SET'

    debug_info = {
        'client_id': client_id,
        'client_secret_preview': masked_secret,
        'client_id_valid': client_id.endswith('.apps.googleusercontent.com'),
        'client_secret_valid': client_secret.startswith('GOCSPX-') if client_secret != 'NOT_SET' else False
    }

    return f"""
    <h2>OAuth Debug Information</h2>
    <p><strong>Client ID:</strong> {debug_info['client_id']}</p>
    <p><strong>Client Secret Preview:</strong> {debug_info['client_secret_preview']}</p>
    <p><strong>Client ID Valid:</strong> {debug_info['client_id_valid']}</p>
    <p><strong>Client Secret Valid:</strong> {debug_info['client_secret_valid']}</p>
    <hr>
    <p>If both are valid, your credentials are loaded correctly.</p>
    <p><a href="/">Back to Home</a></p>
    """


@bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard showing all wills."""
    wills = Will.query.filter_by(user_id=current_user.id).order_by(Will.updated_at.desc()).all()
    return render_template('dashboard.html', wills=wills)


@bp.route('/will/create')
@login_required
def create_will():
    """Start creating a new will - redirect to step 1."""
    return redirect(url_for('main.will_wizard', step=1))


@bp.route('/will/demo')
def demo_will():
    """Demo route to test the wizard without authentication."""
    return redirect(url_for('main.will_wizard_demo', step=1))


@bp.route('/will/demo/<int:step>')
def will_wizard_demo(step):
    """Demo multi-step will creation wizard (no auth required)."""
    # This is a demo route for testing - remove in production
    if step < 1 or step > 6:
        return redirect(url_for('main.demo_will'))

    # Create a mock will object for demo
    class MockWill:
        def __init__(self):
            self.id = 1
            self.title = "Demo Will"
            self.testator_name = ""
            self.testator_date_of_birth = None
            self.testator_address = ""
            self.testator_city = ""
            self.testator_state = ""
            self.testator_zip = ""
            self.testator_country = "United States"
            self.testator_phone = ""
            self.testator_email = ""
            self.marital_status = ""
            self.spouse_name = ""
            self.beneficiaries = ""
            self.primary_executor_name = ""
            self.primary_executor_address = ""
            self.primary_executor_relationship = ""
            self.primary_executor_phone = ""
            self.primary_executor_email = ""
            self.alternate_executor_name = ""
            self.alternate_executor_address = ""
            self.alternate_executor_relationship = ""
            self.alternate_executor_phone = ""
            self.alternate_executor_email = ""
            self.real_estate_properties = ""
            self.bank_accounts = ""
            self.investments = ""
            self.personal_property = ""
            self.other_assets = ""
            self.specific_bequests = ""
            self.residuary_beneficiary = ""
            self.funeral_wishes = ""
            self.burial_cremation_wishes = ""
            self.guardian_minor_children = ""
            self.guardian_address = ""
            self.special_instructions = ""
            self.charitable_donations = ""
            self.current_step = step
            self.step_1_completed = False
            self.step_2_completed = False
            self.step_3_completed = False
            self.step_4_completed = False
            self.step_5_completed = False
            self.is_completed = False

    mock_will = MockWill()

    # Import forms
    from app.forms import (
        TestatorInfoForm, BeneficiariesForm, ExecutorsForm,
        AssetsDistributionForm, SpecialInstructionsForm, WillConfirmationForm
    )

    # Route to appropriate step template
    if step == 1:
        form = TestatorInfoForm()
        return render_template('will/wizard/step1_testator.html',
                             form=form, will=mock_will, current_step=1)
    elif step == 2:
        form = BeneficiariesForm()
        return render_template('will/wizard/step2_beneficiaries.html',
                             form=form, will=mock_will, current_step=2)
    elif step == 3:
        form = ExecutorsForm()
        return render_template('will/wizard/step3_executors.html',
                             form=form, will=mock_will, current_step=3)
    elif step == 4:
        form = AssetsDistributionForm()
        return render_template('will/wizard/step4_assets.html',
                             form=form, will=mock_will, current_step=4)
    elif step == 5:
        form = SpecialInstructionsForm()
        return render_template('will/wizard/step5_special.html',
                             form=form, will=mock_will, current_step=5)
    elif step == 6:
        form = WillConfirmationForm()
        return render_template('will/wizard/step6_confirmation.html',
                             form=form, will=mock_will, current_step=6)


@bp.route('/will/wizard/<int:step>', methods=['GET', 'POST'])
@bp.route('/will/wizard/<int:step>/<int:will_id>', methods=['GET', 'POST'])
@login_required
def will_wizard(step, will_id=None):
    """Multi-step will creation wizard."""
    # Validate step number
    if step < 1 or step > 6:
        flash('Invalid step number.', 'error')
        return redirect(url_for('main.create_will'))

    # Get or create will
    if will_id:
        will = Will.query.filter_by(id=will_id, user_id=current_user.id).first()
        if not will:
            flash('Will not found.', 'error')
            return redirect(url_for('main.dashboard'))
    else:
        # Check if there's an existing draft will
        will = Will.query.filter_by(user_id=current_user.id, is_completed=False).first()
        if not will:
            # Create new will
            will = Will(
                user_id=current_user.id,
                title=f"{current_user.name}'s Will",
                current_step=1
            )
            db.session.add(will)
            db.session.commit()

    # Route to appropriate step handler
    if step == 1:
        return handle_testator_info(will)
    elif step == 2:
        return handle_beneficiaries(will)
    elif step == 3:
        return handle_executors(will)
    elif step == 4:
        return handle_assets_distribution(will)
    elif step == 5:
        return handle_special_instructions(will)
    elif step == 6:
        return handle_confirmation(will)


def handle_testator_info(will):
    """Handle Step 1: Testator Information."""
    form = TestatorInfoForm()

    if form.validate_on_submit():
        # Save form data to will
        will.title = form.title.data
        will.testator_name = form.testator_name.data
        will.testator_date_of_birth = form.testator_date_of_birth.data
        will.testator_address = form.testator_address.data
        will.testator_city = form.testator_city.data
        will.testator_state = form.testator_state.data
        will.testator_zip = form.testator_zip.data
        will.testator_country = form.testator_country.data
        will.testator_phone = form.testator_phone.data
        will.testator_email = form.testator_email.data
        will.marital_status = form.marital_status.data
        will.spouse_name = form.spouse_name.data
        will.step_1_completed = True
        will.current_step = max(will.current_step, 2)
        will.updated_at = datetime.now(timezone.utc)

        db.session.commit()
        flash('Testator information saved successfully!', 'success')
        return redirect(url_for('main.will_wizard', step=2, will_id=will.id))

    # Pre-populate form with existing data
    if will.testator_name:
        form.title.data = will.title
        form.testator_name.data = will.testator_name
        form.testator_date_of_birth.data = will.testator_date_of_birth
        form.testator_address.data = will.testator_address
        form.testator_city.data = will.testator_city
        form.testator_state.data = will.testator_state
        form.testator_zip.data = will.testator_zip
        form.testator_country.data = will.testator_country
        form.testator_phone.data = will.testator_phone
        form.testator_email.data = will.testator_email
        form.marital_status.data = will.marital_status
        form.spouse_name.data = will.spouse_name

    return render_template('will/wizard/step1_testator.html',
                         form=form, will=will, current_step=1)


def handle_beneficiaries(will):
    """Handle Step 2: Beneficiaries."""
    from flask import request

    if request.method == 'POST':
        # Get form data directly from request
        beneficiary_name = request.form.get('beneficiary-name', '').strip()
        beneficiary_relationship = request.form.get('beneficiary-relationship', '').strip()
        beneficiary_percentage = request.form.get('beneficiary-percentage', '').strip()
        beneficiary_address = request.form.get('beneficiary-address', '').strip()
        beneficiary_bequest = request.form.get('beneficiary-bequest', '').strip()
        beneficiary_contingent = 'beneficiary-contingent' in request.form

        # Basic validation
        if not beneficiary_name:
            flash('Please provide the beneficiary name.', 'error')
            return render_template('will/wizard/step2_beneficiaries.html',
                                 form=None, will=will, current_step=2)

        # Save beneficiary data
        beneficiaries_data = [{
            'name': beneficiary_name,
            'relationship': beneficiary_relationship,
            'address': beneficiary_address,
            'percentage': beneficiary_percentage,
            'specific_bequest': beneficiary_bequest,
            'contingent': beneficiary_contingent
        }]

        will.beneficiaries = json.dumps(beneficiaries_data)
        will.step_2_completed = True
        will.current_step = max(will.current_step, 3)
        will.updated_at = datetime.now(timezone.utc)

        db.session.commit()
        flash('Beneficiaries information saved successfully!', 'success')
        return redirect(url_for('main.will_wizard', step=3, will_id=will.id))

    # For GET requests, create a simple form object for CSRF protection
    form = BeneficiariesForm()

    # Pre-populate form data if it exists
    beneficiary_data = {}
    if will.beneficiaries:
        try:
            beneficiaries_data = json.loads(will.beneficiaries)
            if beneficiaries_data and len(beneficiaries_data) > 0:
                beneficiary_data = beneficiaries_data[0]  # Get first beneficiary
        except (json.JSONDecodeError, AttributeError, IndexError):
            pass

    return render_template('will/wizard/step2_beneficiaries.html',
                         form=form, will=will, current_step=2,
                         beneficiary_data=beneficiary_data)


@bp.route('/will/view/<int:will_id>')
@login_required
def view_will(will_id):
    """Display a completed will as a formatted, printable document."""
    will = Will.query.filter_by(id=will_id, user_id=current_user.id).first_or_404()

    # Additional security check
    if will.user_id != current_user.id:
        flash('You do not have permission to view this will.', 'error')
        return redirect(url_for('main.dashboard'))

    # Parse JSON data for each section
    testator_data = {}
    beneficiaries_data = []
    executors_data = []
    assets_data = {}
    special_instructions_data = {}

    # Build testator data from individual fields
    testator_data = {
        'name': will.testator_name,
        'date_of_birth': will.testator_date_of_birth.strftime('%B %d, %Y') if will.testator_date_of_birth else None,
        'age': None,  # Calculate if needed
        'address': f"{will.testator_address}, {will.testator_city}, {will.testator_state} {will.testator_zip}" if will.testator_address else None,
        'marital_status': will.marital_status,
        'spouse_name': will.spouse_name,
        'phone': will.testator_phone,
        'email': will.testator_email
    }

    try:
        if will.beneficiaries:
            beneficiaries_data = json.loads(will.beneficiaries)
    except (json.JSONDecodeError, TypeError):
        pass

    # Build executors data from individual fields
    executors_data = []
    if will.primary_executor_name:
        executors_data.append({
            'name': will.primary_executor_name,
            'relationship': will.primary_executor_relationship,
            'address': will.primary_executor_address,
            'phone': will.primary_executor_phone,
            'email': will.primary_executor_email,
            'alternate': False
        })

    if will.alternate_executor_name:
        executors_data.append({
            'name': will.alternate_executor_name,
            'relationship': will.alternate_executor_relationship,
            'address': will.alternate_executor_address,
            'phone': will.alternate_executor_phone,
            'email': will.alternate_executor_email,
            'alternate': True
        })

    # Build assets data from individual fields
    assets_data = {}

    try:
        if will.real_estate_properties:
            assets_data['real_estate'] = json.loads(will.real_estate_properties)
    except (json.JSONDecodeError, TypeError):
        pass

    try:
        if will.bank_accounts:
            assets_data['bank_accounts'] = json.loads(will.bank_accounts)
    except (json.JSONDecodeError, TypeError):
        pass

    try:
        if will.investments:
            assets_data['investments'] = json.loads(will.investments)
    except (json.JSONDecodeError, TypeError):
        pass

    try:
        if will.personal_property:
            assets_data['personal_property'] = json.loads(will.personal_property)
    except (json.JSONDecodeError, TypeError):
        pass

    try:
        if will.other_assets:
            assets_data['other_assets'] = json.loads(will.other_assets)
    except (json.JSONDecodeError, TypeError):
        pass

    if will.residuary_beneficiary:
        assets_data['residuary_beneficiary'] = will.residuary_beneficiary

    # Build special instructions data from individual fields
    special_instructions_data = {
        'funeral_wishes': will.funeral_wishes,
        'burial_cremation_wishes': will.burial_cremation_wishes,
        'guardian_minor_children': will.guardian_minor_children,
        'guardian_address': will.guardian_address,
        'additional_instructions': will.special_instructions
    }

    # Parse charitable donations JSON
    try:
        if will.charitable_donations:
            special_instructions_data['charitable_donations'] = json.loads(will.charitable_donations)
    except (json.JSONDecodeError, TypeError):
        pass

    return render_template('will/view.html',
                         will=will,
                         testator_data=testator_data,
                         beneficiaries_data=beneficiaries_data,
                         executors_data=executors_data,
                         assets_data=assets_data,
                         special_instructions_data=special_instructions_data,
                         current_date=datetime.now())


@bp.route('/will/download/<int:will_id>')
@login_required
def download_will_pdf(will_id):
    """Generate and download a PDF of the will."""
    import io

    will = Will.query.filter_by(id=will_id, user_id=current_user.id).first_or_404()

    # Additional security check
    if will.user_id != current_user.id:
        flash('You do not have permission to download this will.', 'error')
        return redirect(url_for('main.dashboard'))

    # Check if will has sufficient data for PDF generation
    if not will.testator_name:
        flash('This will does not have sufficient information for PDF generation.', 'warning')
        return redirect(url_for('main.view_will', will_id=will_id))

    # Parse JSON data for each section (same as view_will)
    testator_data = {}
    beneficiaries_data = []
    executors_data = []
    assets_data = {}
    special_instructions_data = {}

    # Build testator data from individual fields
    testator_data = {
        'name': will.testator_name,
        'date_of_birth': will.testator_date_of_birth.strftime('%B %d, %Y') if will.testator_date_of_birth else None,
        'age': None,  # Calculate if needed
        'address': f"{will.testator_address}, {will.testator_city}, {will.testator_state} {will.testator_zip}" if will.testator_address else None,
        'marital_status': will.marital_status,
        'spouse_name': will.spouse_name,
        'phone': will.testator_phone,
        'email': will.testator_email
    }

    try:
        if will.beneficiaries:
            beneficiaries_data = json.loads(will.beneficiaries)
    except (json.JSONDecodeError, TypeError):
        pass

    # Build executors data from individual fields
    executors_data = []
    if will.primary_executor_name:
        executors_data.append({
            'name': will.primary_executor_name,
            'relationship': will.primary_executor_relationship,
            'address': will.primary_executor_address,
            'phone': will.primary_executor_phone,
            'email': will.primary_executor_email,
            'alternate': False
        })

    if will.alternate_executor_name:
        executors_data.append({
            'name': will.alternate_executor_name,
            'relationship': will.alternate_executor_relationship,
            'address': will.alternate_executor_address,
            'phone': will.alternate_executor_phone,
            'email': will.alternate_executor_email,
            'alternate': True
        })

    # Build assets data from individual fields
    assets_data = {}

    try:
        if will.real_estate_properties:
            assets_data['real_estate'] = json.loads(will.real_estate_properties)
    except (json.JSONDecodeError, TypeError):
        pass

    try:
        if will.bank_accounts:
            assets_data['bank_accounts'] = json.loads(will.bank_accounts)
    except (json.JSONDecodeError, TypeError):
        pass

    try:
        if will.investments:
            assets_data['investments'] = json.loads(will.investments)
    except (json.JSONDecodeError, TypeError):
        pass

    try:
        if will.personal_property:
            assets_data['personal_property'] = json.loads(will.personal_property)
    except (json.JSONDecodeError, TypeError):
        pass

    try:
        if will.other_assets:
            assets_data['other_assets'] = json.loads(will.other_assets)
    except (json.JSONDecodeError, TypeError):
        pass

    if will.residuary_beneficiary:
        assets_data['residuary_beneficiary'] = will.residuary_beneficiary

    # Build special instructions data from individual fields
    special_instructions_data = {
        'funeral_wishes': will.funeral_wishes,
        'burial_cremation_wishes': will.burial_cremation_wishes,
        'guardian_minor_children': will.guardian_minor_children,
        'guardian_address': will.guardian_address,
        'additional_instructions': will.special_instructions
    }

    # Parse charitable donations JSON
    try:
        if will.charitable_donations:
            special_instructions_data['charitable_donations'] = json.loads(will.charitable_donations)
    except (json.JSONDecodeError, TypeError):
        pass

    # Create a PDF-specific template (without action buttons)
    html_content = render_template('will/pdf_template.html',
                                 will=will,
                                 testator_data=testator_data,
                                 beneficiaries_data=beneficiaries_data,
                                 executors_data=executors_data,
                                 assets_data=assets_data,
                                 special_instructions_data=special_instructions_data,
                                 current_date=datetime.now())

    # Generate PDF using xhtml2pdf
    try:
        from xhtml2pdf import pisa

        pdf_buffer = io.BytesIO()

        # Convert HTML to PDF
        pisa_status = pisa.CreatePDF(html_content, dest=pdf_buffer)

        if pisa_status.err:
            flash('Error generating PDF: PDF creation failed', 'error')
            return redirect(url_for('main.view_will', will_id=will_id))

        pdf_buffer.seek(0)

        # Create response
        response = make_response(pdf_buffer.read())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename="Will_{will.testator_name or "Document"}_{datetime.now().strftime("%Y%m%d")}.pdf"'

        return response

    except Exception as e:
        flash(f'Error generating PDF: {str(e)}', 'error')
        return redirect(url_for('main.view_will', will_id=will_id))


def handle_executors(will):
    """Handle Step 3: Executors."""
    form = ExecutorsForm()

    if form.validate_on_submit():
        # Save executor information
        will.primary_executor_name = form.primary_executor_name.data
        will.primary_executor_address = form.primary_executor_address.data
        will.primary_executor_relationship = form.primary_executor_relationship.data
        will.primary_executor_phone = form.primary_executor_phone.data
        will.primary_executor_email = form.primary_executor_email.data

        will.alternate_executor_name = form.alternate_executor_name.data
        will.alternate_executor_address = form.alternate_executor_address.data
        will.alternate_executor_relationship = form.alternate_executor_relationship.data
        will.alternate_executor_phone = form.alternate_executor_phone.data
        will.alternate_executor_email = form.alternate_executor_email.data

        will.step_3_completed = True
        will.current_step = max(will.current_step, 4)
        will.updated_at = datetime.now(timezone.utc)

        db.session.commit()
        flash('Executor information saved successfully!', 'success')
        return redirect(url_for('main.will_wizard', step=4, will_id=will.id))

    # Pre-populate form with existing data
    if will.primary_executor_name:
        form.primary_executor_name.data = will.primary_executor_name
        form.primary_executor_address.data = will.primary_executor_address
        form.primary_executor_relationship.data = will.primary_executor_relationship
        form.primary_executor_phone.data = will.primary_executor_phone
        form.primary_executor_email.data = will.primary_executor_email

        form.alternate_executor_name.data = will.alternate_executor_name
        form.alternate_executor_address.data = will.alternate_executor_address
        form.alternate_executor_relationship.data = will.alternate_executor_relationship
        form.alternate_executor_phone.data = will.alternate_executor_phone
        form.alternate_executor_email.data = will.alternate_executor_email

    return render_template('will/wizard/step3_executors.html',
                         form=form, will=will, current_step=3)


def handle_assets_distribution(will):
    """Handle Step 4: Assets Distribution."""
    form = AssetsDistributionForm()

    if form.validate_on_submit():
        # Save assets data as JSON
        real_estate_data = []
        for asset_form in form.real_estate_properties:
            if asset_form.description.data:
                real_estate_data.append({
                    'description': asset_form.description.data,
                    'value': asset_form.value.data,
                    'location': asset_form.location.data
                })

        bank_accounts_data = []
        for asset_form in form.bank_accounts:
            if asset_form.description.data:
                bank_accounts_data.append({
                    'description': asset_form.description.data,
                    'value': asset_form.value.data,
                    'location': asset_form.location.data
                })

        investments_data = []
        for asset_form in form.investments:
            if asset_form.description.data:
                investments_data.append({
                    'description': asset_form.description.data,
                    'value': asset_form.value.data,
                    'location': asset_form.location.data
                })

        personal_property_data = []
        for asset_form in form.personal_property:
            if asset_form.description.data:
                personal_property_data.append({
                    'description': asset_form.description.data,
                    'value': asset_form.value.data,
                    'location': asset_form.location.data
                })

        other_assets_data = []
        for asset_form in form.other_assets:
            if asset_form.description.data:
                other_assets_data.append({
                    'description': asset_form.description.data,
                    'value': asset_form.value.data,
                    'location': asset_form.location.data
                })

        specific_bequests_data = []
        for bequest_form in form.specific_bequests:
            if bequest_form.item_description.data:
                specific_bequests_data.append({
                    'item_description': bequest_form.item_description.data,
                    'beneficiary_name': bequest_form.beneficiary_name.data,
                    'instructions': bequest_form.instructions.data
                })

        will.real_estate_properties = json.dumps(real_estate_data)
        will.bank_accounts = json.dumps(bank_accounts_data)
        will.investments = json.dumps(investments_data)
        will.personal_property = json.dumps(personal_property_data)
        will.other_assets = json.dumps(other_assets_data)
        will.specific_bequests = json.dumps(specific_bequests_data)
        will.residuary_beneficiary = form.residuary_beneficiary.data

        will.step_4_completed = True
        will.current_step = max(will.current_step, 5)
        will.updated_at = datetime.now(timezone.utc)

        db.session.commit()
        flash('Assets distribution information saved successfully!', 'success')
        return redirect(url_for('main.will_wizard', step=5, will_id=will.id))

    # Pre-populate form with existing data
    # (Implementation would be similar to beneficiaries, loading from JSON)

    return render_template('will/wizard/step4_assets.html',
                         form=form, will=will, current_step=4)


def handle_special_instructions(will):
    """Handle Step 5: Special Instructions."""
    form = SpecialInstructionsForm()

    if form.validate_on_submit():
        # Save special instructions
        will.funeral_wishes = form.funeral_wishes.data
        will.burial_cremation_wishes = form.burial_cremation_wishes.data
        will.guardian_minor_children = form.guardian_minor_children.data
        will.guardian_address = form.guardian_address.data
        will.special_instructions = form.special_instructions.data

        # Save charitable donations as JSON
        charitable_donations_data = []
        for donation_form in form.charitable_donations:
            if donation_form.charity_name.data:
                charitable_donations_data.append({
                    'charity_name': donation_form.charity_name.data,
                    'charity_address': donation_form.charity_address.data,
                    'donation_amount': donation_form.donation_amount.data,
                    'purpose': donation_form.purpose.data
                })

        will.charitable_donations = json.dumps(charitable_donations_data)
        will.step_5_completed = True
        will.current_step = max(will.current_step, 6)
        will.updated_at = datetime.now(timezone.utc)

        db.session.commit()
        flash('Special instructions saved successfully!', 'success')
        return redirect(url_for('main.will_wizard', step=6, will_id=will.id))

    # Pre-populate form with existing data
    if will.funeral_wishes:
        form.funeral_wishes.data = will.funeral_wishes
        form.burial_cremation_wishes.data = will.burial_cremation_wishes
        form.guardian_minor_children.data = will.guardian_minor_children
        form.guardian_address.data = will.guardian_address
        form.special_instructions.data = will.special_instructions

    return render_template('will/wizard/step5_special.html',
                         form=form, will=will, current_step=5)


def handle_confirmation(will):
    """Handle Step 6: Confirmation and Final Submission."""
    form = WillConfirmationForm()

    if form.validate_on_submit():
        # Mark will as completed
        will.is_completed = True
        will.updated_at = datetime.now(timezone.utc)

        db.session.commit()
        flash('Your will has been completed successfully! You can now view, print, or download your will.', 'success')
        return redirect(url_for('main.view_will', will_id=will.id))

    return render_template('will/wizard/step6_confirmation.html',
                         form=form, will=will, current_step=6)


@bp.route('/will/save', methods=['POST'])
@login_required
def save_will():
    """Save or update a will."""
    data = request.get_json()
    
    will_id = data.get('id')
    
    if will_id:
        # Update existing will
        will = Will.query.filter_by(id=will_id, user_id=current_user.id).first()
        if not will:
            return jsonify({'error': 'Will not found'}), 404
    else:
        # Create new will
        will = Will(user_id=current_user.id)
        db.session.add(will)
    
    # Update will fields
    will.title = data.get('title', 'Untitled Will')
    will.testator_name = data.get('testator_name', '')
    will.testator_address = data.get('testator_address', '')
    will.testator_city = data.get('testator_city', '')
    will.testator_state = data.get('testator_state', '')
    will.testator_zip = data.get('testator_zip', '')
    will.executor_name = data.get('executor_name', '')
    will.executor_address = data.get('executor_address', '')
    will.executor_relationship = data.get('executor_relationship', '')
    will.beneficiaries = json.dumps(data.get('beneficiaries', []))
    will.assets_description = data.get('assets_description', '')
    will.specific_bequests = data.get('specific_bequests', '')
    will.is_completed = data.get('is_completed', False)
    will.updated_at = datetime.now(timezone.utc)
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'will_id': will.id,
        'message': 'Will saved successfully'
    })


@bp.route('/will/edit/<int:will_id>')
@login_required
def edit_will(will_id):
    """Edit an existing will."""
    will = Will.query.filter_by(id=will_id, user_id=current_user.id).first()
    if not will:
        flash('Will not found.', 'error')
        return redirect(url_for('main.dashboard'))
    
    # Parse beneficiaries JSON
    try:
        beneficiaries = json.loads(will.beneficiaries) if will.beneficiaries else []
    except json.JSONDecodeError:
        beneficiaries = []
    
    return render_template('will/edit.html', will=will, beneficiaries=beneficiaries)


@bp.route('/will/delete/<int:will_id>', methods=['POST'])
@login_required
def delete_will(will_id):
    """Delete a will."""
    will = Will.query.filter_by(id=will_id, user_id=current_user.id).first()
    if not will:
        return jsonify({'error': 'Will not found'}), 404
    
    db.session.delete(will)
    db.session.commit()
    
    flash('Will deleted successfully.', 'success')
    return jsonify({'success': True})



