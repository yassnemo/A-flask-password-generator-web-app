from flask import Flask, render_template, request, flash, redirect, url_for, make_response
import random
import string
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Function to generate a single password
def generate_password(length, use_uppercase, use_digits, use_special_chars, special_chars):
    characters = string.ascii_lowercase  # Always include lowercase characters
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_digits:
        characters += string.digits
    if use_special_chars:
        characters += special_chars
    return ''.join(random.choice(characters) for _ in range(length))

@app.route("/", methods=["GET", "POST"])
def index():
    passwords = []  # Initialize passwords as an empty list

    # Default settings
    default_settings = {
        "length": 12,
        "num_passwords": 5,
        "uppercase": False,
        "digits": False,
        "special_chars": False,
        "special_chars_set": string.punctuation
    }

    # Retrieve settings from cookies (if available)
    if request.cookies.get("password_settings"):
        stored_settings = request.cookies.get("password_settings")
        stored_settings = stored_settings.split('|')  # Split settings based on separator

        # Convert string values to appropriate types
        default_settings = {
            "length": int(stored_settings[0]),
            "num_passwords": int(stored_settings[1]),
            "uppercase": bool(int(stored_settings[2])),
            "digits": bool(int(stored_settings[3])),
            "special_chars": bool(int(stored_settings[4])),
            "special_chars_set": stored_settings[5] if stored_settings[5] != "None" else string.punctuation
        }

    if request.method == "POST":
        try:
            # Retrieve form data with default values
            length = int(request.form.get("length", default_settings["length"]))
            num_passwords = int(request.form.get("num_passwords", default_settings["num_passwords"]))
            use_uppercase = "uppercase" in request.form
            use_digits = "digits" in request.form
            use_special_chars = "special_chars" in request.form
            special_chars = request.form.get("special_chars_set", string.punctuation) if use_special_chars else string.punctuation

            # Input validation
            if length < 4:
                raise ValueError("Password length must be at least 4.")
            if num_passwords < 1:
                raise ValueError("You must generate at least one password.")

            # Generate multiple passwords
            for _ in range(num_passwords):
                password = generate_password(length, use_uppercase, use_digits, use_special_chars, special_chars)
                passwords.append(password)

            # Store settings in a cookie
            settings = "|".join([str(length), str(num_passwords), str(int(use_uppercase)), str(int(use_digits)), str(int(use_special_chars)), special_chars if special_chars != string.punctuation else "None"])
            resp = make_response(render_template("index.html", passwords=passwords))
            resp.set_cookie("password_settings", settings, max_age=30 * 24 * 60 * 60)  # Cookie expires after 30 days
            return resp

        except ValueError as ve:
            flash(str(ve))
            return redirect(url_for('index'))
        except Exception as e:
            flash("An unexpected error occurred.")
            return redirect(url_for('index'))

    return render_template("index.html", passwords=passwords, settings=default_settings)

if __name__ == "__main__":
    app.run(debug=True)