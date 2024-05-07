from google_auth_oauthlib.flow import Flow
import pathlib
import json

# Read google client ID 
with open("client_secret.json") as client_secret_file:
    client_secret = json.load(client_secret_file)
    GOOGLE_CLIENT_ID = client_secret["web"]["client_id"]

# Configure oauth flow 
flow = Flow.from_client_secrets_file(
    client_secrets_file=pathlib.Path("client_secret.json"),
    scopes= ["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="https://127.0.0.1:5000/callback"
) 