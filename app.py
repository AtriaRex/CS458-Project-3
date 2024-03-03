from flask import Flask
import os

from src.routes import bp

# OAUTHLIB_INSECURE_TRANSPORT must be enabled for Google authentication to work with HTTP
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


# Create flask app
app = Flask(__name__)
app.secret_key = "CS 458 Project #1"
app.register_blueprint(bp)

if __name__ == "__main__":
    app.run(debug=True)
