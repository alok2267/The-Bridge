from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
import os

# Initialize the Flask app
app = Flask(__name__)
# Set a secret key for session management. In a real app, use a secure, random key.
app.secret_key = os.urandom(24)

# --- Dummy User Data ---
# In a real application, this data would be stored in a secure database.
DUMMY_USERS = {
    "admin@alumniconnect.com": {
        "password": "adminpassword",
        "type": "admin",
        "name": "Admin User",
        "grad_year": "N/A"
    },
    "alumni@alumniconnect.com": {
        "password": "alumnipassword",
        "type": "alumni",
        "name": "Jane Doe",
        "grad_year": "2020"
    }
}

# --- Decorator for Authentication ---
# This checks if a user is logged in before allowing access to a route.
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --- Routes ---

@app.route('/', methods=['GET', 'POST'])
def login():
    """Handles the login page and authentication logic."""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = DUMMY_USERS.get(email)

        # Check if the user exists and the password is correct
        if user and user['password'] == password:
            # Store user info in the session
            session['email'] = email
            session['user_type'] = user['type']
            session['name'] = user['name']
            
            flash(f"Welcome back, {user['name']}!", "success")
            return redirect(url_for('profile')) # Redirect to profile page after login
        else:
            flash("Invalid email or password. Please try again.", "danger")
            return redirect(url_for('login'))

    # If already logged in, redirect to home
    if 'email' in session:
        return redirect(url_for('home'))
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logs the user out by clearing the session."""
    session.clear()
    flash("You have been successfully logged out.", "info")
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
    """Displays the main home page."""
    return render_template('home.html')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Displays and handles updates to the user profile."""
    if request.method == 'POST':
        # In a real app, you would update the database here.
        name = request.form.get('fullName')
        grad_year = request.form.get('gradYear')
        
        # Update session data as a demonstration
        session['name'] = name
        DUMMY_USERS[session['email']]['name'] = name
        DUMMY_USERS[session['email']]['grad_year'] = grad_year
        
        flash("Your profile has been updated successfully!", "success")
        return redirect(url_for('profile'))

    user_data = DUMMY_USERS.get(session['email'])
    return render_template('profile.html', user=user_data)

@app.route('/directory')
@login_required
def directory():
    """Displays the alumni directory."""
    # Exclude admin users from the public directory list
    alumni_list = [user for user in DUMMY_USERS.values() if user['type'] == 'alumni']
    return render_template('directory.html', alumni=alumni_list)

@app.route('/events')
@login_required
def events():
    """Displays the events page."""
    return render_template('events.html')

# To run the app:
if __name__ == '__main__':
    # Use debug=True for development to get auto-reloads and error pages.
    # In production, this should be False.
    app.run(debug=True)
