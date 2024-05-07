from flask import Blueprint, request, render_template, session, redirect, abort, flash, jsonify
import google.auth.transport.requests
from pip._vendor import cachecontrol
from google.oauth2 import id_token
import requests
import json
import re
from datetime import datetime
from astropy.time import Time
from astropy.coordinates import get_sun, EarthLocation, SkyCoord
from astropy import units as u
import requests
from shapely.geometry import Point, shape, Polygon
from shapely.ops import nearest_points


from src.google_auth import GOOGLE_CLIENT_ID, flow

bp = Blueprint("routes", __name__)

def get_closest_sea_helper(longitude, latitude):
    return {"sea": "asd", "distance": 0}


@bp.route("/get-closest-sea", methods=["POST"])
def get_closest_sea():
    parameters = request.get_json()
    longitude, latitude = parameters["longitude"], parameters["latitude"]

    sea = get_closest_sea_helper(longitude, latitude)

    return jsonify(sea)

def calculate_distance_to_sun_helper(longitude, latitude, time):
    earth_location = EarthLocation.from_geodetic(longitude, latitude)

    sun_coord = get_sun(time)

    earth_location_icrs = earth_location.get_itrs(obstime=time).transform_to(sun_coord.frame)

    # Calculate distance
    distance = sun_coord.separation_3d(earth_location_icrs)

    return distance.to(u.km).value


@bp.route("/calculate-distance-to-sun", methods=["POST"])
def calculate_distance_to_sun():
    parameters = request.get_json()
    longitude, latitude = parameters["longitude"], parameters["latitude"]

    distance = calculate_distance_to_sun_helper(longitude, latitude, Time.now())

    return jsonify({"distance": distance})

# Login Page
@bp.route("/distance-to-sun", methods=["GET"])
def distance_to_sun():
    return render_template("distance-to-sun.html")

# Login Page
@bp.route("/")
def index():
    return redirect("/login")

@bp.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    elif request.method == "POST":    
        # Check inputs
        email_phone, password = request.form["email_phone"], request.form["password"] 

        # Email/Phone or password cannot be blank
        if email_phone.strip() == "" or password.strip() == "":    
            flash("Email Address/Phone Number or Password cannot be blank", "alert alert-warning")
            return redirect("/login")
        
        # Check if the input is a valid email or a phone number
        def _is_valid_phone(phone_number: str) -> bool:
            phone_number = re.sub("\D", "", phone_number)
            if  phone_number.startswith("905") and len(phone_number) == 12 or \
                phone_number.startswith("05") and len(phone_number) == 11 or \
                phone_number.startswith("5") and len(phone_number) == 10:
                    return True
            return False
        def _is_valid_email(email: str) -> bool:
            return re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email) 

        if _is_valid_phone(email_phone):
            # Valid phone number
            pass        
        elif _is_valid_email(email_phone):
            # Valid email address
            pass
        else:
            flash("Please enter a valid Email Address or a Phone Number", "alert alert-warning")
            return redirect("/login")
            
        # Check if the credentials are valid 
        with open("users.json") as users_file:
            # Read users 
            users = json.load(users_file)

        valid_users = list(filter(lambda user: user["email_phone"] == email_phone and user["password"] == password, users))
        if valid_users:
            session["id"] = email_phone
            session["logged_in"] = True
            return redirect("/mail")
        else:
            flash("Incorrect Email Address/Phone Number or Password", "alert alert-danger")
            return redirect("/login")
        


# Google authentication handlers
@bp.route("/google_auth", methods=["POST"])
def google_auth():
    authorization_url, state = flow.authorization_url()
    session["state"] = state

    return redirect(authorization_url)

@bp.route("/callback")
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

    session["id"] = id_info.get("sub")
    session["logged_in"] = True

    return redirect("/mail")


# Logout
@bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect("/login") 


# Protected page
@bp.route("/mail", methods=["GET"])
def mail():
    if "logged_in" not in session or session["logged_in"] != True:
        return abort(401) 
    else:
        return render_template("mail.html")

