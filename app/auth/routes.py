from flask import render_template, redirect, url_for, flash, request, make_response
from flask_login import login_user, logout_user, login_required, current_user
from flask_dance.contrib.google import google
from app.auth import bp
from app.models import db, User


@bp.route('/login')
def login():
    """Login page - handle Google OAuth and user creation."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    # Check if this is a demo login request
    if request.args.get('demo') == 'true':
        return demo_login()

    # Check if we're coming back from Google OAuth
    if google.authorized:
        try:
            # Get user info from Google
            resp = google.get('/oauth2/v2/userinfo')
            if not resp.ok:
                flash('Failed to fetch user info from Google. Please try again.', 'error')
                return redirect(url_for('main.index'))

            google_info = resp.json()
            google_id = google_info.get('id')
            email = google_info.get('email')
            name = google_info.get('name')
            profile_pic = google_info.get('picture', '')

            if not google_id or not email or not name:
                flash('Incomplete user information from Google. Please try again.', 'error')
                return redirect(url_for('main.index'))

            # Check if user exists
            user = User.query.filter_by(google_id=google_id).first()

            if not user:
                # Create new user
                user = User(
                    google_id=google_id,
                    email=email,
                    name=name,
                    profile_pic=profile_pic
                )
                db.session.add(user)
                db.session.commit()
                flash(f'Welcome {name}! Your account has been created.', 'success')
            else:
                # Update existing user info
                user.name = name
                user.email = email
                user.profile_pic = profile_pic
                db.session.commit()
                flash(f'Welcome back, {name}!', 'success')

            # Log the user in
            login_user(user, remember=True)

            # Redirect to dashboard
            return redirect(url_for('main.dashboard'))

        except Exception as e:
            flash('An error occurred during login. Please try again.', 'error')
            print(f"OAuth error: {e}")
            return redirect(url_for('main.index'))

    # If not authorized, redirect to Google OAuth
    return redirect(url_for('google.login'))


@bp.route('/demo-login')
def demo_login():
    """Demo login for testing purposes (remove in production)."""
    # Check if demo user exists
    demo_user = User.query.filter_by(email='demo@willgen.com').first()

    if not demo_user:
        # Create demo user
        demo_user = User(
            google_id='demo_user_123',
            email='demo@willgen.com',
            name='Demo User',
            profile_pic=''
        )
        db.session.add(demo_user)
        db.session.commit()

    login_user(demo_user, remember=True)
    flash('Welcome to the WillGen demo! You can now test the will creation wizard.', 'success')
    return redirect(url_for('main.dashboard'))


@bp.route('/logout')
@login_required
def logout():
    """Logout user completely - clear all sessions and force re-authentication."""
    from flask import session
    from flask_dance.contrib.google import google

    # Clear Flask-Login session first
    logout_user()

    # Try to revoke the OAuth token with Google
    try:
        if google.authorized and google.token:
            revoke_url = 'https://oauth2.googleapis.com/revoke'
            google.post(revoke_url, data={'token': google.token['access_token']})
    except Exception as e:
        print(f"Error revoking token: {e}")

    # Clear all session data completely
    session.clear()

    # Force clear Flask-Dance OAuth data
    try:
        # Remove the OAuth token from session storage
        if 'google_oauth_token' in session:
            del session['google_oauth_token']

        # Clear any Flask-Dance related session keys
        keys_to_remove = []
        for key in session.keys():
            if 'google' in key.lower() or 'oauth' in key.lower() or 'flask_dance' in key.lower():
                keys_to_remove.append(key)

        for key in keys_to_remove:
            session.pop(key, None)

    except Exception as e:
        print(f"Error clearing OAuth storage: {e}")

    # Create a response that aggressively clears everything
    response = make_response(redirect(url_for('main.index')))

    # Clear all possible cookies
    cookie_names = ['session', 'google_oauth_token', 'flask_dance_google', 'remember_token']
    for cookie_name in cookie_names:
        response.set_cookie(cookie_name, '', expires=0, path='/')
        response.set_cookie(cookie_name, '', expires=0, path='/', domain='localhost')
        response.set_cookie(cookie_name, '', expires=0, path='/', domain='.localhost')

    # Add aggressive cache control headers
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    response.headers['Clear-Site-Data'] = '"cache", "cookies", "storage"'

    # Instead of just redirecting, show a logout page that forces a clean state
    response = make_response(render_template('auth/logout_success.html'))

    # Set aggressive headers to prevent any caching
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    response.headers['Clear-Site-Data'] = '"cache", "cookies", "storage", "executionContexts"'

    return response


@bp.route('/force-logout')
def force_logout():
    """Force logout by destroying session completely."""
    from flask import session

    # Nuclear option - destroy everything
    session.clear()
    session.permanent = False

    # Create new session
    session.regenerate()

    response = make_response(redirect(url_for('main.index')))

    # Clear all cookies aggressively
    cookie_names = ['session', 'google_oauth_token', 'flask_dance_google', 'remember_token', '_csrf_token']
    for cookie_name in cookie_names:
        response.set_cookie(cookie_name, '', expires=0, path='/')
        response.set_cookie(cookie_name, '', expires=0, path='/', domain='localhost')
        response.set_cookie(cookie_name, '', expires=0, path='/', domain='.localhost')
        response.set_cookie(cookie_name, '', expires=0, path='/', secure=False, httponly=True)

    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'

    flash('Session completely cleared. Please login again.', 'info')
    return response



