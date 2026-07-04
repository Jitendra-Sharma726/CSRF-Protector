from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)

# The secret key is used to cryptographically sign session cookies and flash messages.
# This prevents attackers from tampering with their browser cookies to hijack accounts.
# Note: In a real production app, NEVER hardcode this! Use a secure environment variable.
app.secret_key = 'supersecret_dev_key'

DB_FILE = 'users.db'

# Database Functions:
def execute_query(query, args=(), fetchone=False):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(query, args)
    if fetchone:
        result = cursor.fetchone()
    else:
        conn.commit()
        result = None
    conn.close()
    return result

# Routes:
@app.route('/update-email', methods=['GET', 'POST'])
def update_email():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user = session['user']
    
    if request.method == 'POST':
        # VULNERABILITY: No CSRF token verification.
        # TODO: Verify the CSRF token before updating the database.

        new_email = request.form.get('email', '').strip()
        if new_email:
            execute_query("UPDATE users SET email = ? WHERE username = ?", (new_email, user))
            flash('Email updated successfully!', 'success')
        return redirect(url_for('update_email'))
        
    current_email_record = execute_query("SELECT email FROM users WHERE username = ?", (user,), fetchone=True)
    current_email = current_email_record[0] if current_email_record else ""
    
    # TODO: Generate a CSRF token using 'secrets', save it to the session, and pass it to the template.
    
    return render_template('update_email.html', user=user, current_email=current_email)

@app.route('/attacker-demo')
def attacker_demo():
    """Simulates the malicious website used in Phase 1 of the attack."""
    return render_template('attacker.html')

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('update_email'))
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()
        email = request.form.get('email').strip()
        
        try:
            execute_query("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, password, email))
            session['user'] = username
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return "Username already exists!", 400
            
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()
        
        user_record = execute_query("SELECT password FROM users WHERE username = ?", (username,), fetchone=True)
        
        if user_record and user_record[0] == password:
            session['user'] = username
            return redirect(url_for('update_email'))
        else:
            error = "Invalid username or password"
            
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
    

    
