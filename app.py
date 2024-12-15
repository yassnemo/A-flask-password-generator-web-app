import random
import string
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.secret_key = os.urandom(24)

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
            length = int(request.form.get("length", 12))
            num_passwords = int(request.form.get("num_passwords", 5))
            use_uppercase = "uppercase" in request.form
            use_digits = "digits" in request.form
            use_special_chars = "special_chars" in request.form
            special_chars = request.form.get("special_chars_set", string.punctuation) if use_special_chars else string.punctuation

            if length < 4:
                raise ValueError("Password length must be at least 4.")
            if num_passwords < 1:
                raise ValueError("You must generate at least one password.")

            for _ in range(num_passwords):
                password = generate_password(length, use_uppercase, use_digits, use_special_chars, special_chars)
                passwords.append(password)

        except ValueError as ve:
            passwords = [{"error": str(ve)}]
        except Exception as e:
            passwords = [{"error": "An unexpected error occurred."}]

    return render_template("index.html", passwords=passwords)

# New route for AJAX
@app.route("/generate_passwords", methods=["POST"])
def generate_passwords():
    try:
        length = int(request.form.get("length", 12))
        num_passwords = int(request.form.get("num_passwords", 5))
        use_uppercase = "uppercase" in request.form
        use_digits = "digits" in request.form
        use_special_chars = "special_chars" in request.form
        special_chars = request.form.get("special_chars_set", string.punctuation) if use_special_chars else string.punctuation

        if length < 4:
            raise ValueError("Password length must be at least 4.")
        if num_passwords < 1:
            raise ValueError("You must generate at least one password.")

        passwords = []
        for _ in range(num_passwords):
            password = generate_password(length, use_uppercase, use_digits, use_special_chars, special_chars)
            passwords.append(password)

        return jsonify(passwords=passwords)  # Send passwords as JSON

    except ValueError as ve:
        return jsonify(error=str(ve))
    except Exception as e:
        return jsonify(error="An unexpected error occurred.")

if __name__ == "__main__":
    app.run(debug=True)
