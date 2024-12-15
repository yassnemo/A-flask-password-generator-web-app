import random
import string
from flask import Flask, render_template, request

app = Flask(__name__)

# function to generate password
def generate_password(length, use_uppercase, use_digits, use_special_chars, special_chars):
    characters = string.ascii_lowercase  
    
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_digits:
        characters += string.digits
    if use_special_chars:
        characters += string.punctuation
    
    return ''.join(random.choice(characters) for _ in range(length))


@app.route("/", methods=["GET", "POST"])
def index():
    password = []
    
    if request.method == "POST":
        #get this from data
        length = int(request.form["length"])
        num_passwords = int(request.form["num_passwords"])
        use_uppercase = "uppercase" in request.form
        use_digits = "digits" in request.form
        use_special_chars = "special_chars" in request.form
        special_chars = request.form["special_chars_set"] if use_special_chars else string.punctuation
        
        # generate multi passwords
        for _ in range(num_passwords):
            password = generate_password(length, use_uppercase, use_digits, use_special_chars, special_chars)
            passwords.append(password)
    
    return render_template("index.html", passwords=passwords)

if __name__ == "__main__":
    app.run(debug=True)
