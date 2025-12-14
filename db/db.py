# Import the test data
from db.test_listing import listings_data
# import sqlite3
# import os
# from flask import abort
# from werkzeug.security import check_password_hash, generate_password_hash

# # This defines which functions are available for import when using 'from db.db import *'
# __all__ = [
#     "get_all_films",
#     "get_film_by_id",
#     "create_film",
#     "update_film",
#     "delete_film",
#     "create_user",
#     "validate_login",
#     "get_user_by_username",
#     "get_user_by_id",
# ]

# # Establish connection to the SQLite database


# def get_db_connection():
#     # Get the directory of the current file
#     BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#     # Construct the full path to the database file
#     DB_PATH = os.path.join(BASE_DIR, 'database.db')
#     conn = sqlite3.connect(DB_PATH)                 # Connect to the database
#     # Enable dictionary-like access to rows
#     conn.row_factory = sqlite3.Row
#     return conn

# # Authentication functions
# # =========================================================
# # Insert a new user (Register)


# def create_user(username, password):
#     hashed_password = generate_password_hash(password)
#     conn = get_db_connection()
#     conn.execute('INSERT INTO users (username, password) VALUES (?, ?)',
#                  (username, hashed_password))
#     conn.commit()
#     conn.close()

# # Validate user exists with password (Login)


# def validate_login(username, password):
#     user = get_user_by_username(username)
#     if user and check_password_hash(user['password'], password):
#         return user
#     return None

# # Check if a user exists


# def get_user_by_username(username):
#     conn = get_db_connection()
#     user = conn.execute(
#         'SELECT * FROM users WHERE username = ?', (username,)).fetchone()
#     conn.close()
#     return user

# # Get user by ID


# def get_user_by_id(user_id):
#     conn = get_db_connection()
#     user = conn.execute('SELECT * FROM users WHERE id = ?',
#                         (user_id,)).fetchone()
#     conn.close()
#     if user is None:
#         abort(404)
#     return user


# # Film Display functions
# # =========================================================
# # Get all films (or filter by user)
# def get_all_films(user=None, limit=None, order_by='title ASC'):
#     conn = get_db_connection()
#     # Construct base query
#     query = 'SELECT * FROM films'
#     # If user is specified, filter films by that user
#     if user:
#         query += ' WHERE user = ?'
#     # Add ORDER BY to the query if specified
#     query += f' ORDER BY {order_by}'
#     # Add LIMIT if specified
#     if limit:
#         query += f' LIMIT {limit}'

#     # Execute the query
#     if user:
#         films = conn.execute(query, (user,)).fetchall()
#     else:
#         films = conn.execute(query).fetchall()

#     conn.close()

#     return films

# # Get a film by its ID


# def get_film_by_id(film_id):
#     conn = get_db_connection()
#     film = conn.execute('SELECT * FROM films WHERE id = ?',
#                         (film_id,)).fetchone()
#     conn.close()
#     return film


# # Create a new film


# def create_film(film_data):
#     # Generate a new ID based on the current max
#     new_id = max(f['id'] for f in films_data) + 1 if films_data else 1
#     film_data['id'] = new_id
#     films_data.append(film_data)
#     return film_data

# # Update an existing film


# def update_film(film_id, updated_data):
#     film = get_film_by_id(film_id)
#     if film:
#         film.update(updated_data)
#         return film
#     return None

# # Delete a film by its ID


# def delete_film(film_id):
#     films_data.pop(film_id-1)
#     return

# Get all films
def get_all_listings():
    return listings_data

# Get a film by its ID


def get_listing_by_id(listing_id):
    return next((listing for listing in listings_data if listing['id'] == listing_id), None)

# Create a new film


def create_listing(listing_data):
    # Generate a new ID based on the current max
    new_id = max(f['id'] for f in listings_data) + 1 if listings_data else 1
    listing_data['id'] = new_id
    listings_data.append(listing_data)
    return listing_data

# Update an existing film


def update_listing(listing_id, updated_data):
    listing = get_listing_by_id(listing_id)
    if listing:
        listing.update(updated_data)
        return listing
    return None

# Delete a film by its ID


def delete_listing(listing_id):
    listings_data.pop(listing_id-1)
    return
