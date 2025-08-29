# Import necessary parts from Flask and a database library (psycopg2)
from flask import Flask, render_template, request, redirect, url_for
import os
import psycopg2 # This library helps Python talk to PostgreSQL database

app = Flask(__name__)

# --- Database Connection Setup ---
# Explanation: These lines get database connection details from environment variables.
# Environment variables are like secret notes passed to our application from Docker Compose.
DB_HOST = os.environ.get('DB_HOST', 'localhost') # Default to 'localhost' if not set
DB_NAME = os.environ.get('DB_NAME', 'mydatabase')
DB_USER = os.environ.get('DB_USER', 'myuser')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'mypassword')

def get_db_connection():
    # Explanation: This function connects to our PostgreSQL database.
    # It uses the details from the environment variables.
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

# --- Database Initialization (Run once when app starts) ---
# Explanation: This code tries to create a simple table in our database
# if it doesn't already exist. This table will store our messages.
with app.app_context():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            content TEXT NOT NULL
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

# --- Web Application Routes ---
# Explanation: These define what happens when a user visits different URLs.

@app.route('/', methods=('GET', 'POST'))
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        # If the user submitted a new message
        message_content = request.form['content']
        if message_content:
            cur.execute('INSERT INTO messages (content) VALUES (%s)', (message_content,))
            conn.commit()
            return redirect(url_for('index')) # Redirect to refresh the page

    # Get all messages from the database to display them
    cur.execute('SELECT id, content FROM messages ORDER BY id DESC')
    messages = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', messages=messages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

