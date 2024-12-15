import random
import string
import os  # Import os for generating a secure key
from flask import Flask, render_template, request, flash, redirect, url_for, make_response

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generates a secure random key

# Function to generate a single password
def generate_password(length, use_lowercase, use_uppercase, use_digits, use_special_chars, special_chars):
    characters = ""
    
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_digits:
        characters += string.digits
    if use_special_chars:
        characters += special_chars

    # If no characters selected, default to lowercase letters
    if not characters:
        characters = string.ascii_lowercase
    
    return ''.join(random.choice(characters) for _ in range(length))

@app.route("/", methods=["GET", "POST"])
def index():
    passwords = []  # Initialize passwords as an empty list
    settings = {
        'length': 12,
        'num_passwords': 5,
        'lowercase': True,
        'uppercase': False,
        'digits': False,
        'special_chars': False,
        'special_chars_set': string.punctuation
    }

    # Load settings from cookies if available
    try:
        if 'settings' in request.cookies:
            settings = eval(request.cookies.get('settings'))  # Be cautious with eval - use this only if you trust the source
    except Exception as e:
        flash(f"Error loading settings: {e}")

    if request.method == "POST":
        try:
            # Retrieve form data with default values
            length = int(request.form.get("length", settings['length']))
            num_passwords = int(request.form.get("num_passwords", settings['num_passwords']))
            use_lowercase = "lowercase" in request.form
            use_uppercase = "uppercase" in request.form
            use_digits = "digits" in request.form
            use_special_chars = "special_chars" in request.form
            special_chars = string.punctuation if use_special_chars else settings['special_chars_set']

            # Input validation
            if length < 4:
                raise ValueError("Password length must be at least 4.")
            if num_passwords < 1:
                raise ValueError("You must generate at least one password.")

            # Generate multiple passwords
            for _ in range(num_passwords):
                password = generate_password(length, use_lowercase, use_uppercase, use_digits, use_special_chars, special_chars)
                passwords.append(password)

            # Save settings to cookies
            settings = {
                'length': length,
                'num_passwords': num_passwords,
                'lowercase': use_lowercase,
                'uppercase': use_uppercase,
                'digits': use_digits,
                'special_chars': use_special_chars,
                'special_chars_set': special_chars
            }

            resp = make_response(render_template("index.html", passwords=passwords, settings=settings))
            resp.set_cookie('settings', str(settings), max_age=60*60*24*365)  # Cookie expires in 1 year
            return resp

        except ValueError as ve:
            # Flash error message and redirect
            flash(str(ve))
            return redirect(url_for('index'))
        except Exception as e:
            # Flash unexpected error message and redirect
            flash("An unexpected error occurred.")
            return redirect(url_for('index'))

    return render_template("index.html", passwords=passwords, settings=settings)

if __name__ == "__main__":
    app.run(debug=True)
