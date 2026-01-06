# Import the test data
from db.test_listing import listings_data
import sqlite3
import os
from flask import abort
from werkzeug.security import check_password_hash, generate_password_hash

# This defines which functions are available for import when using 'from db.db import *'
__all__ = [
    "get_all_listings",
    "get_listing_by_id",
    "create_listing",
    "update_listing",
    "delete_listing",
    "create_user",
    "validate_login",
    "get_user_by_username",
    "get_user_by_id",
]

# Establish connection to the SQLite database


def get_db_connection():
    # Get the directory of the current file
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # Construct the full path to the database file
    DB_PATH = os.path.join(BASE_DIR, 'database.db')
    conn = sqlite3.connect(DB_PATH)                 # Connect to the database
    # Enable dictionary-like access to rows
    conn.row_factory = sqlite3.Row
    return conn

# Authentication functions
# =========================================================
# Insert a new user (Register)


def create_user(username, password):
    hashed_password = generate_password_hash(password)
    conn = get_db_connection()
    conn.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                 (username, hashed_password))
    conn.commit()
    conn.close()

# Validate user exists with password (Login)


def validate_login(username, password):
    user = get_user_by_username(username)
    if user and check_password_hash(user['password'], password):
        return user
    return None

# Check if a user exists


def get_user_by_username(username):
    conn = get_db_connection()
    user = conn.execute(
        'SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    return user

# Get user by ID


def get_user_by_id(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?',
                        (user_id,)).fetchone()
    conn.close()
    if user is None:
        abort(404)
    return user


# Listing Display functions
# =========================================================
# Get all listings (or filter by user)
def get_all_listings(user=None, limit=None, order_by='listing_type ASC'):
    conn = get_db_connection()
    # Construct base query
    query = 'SELECT * FROM listings'
    # If user is specified, filter listings by that user
    if user:
        query += ' WHERE user = ?'
    # Add ORDER BY to the query if specified
    query += f' ORDER BY {order_by}'
    # Add LIMIT if specified
    if limit:
        query += f' LIMIT {limit}'

    # Execute the query
    if user:
        listings = conn.execute(query, (user,)).fetchall()
    else:
        listings = conn.execute(query).fetchall()

    conn.close()

    return listings

# Get a listing by its ID


def get_listing_by_id(listing_id):
    conn = get_db_connection()
    listing = conn.execute('SELECT * FROM listings WHERE id = ?',
                           (listing_id,)).fetchone()
    conn.close()
    return listing

# Listings CRUD functions
# Create a new listing


def create_listing(user_id, listing_type, postcode, listing_details, poster, duration, town, price):
    conn = get_db_connection()
    conn.execute('INSERT INTO listings (user, listing_type, postcode, listing_details, poster, duration, town, price) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                 (user_id, listing_type, postcode, listing_details, poster, duration, town, price))
    conn.commit()
    conn.close()


# Update an existing listing


def update_listing(listing_id, listing_type, postcode, listing_details, poster, duration, town, price):
    conn = get_db_connection()
    conn.execute('UPDATE listings SET listing_type = ?, postcode = ?, listing_details = ?, poster = ?, duration = ?, town = ?, price = ? WHERE id = ?',
                 (listing_type, postcode, listing_details, poster, duration, town, price, listing_id))
    conn.commit()
    conn.close()


# Delete a listing by its ID


def delete_listing(listing_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM listings WHERE id = ?', (listing_id,))
    conn.commit()
    conn.close()


# Get all listings
# def get_all_listings():
#     return listings_data

# Get a listing by its ID


# def get_listing_by_id(listing_id):
#     return next((listing for listing in listings_data if listing['id'] == listing_id), None)

# # Create a new listing


# def create_listing(listing_data):
#     # Generate a new ID based on the current max
#     new_id = max(f['id'] for f in listings_data) + 1 if listings_data else 1
#     listing_data['id'] = new_id
#     listings_data.append(listing_data)
#     return listing_data

# # Update an existing listing


# def update_listing(listing_id, updated_data):
#     listing = get_listing_by_id(listing_id)
#     if listing:
#         listing.update(updated_data)
#         return listing
#     return None

# # Delete a listing by its ID


# def delete_listing(listing_id):
#     listings_data.pop(listing_id-1)
#     return
