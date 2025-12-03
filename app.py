from flask import Flask, render_template, url_for, request, flash, redirect
from flask_wtf import CSRFProtect
from flask_wtf.csrf import generate_csrf
from db.db import get_all_listings, get_listing_by_id

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
    return render_template('landing.html', title="Welcome", username=studentName)

# about page


@app.route('/about')
def about():
    return render_template('about.html', title="About Page")

# register page


@app.route('/register/', methods=("GET", "POST"))
def register():
    if request.method == "POST":

        # get the username and password from the form
        username = request.form['username']
        password = request.form['password']
        repassword = request.form['repassword']

        # Simple validation checks
        error = None
        if not username:
            error = "Username is required!"
        elif not password or not repassword:
            error = "Password is required!"
        elif password != repassword:
            error = "Passwords do not match"

        # Check if username already exists
        # if get_user_by_username(username):
        #     error = 'Username already exists! Please choose a different one.'

        # display appropriate flash messages
        if error is None:
            flash(category="success",
                  message=f"Account created succesfully! Well done {username}")
            return redirect(url_for('login'))
        else:
            flash(category="danger", message=f"Registration failed: {error}")
            return render_template('register.html', title="Register")

    # if it's GET request, just render the registration page
    return render_template('register.html', title="Sign up")


@app.route('/login/')
def login():
    # if the login requeust is a POST Method
    if request.method == "POST":
        # get the username and password from the form
        username = request.form["username"]
        password = request.form["password"]

        # Simple validation checks
        if not username:
            error = "Username is required!"
        elif not password:
            error = "Password is required!"

        # Validate user credentials
        # if error is None:
        #     user = validate_login(username, password)
        #     if user is None:
        #         error = 'Invalid username or password!'
        #     else:
        #         session.clear()
        #         session['user_id'] = user['id']
        #         session['username'] = user['username']

        # dispaly appropriate flash messages
        if error is None:
            flash(category='success',
                  message=f'login successful. Welcome {username}')
        else:
            flash(category='danger', message=f'login failed: {error}')
    return render_template('login.html', title="Log In")

# listings page


@app.route('/listings/')
def listings():
    # get all listings
    tenancy_list = get_all_listings()
    return render_template('listings.html', title='All Listings', listings=tenancy_list)

# Film Detail Page


@app.route('/listing/<int:id>/')
def listing(id):

    # Get film data
    listing_data = get_listing_by_id(id)

    if listing_data:
        return render_template('listings.html', title=listing_data['title'], film=listing_data)
    else:
        # If film not found, redirect to films list with a flash message
        flash(category='warning', message='Requested film not found!')
        return redirect(url_for('listings'))


@app.route('/profile/')
def profile():
    return render_template('profile.html', title='Your Account')


# Run application
# =========================================================
# This code executes when the script is run directly.
if __name__ == '__main__':
    print("Starting Flask application...")
    print("Open Your Application in Your Browser: http://localhost:81")
    # The app will run on port 81, accessible from any local IP address
    app.run(host='0.0.0.0', port=81)
