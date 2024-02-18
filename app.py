from flask import Flask, request, render_template, session, redirect, abort
from google_auth_oauthlib.flow import Flow
import google.auth.transport.requests
from pip._vendor import cachecontrol
from google.oauth2 import id_token
import requests
import pathlib
import json
import os


# OAUTHLIB_INSECURE_TRANSPORT must be enabled for Google authentication to work with HTTP
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# Read google client ID and configure oauth flow 
with open("client_secret.json") as client_secret_file:
    client_secret = json.load(client_secret_file)
GOOGLE_CLIENT_ID = client_secret["web"]["client_id"]

flow = Flow.from_client_secrets_file(
    client_secrets_file=pathlib.Path("client_secret.json"),
    scopes= ["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
) 


# Create flask app
app = Flask(__name__)
app.secret_key = "CS 458 Project #1"


# A decorator to prevent unauthorized access  
def login_required(function):
    def wrapper(*args, **kwargs):
        if "logged_in" not in session or session["logged_in"] != True:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper


# Login Page
@app.route("/")
def index():
    return redirect("/login")
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    elif request.method == "POST":    
        # Check inputs
        return "TODO"

# Google authentication handlers
@app.route("/google_auth", methods=["POST"])
def google_auth():
    authorization_url, state = flow.authorization_url()
    session["state"] = state

    return redirect(authorization_url)
@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["logged_in"] = True

    return redirect("/mail")

# Protected page
@app.route("/mail", methods=["GET"])
@login_required
def mail():
    return render_template("mail.html")

# Logout
@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect("/login") 

if __name__ == "__main__":
    app.run(debug=True)