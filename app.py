from flask import Flask, render_template, request, flash, redirect, url_for
import random
import string
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Function to generate a single password
def generate_password(length, use_uppercase, use_digits, use_special_chars, special_chars):
    # Ensure length is capped at 40
    length = min(length, 40)
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
            if length < 4 or length > 40:
                raise ValueError("Password length must be between 4 and 40.")
            if num_passwords < 1 or num_passwords > 30:
                raise ValueError("You must generate between 1 and 30 passwords.")

            # Generate passwords
            for _ in range(num_passwords):
                password = generate_password(length, use_uppercase, use_digits, use_special_chars, special_chars)
                passwords.append(password)

        except ValueError as e:
            flash(str(e), "error")

    return render_template("index.html", passwords=passwords)

if __name__ == "__main__":
    app.run(debug=True)
