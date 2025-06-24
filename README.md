# WillGen - Digital Will Generator

A secure, user-friendly Flask web application for creating and managing digital wills with Google OAuth authentication.

## Features

- 🔐 **Secure Authentication**: Google OAuth integration using Flask-Dance
- 📝 **Step-by-Step Will Creation**: Guided form process for creating comprehensive wills
- 👥 **User Isolation**: Each user's data is completely isolated and secure
- 📄 **PDF Generation**: Professional PDF documents ready for legal use
- 💾 **Draft Management**: Save, edit, and manage multiple will drafts
- 📱 **Responsive Design**: Modern Bootstrap 5 interface that works on all devices
- 🏗️ **Clean Architecture**: Well-structured code using Flask Blueprints

## Technology Stack

- **Backend**: Flask 2.3.3
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Flask-Login + Flask-Dance (Google OAuth)
- **Frontend**: Bootstrap 5, HTML5, JavaScript
- **PDF Generation**: ReportLab
- **Environment**: Python 3.8+

## Project Structure

```
willgen/
├── app/
│   ├── __init__.py              # Application factory
│   ├── models.py                # Database models
│   ├── auth/                    # Authentication blueprint
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── main/                    # Main application blueprint
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── templates/               # Jinja2 templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── dashboard.html
│   │   ├── auth/
│   │   └── will/
│   └── static/                  # Static assets
│       ├── css/
│       ├── js/
│       └── img/
├── config.py                    # Configuration settings
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── run.py                       # Application entry point
└── README.md                    # This file
```

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

### 1. Clone the Repository

```bash
git clone <repository-url>
cd willgen
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Google OAuth

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google+ API
4. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client IDs"
5. Set application type to "Web application"
6. Add authorized redirect URIs:
   - `http://localhost:5000/auth/google/authorized`
   - `http://127.0.0.1:5000/auth/google/authorized`
7. Copy the Client ID and Client Secret

### 5. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your actual values
# Windows: notepad .env
# macOS/Linux: nano .env
```

Update the `.env` file with your Google OAuth credentials:

```env
FLASK_ENV=development
FLASK_CONFIG=development
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=sqlite:///app.db
GOOGLE_OAUTH_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=your-google-client-secret
OAUTHLIB_INSECURE_TRANSPORT=True
PORT=5000
```

### 6. Initialize Database

The database will be automatically created when you first run the application.

### 7. Run the Application

```bash
python run.py
```

The application will be available at: `http://localhost:5000`

## Usage

### First Time Setup

1. Open your browser and navigate to `http://localhost:5000`
2. Click "Login with Google" to authenticate
3. Grant the necessary permissions
4. You'll be redirected to your dashboard

### Creating a Will

1. From the dashboard, click "Create New Will"
2. Follow the step-by-step process:
   - **Step 1**: Enter your personal information
   - **Step 2**: Specify executor details
   - **Step 3**: Add beneficiaries
   - **Step 4**: Describe assets and specific bequests
3. Save your will as a draft or mark it as completed

### Managing Wills

- **Edit**: Click the pencil icon to modify an existing will
- **Download**: Generate and download a PDF version (for completed wills)
- **Delete**: Remove a will permanently

## Development

### Running in Development Mode

```bash
# Set environment variables
set FLASK_ENV=development  # Windows
export FLASK_ENV=development  # macOS/Linux

# Run with debug mode
python run.py
```

### Code Structure

- **Blueprints**: The application uses Flask Blueprints for modular organization
- **Models**: Database models are defined in `app/models.py`
- **Templates**: Jinja2 templates with Bootstrap 5 styling
- **Static Assets**: CSS and JavaScript files for enhanced user experience

## Security Features

- **OAuth Authentication**: Secure Google OAuth integration
- **User Isolation**: Each user can only access their own wills
- **CSRF Protection**: Built-in Flask-WTF CSRF protection
- **Secure Sessions**: Flask-Login session management
- **Input Validation**: Server-side and client-side form validation

## Deployment

### Environment Variables for Production

```env
FLASK_ENV=production
FLASK_CONFIG=production
SECRET_KEY=your-production-secret-key
DATABASE_URL=your-production-database-url
GOOGLE_OAUTH_CLIENT_ID=your-production-client-id
GOOGLE_OAUTH_CLIENT_SECRET=your-production-client-secret
OAUTHLIB_INSECURE_TRANSPORT=False
```

### Production Considerations

- Use a production-grade database (PostgreSQL, MySQL)
- Set up proper SSL/TLS certificates
- Configure a reverse proxy (Nginx, Apache)
- Use a WSGI server (Gunicorn, uWSGI)
- Set up proper logging and monitoring

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any issues or have questions:

1. Check the existing issues on GitHub
2. Create a new issue with detailed information
3. Include error messages and steps to reproduce

## Disclaimer

This application generates will documents for informational purposes. Always consult with a qualified attorney to ensure your will meets all legal requirements in your jurisdiction.
