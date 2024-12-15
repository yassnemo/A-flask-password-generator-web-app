import random
import string
import os  # Import os for generating a secure key
from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generates a secure random key

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

    if request.method == "POST":
        try:
            # Retrieve form data with default values
            length = int(request.form.get("length", 12))
            num_passwords = int(request.form.get("num_passwords", 5))
            use_uppercase = "uppercase" in request.form
            use_digits = "digits" in request.form
            use_special_chars = "special_chars" in request.form
            special_chars = request.form.get("special_chars_set", string.punctuation) if use_special_chars else string.punctuation

            # Input validation
            if length < 4:
                raise ValueError("Password length must be at least 4.")
            if num_passwords < 1 or num_passwords > 30:
                raise ValueError("You must generate between 1 and 30 passwords.")

            # Generate multiple passwords
            for _ in range(num_passwords):
                password = generate_password(length, use_uppercase, use_digits, use_special_chars, special_chars)
                passwords.append(password)

        except ValueError as ve:
            # Flash error message and redirect
            flash(str(ve))
            return redirect(url_for('index'))
        except Exception as e:
            # Flash unexpected error message and redirect
            flash("An unexpected error occurred.")
            return redirect(url_for('index'))

    return render_template("index.html", passwords=passwords)

if __name__ == "__main__":
    app.run(debug=True)
