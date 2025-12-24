from flask import Flask, render_template, url_for, request, flash, redirect, session
from flask_wtf import CSRFProtect
from flask_wtf.csrf import generate_csrf
from db.db import *

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


@app.route('/register/', methods=["GET", "POST"])
def register():
    error = None

    if request.method == "POST":
        # Get form data
        username = request.form.get('username')
        password = request.form.get('password')
        repassword = request.form.get('repassword')

        # Validate password match
        if password != repassword:
            error = "Passwords do not match!"

        # Check if username already exists
        elif get_user_by_username(username):
            error = "Username already exists! Please choose a different one."

        # If no errors, create the user
        if error is None:
            create_user(username, password)
            flash(
                f"Registration successful! Welcome {username}!", category='success')
            return redirect(url_for('login'))
        else:
            flash(f"Registration failed: {error}", category='danger')
            return render_template('register.html', title="Register")

    # GET request → show registration page
    return render_template('register.html', title="Sign up")


@app.route('/login/', methods=['GET', 'POST'])
def login():
    error = None

    # If the login request is a POST method
    if request.method == "POST":
        # Get the username and password from the form
        username = request.form.get("username")
        password = request.form.get("password")

        # Validate user credentials
        user = validate_login(username, password)

        if user is None:
            error = 'Invalid username or password!'
        else:
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            # or wherever you want to redirect
            return redirect(url_for('listings'))

    # Render login page with error (if any)
    return render_template('login.html', error=error)

# Logout


@app.route('/logout/')
def logout():
    # Clear the session and redirect to the index page with a flash message
    session.clear()
    flash(category='info', message='You have been logged out.')
    return redirect(url_for('landing'))


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
        return render_template('listing.html', listing_type=listing_data['listing_type'], listing=listing_data)
    else:
        # If film not found, redirect to films list with a flash message
        flash(category='warning', message='Requested film not found!')
        return redirect(url_for('listings'))
# Add A Film Page


@app.route('/create/', methods=('GET', 'POST'))
def create():

    # If the request method is POST, process the form submission
    if request.method == 'POST':

        # Get the type input from the form
        listing_type = request.form['listing_type']

        # Validate the input
        if not listing_type:
            flash(category='danger', message='Listing Type is required!')
            return render_template('create.html')

        # [TO-DO]: Add real creation logic here (e.g. save to database record)
        new_listing = {
            'user': 1,  # test user
            'listing_type': listing_type,
            'postcode': request.form.get('postcode'),
            'listing_details': request.form.get('listing_details', ''),
            'poster': request.form.get('poster', ''),
            'duration': request.form.get('duration', 0),
            'town': request.form.get('town', ''),
            'bills_inclusive': 'bills_inclusive' in request.form,
            'price': request.form.get('price', 0),
        }
        create_listing(new_listing)
        # ===========================

        # Flash a success message
        flash(category='success', message='Created successfully!')
        return redirect(url_for('listings'))

    return render_template('create.html', title="Add A New Listing")


# Edit A Film Page
@app.route('/update/<int:id>/', methods=('GET', 'POST'))
def update(id):
    # Get film data
    listing_data = get_listing_by_id(id)
    if not listing_data:
        flash('Listing not found!', 'warning')
        return redirect(url_for('listings'))

    # If the request method is POST, process the form submission
    if request.method == 'POST':

        # Get the title input from the form
        listing_type = request.form['listing_type']

        # Validate the input
        if not listing_type:
            flash(category='danger', message='Listing Type is required!')
            return render_template('update.html', id=id)

        # [TO-DO]: Add real update logic here (e.g. update database record)
        updated_fields = {
            'listing_type': listing_type,
            'postcode': request.form.get('postcode', ''),
            'listing_details': request.form.get('listing_details', ''),
            'poster': request.form.get('poster', ''),
            'duration': request.form.get('duration', 0),
            'town': request.form.get('town', ''),
            'bills_inclusive': 'bills_inclusive' in request.form,
            'price': request.form.get('price', 0),
        }

        update_listing(id, updated_fields)
        # ===========================

        # Flash a success message
        flash(category='success', message='Updated successfully!')
        return redirect(url_for('listing', id=id))

    return render_template('update.html', title="Update listing", listing=listing_data)

# Delete A Film


@app.route('/delete/<int:id>', methods=('POST',))
def delete(id):

    # [TO-DO]: Add real deletion logic here (e.g. delete database record)
    delete_listing(id)
    # ===========================

    # Flash a success message and redirect to the index page
    flash(category='success', message='Listing deleted successfully!')
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
