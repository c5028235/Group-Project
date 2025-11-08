from flask import Flask, render_template
from flask_wtf import CSRFProtect
from flask_wtf.csrf import generate_csrf


# Create a Flask application instance
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for CSRF protection
csrf = CSRFProtect(app)  # This automatically protects all POST routes


@app.context_processor
def inject_csrf_token():
    return dict(csrf_token=generate_csrf())


# Global variable for site name: Used in templates to display the site name
localSiteName = "Tenancy Takeovers"
# Set the site name in the app context


@app.context_processor
def inject_site_name():
    return dict(siteName=localSiteName)

# Routes
# ===================
# Home Page


@app.route('/')
def home():
    # This defines a variable 'studentName' that will be passed to the output HTML
    studentName = "SHU Student"
    # Render HTML with the name in a H1 tag
    return render_template('home.html', title="Welcome", username=studentName)


@app.route('/about')
def about():
    return render_template('about.html', title="About Page")


@app.route('/register')
def register():
    return render_template('register.html', title="Sign up")


@app.route('/login')
def login():
    return render_template('login.html', title="login")


# Run application
# =========================================================
# This code executes when the script is run directly.
if __name__ == '__main__':
    print("Starting Flask application...")
    print("Open Your Application in Your Browser: http://localhost:81")
    # The app will run on port 81, accessible from any local IP address
    app.run(host='0.0.0.0', port=81)
