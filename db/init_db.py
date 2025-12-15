import sqlite3
from werkzeug.security import generate_password_hash
from test_listing import listings_data  # Import the test data
# This script should be run once to set up the database schema and initial data

# Database will be created in the same listing_detailsy as this script and named 'database.db'
connection = sqlite3.connect('database.db')

# This opens the schema.sql file and executes its contents to create the necessary tables
with open('schema.sql') as f:
    connection.executescript(f.read())

# Create a cursor object to execute SQL commands
cur = connection.cursor()

# Insert initial data into the user table
cur.execute("INSERT INTO users (username, password) VALUES (?, ?)",
            ('admin', generate_password_hash('password'))
            )

cur.execute("INSERT INTO users (username, password) VALUES (?, ?)",
            ('user1', generate_password_hash('password'))
            )

# Create listings based on listings_data in test_data.py
for listing in listings_data:
    cur.execute("INSERT INTO listings (user, listing_type, postcode, listing_details, poster, duration, town, price) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (2, listing['listing_type'], listing['postcode'], listing['listing_details'], listing['poster'], listing['duration'], listing['town'], listing['price'])
                )

# Commit the changes to the database and close the connection
connection.commit()
connection.close()
