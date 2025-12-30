from flask import Flask, render_template, url_for, request, flash, redirect, session
from flask_wtf import CSRFProtect
from flask_wtf.csrf import generate_csrf
from db.db import *

# Create a Flask application instance
app = Flask(__name__)
# Allowed image extensions for uploads
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

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

# Helper function to get a username by user ID and provide it to templates
# eg: {{ film['user']|get_username }})


@app.template_filter()
def get_username(user_id):
    user = get_user_by_id(user_id)
    return user['username'] if user else 'Unknown'

# Routes
# ===================
# Home Page


@app.route('/')
def landing():
    # This defines a variable 'studentName' that will be passed to the output HTML
    studentName = "SHU Student"
    # If a ‘username’ exists in the session data, use this instead
    if 'username' in session:
        studentName = session['username']

    # Get a list of listings to display on the homepage
    # Fetch the latest 5 listings added
    listings = get_all_listings(limit=5, order_by='created DESC')

    # Render the 'index.html' template and pass the 'name' variable to it and a title to set the page title dynamically
    return render_template('landing.html', title="Welcome", username=studentName, listings=listings)


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
    # Get the logged-in user's ID from the session
    user_id = session.get('user_id')

    # Ensure user is logged in to view films
    if user_id is None:
        flash(category='warning', message='You must be logged in to view this page.')
        return redirect(url_for('login'))

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
        # If film not found, redirect to listings list with a flash message
        flash(category='warning', message='Requested listings not found!')
        return redirect(url_for('listings'))

# Users listings List Page


@app.route('/listings/<int:user_id>/')
def userlistings(user_id):

    # Get listing data
    listing_list = get_all_listings(user_id)

    # Get user info
    user = get_user_by_id(user_id)

    # Render the listing.html template with a list of listings
    return render_template('listings.html', title=f"listings added by {user['username']}", listings=listing_list, listings_user=user_id)


# Add A Film Page
@app.route('/create/', methods=('GET', 'POST'))
def create():

    # Get the logged-in user's ID from the session
    user = session.get('user_id')
    # Ensure user is logged in to add films
    if user is None:
        flash(category='warning', message='You must be logged in to add a film.')
        return redirect(url_for('login'))

    # If the request method is POST, process the form submission
    if request.method == 'POST':

        # Get the type input from the form
        listing_type = request.form['listing_type']
        postcode = request.form['postcode']
        listing_details = request.form['listing_details']

        # Handle poster image upload
        poster = None
        if 'poster' in request.files:
            poster_file = request.files['poster']
            # Check it is an image file and save it
            if poster_file and poster_file.filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS:
                # Save the file to the static/uploads directory
                poster_url = f"/static/uploads/{poster_file.filename}"
                poster_file.save(f".{poster_url}")
                poster = poster_url  # Use the uploaded file URL in database

        duration = request.form['duration']
        town = request.form['town']
        price = request.form['price']

        # Validate the input
        if not listing_type:
            flash(category='danger', message='Listing Type is required!')
            return redirect(url_for('create'))

        # Use the database function to insert new listing
        create_listing(user, listing_type, postcode,
                       listing_details, poster, duration, town, price)
        # ===========================

        # Flash a success message
        flash(category='success', message='Listing Created successfully!')
        return redirect(url_for('listings'))

    return render_template('create.html', title="Add A New Listing")


# Edit A Listing Page
@app.route('/update/<int:id>/', methods=('GET', 'POST'))
def update(id):
    # Get film data
    listing_data = get_listing_by_id(id)

    # Check for errors
    error = None
    if not listing_data:
        error = 'Listing not found!'
        flash(category='warning', message=error)
    elif listing_data['user'] != session.get('user_id'):
        error = 'You do not have permission to edit this listing.'
        flash(category='danger', message=error)
        return redirect(url_for('listings'))
    if error:
        redirect(url_for('listings'))

    # If the request method is POST, process the form submission
    if request.method == 'POST':

        # Get the title input from the form
        listing_type = request.form['listing_type']
        postcode = request.form['postcode']
        listing_details = request.form['listing_details']
        poster = listing['poster']  # Default to existing poster
        if 'poster' in request.files:
            poster_file = request.files['poster']
            # Check it is an image file and save it
            if poster_file and poster_file.filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS:
                # Save the file to the static/uploads directory
                poster_url = f"/static/uploads/{poster_file.filename}"
                poster_file.save(f".{poster_url}")
                poster = poster_url  # Use the uploaded file URL in database

        duration = request.form['duration']
        town = request.form['town']
        price = request.form['price']

        # Validate the input
        if not listing_type:
            flash(category='danger', message='Listing Type is required!')
            return render_template('update.html', id=id)

        # Use database function to update listings

        update_listing(id, listing_type, postcode,
                       listing_details, poster, duration, town, price)
        # ===========================

        # Flash a success message
        flash(category='success', message='Updated successfully!')
        return redirect(url_for('listing', id=id))

    return render_template('update.html', title="Update listing", listing=listing_data)

# Delete A Film


@app.route('/delete/<int:id>', methods=('POST',))
def delete(id):

    # Get the film
    listing = get_listing_by_id(id)
    # Check for errors
    error = None
    if listing is None:     # If listing not found, add error message
        error = 'Listing not found!'
        flash(category='warning', message=error)
    # Check user is only accessing their own films
    elif listing['user'] != session.get('user_id'):
        error = 'You do not have permission to delete this film.'
        flash(category='danger', message=error)

    # If there was an error, redirect to films list
    if error:
        return redirect(url_for('listings'))

    # Use the database function to delete the film

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
