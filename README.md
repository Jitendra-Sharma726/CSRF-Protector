# CSRF-Protector

You are auditing the profile settings portal of a Python web application. The provided server (app.py) currently processes POST requests to the /update-email route without verifying where the request actually came from.

This contains a critical flaw known as Cross-Site Request Forgery (CSRF). When a user logs in, their browser stores a session cookie. Browsers automatically attach this cookie to any request sent to the application's domain, regardless of who initiated it. An attacker can trick an authenticated user into visiting a malicious third-party website that contains a hidden form. This hidden form silently submits an email update request to your server. Because the browser attaches the user's session cookie, the server assumes it's a legitimate request and changes the user's email to the attacker's email, locking the user out of their account!

Project Structure:
You are given a few key files:

setup_users.py: A script to initialize the local SQLite database (users.db).
app.py: The Flask backend server containing the vulnerable /update-email route.
templates/update_email.html: The frontend UI where the user updates their email.
templates/attacker.html: A simulated malicious website that auto-submits a hidden form.
Your Task
Prove the vulnerability exists by simulating a CSRF attack to hijack a user's account. Then, act as the defender and patch app.py by implementing a Synchronizer Token Pattern. You will generate a unique, cryptographically secure CSRF token, embed it in the legitimate form, and verify it on the server, neutralizing the attack.

Phase 1: The Attack

Open your terminal and initialize the database by running: python setup_users.py
Start the web server by running: python app.py
Open the application in your workspace browser preview (it runs on port 3000).
Sign up for a new account (e.g., Username: alice, Email: alice@work.com). You will be redirected to your profile settings.
Now, imagine Alice receives a spam email promising a free gift card and clicks the link. Simulate this by edit the codechef browser url from codechef.com/update-email to codechef.com/attacker-demo
https://lunar-bat.codechef-apps.com/attacker-demo
The "Free Gift Card" page will load and instantly auto-submit a hidden form. Because the form submits to the server's update route, your tab will automatically be redirected back to your logged-in Profile Settings page.
Look closely at the screen: your email has been maliciously changed to hacker@evil.com without your consent! You have successfully exploited the application.
(For more info and a visual walkthrough of this attack, please refer to the project demonstration video.)
Docs: OWASP Cross-Site Request Forgery (CSRF)
Phase 2: The Defense

Stop your Flask server in the terminal (press Ctrl+C).
Open app.py in your code editor.
At the top of the file, import the secrets library to give Python access to cryptographic token generation.
The Setup Patch: Scroll down to the bottom of the update_email() route (before the render_template return). Generate a secure token using secrets.token_hex(16). Save this token into the user's session['csrf_token'], and pass it to the template as a variable.
The UI Patch: Open the templates/update_email.html file. Inside the <form>, add the following line of code to create a hidden input field. This ensures the secure token is secretly submitted along with the user's new email:
<input type="hidden" name="csrf_token" value="{{ csrf_token }}">
The Verification Patch: Go back to app.py. Inside the if request.method == 'POST': block, retrieve the token from the form submission. Write an if statement to check if the form's token matches the session's token. If it is missing or does not match, block the request using abort(400).
Run python app.py one more time. Log in, and try visiting /attacker-demo endpoint again.
Docs: Python Secrets Module | CSRF Prevention Cheat Sheet
Expected Behaviour:

Phase 1: Before Patching (The Successful Attack)
When you visit the attacker demo page, the malicious script executes flawlessly in the background. Your legitimate session cookie is used against you, you are redirected back to the portal, and your profile updates to the hacker's email address.
Phase 2: After Patching (The Successful Defense)
When you visit the attacker demo page, the attacker tries to submit the form, but they cannot guess your secret, randomly generated CSRF token. The server rejects the malicious request entirely, keeping your account safe.

Did you like the problem?
1 user found this helpful
