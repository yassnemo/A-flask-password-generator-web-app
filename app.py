import random
import string
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.secret_key = os.urandom(24)

def generate_password(length, use_uppercase, use_digits, use_special_chars):
    """
    Generates a random password based on the specified parameters.
    
    Parameters:
    - length (int): Length of the password.
    - use_uppercase (bool): Whether to include uppercase letters.
    - use_digits (bool): Whether to include digits.
    - use_special_chars (bool): Whether to include special characters.
    
    Returns:
    - str: The generated password.
    """
    characters = string.ascii_lowercase  # Always include lowercase characters
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_digits:
        characters += string.digits
    if use_special_chars:
        characters += string.punctuation

    if not characters:
        raise ValueError("No character types selected. Please select at least one option.")

    # Generate the password ensuring randomness
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

@app.route("/", methods=["GET", "POST"])
def index():
    passwords = []  # Initialize passwords as an empty list

    if request.method == "POST":
        try:
            # Retrieve form data
            length = int(request.form.get("length", 12))
            num_passwords = int(request.form.get("num_passwords", 5))
            use_uppercase = "uppercase" in request.form
            use_digits = "digits" in request.form
            use_special_chars = "special_chars" in request.form

            # Validate input
            if length < 4:
                raise ValueError("Password length must be at least 4.")
            if num_passwords < 1:
                raise ValueError("You must generate at least one password.")
            if not (use_uppercase or use_digits or use_special_chars):
                raise ValueError("At least one character type must be selected.")

            # Generate passwords
            for _ in range(num_passwords):
                password = generate_password(length, use_uppercase, use_digits, use_special_chars)
                passwords.append(password)

        except ValueError as ve:
            passwords = [{"error": str(ve)}]
        except Exception as e:
            passwords = [{"error": "An unexpected error occurred."}]

    return render_template("index.html", passwords=passwords)

# Route for AJAX password generation
@app.route("/generate_passwords", methods=["POST"])
def generate_passwords_route():
    try:
        # Retrieve form data sent via AJAX
        length = int(request.form.get("length", 12))
        num_passwords = int(request.form.get("num_passwords", 5))
        use_uppercase = request.form.get("uppercase") in ['true', 'on']
        use_digits = request.form.get("digits") in ['true', 'on']
        use_special_chars = request.form.get("special_chars") in ['true', 'on']

        # Validate input
        if length < 4:
            raise ValueError("Password length must be at least 4.")
        if num_passwords < 1:
            raise ValueError("You must generate at least one password.")
        if not (use_uppercase or use_digits or use_special_chars):
            raise ValueError("At least one character type must be selected.")

        # Generate passwords
        passwords = []
        for _ in range(num_passwords):
            password = generate_password(length, use_uppercase, use_digits, use_special_chars)
            passwords.append(password)

        return jsonify(passwords=passwords)  # Return passwords as JSON

    except ValueError as ve:
        return jsonify(error=str(ve)), 400  # Return error message with 400 status code
    except Exception as e:
        return jsonify(error="An unexpected error occurred."), 500  # Return generic error message with 500 status code

if __name__ == "__main__":
    app.run(debug=True)
