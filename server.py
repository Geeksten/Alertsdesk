"""Alerts."""

import json
# import jinja debugging tool
from jinja2 import StrictUndefined
# import flask tools
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
# import geopy tools for lat/long derivation from address data
from geopy.geocoders import GoogleV3
# import database & classes from model.py
from model import connect_to_db, db, User, Userreport, Reportsymptom
from model import Symptom, State, Staterecall, Fdarecall
import requests
import pprint
from datetime import datetime
#import os so we can use the secrets file
import os
#Twilio
# from twilio.rest import TwilioRestClient
# import twilio.twiml

# make it a Flask app
app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = os.environ['app_key']
openweather_api = os.environ['openweather_api']

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


################################################################

# @app.route('/')
# def index():
#     """Homepage."""

#     return render_template("index.html")

############################################################################

@app.route('/')
def display_default_map():
    """Show default map."""
    print "There should be a map here"
    print "There should be a map here"
    print "There should be a map here"
    print "There should be a map here"

    return render_template("map_geodefault.html")
############################################################################


@app.route('/register', methods=['GET'])
def register_form():
    """New user sign in form."""

    return render_template("register_form.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration.
        Uses a redirect so user does not have to leave page after registration.
        Also uses flash messages to inform user that they have successfully registered
        and displays the username which is the email that was registered."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]
    firstname = request.form["firstname"]
    lastname = request.form["lastname"]

    user = User.query.filter_by(email=email).first()

    if user:
        flash("You're already a user. Please log in.")
        return redirect("/login")

    else:

        new_user = User(email=email, password=password, firstname=firstname, lastname=lastname)

    db.session.add(new_user)
    db.session.commit()

    flash("Thank you %s, you have been added as a user. Go ahead and log in" % email)
    return redirect('/login')

########################################################################


@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("Sorry that email was not found on our system. Please check the email address or register as a new user")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("You logged in successfully")
    return redirect("/profile/%s" % user.user_id)

#########################################################################


@app.route('/profile/<int:user_id>')
def user_profile(user_id):
    """Show logged in users profile"""

    # user = User.query.get(user_id)

    user_id = session.get("user_id")

    if not user_id:
        return redirect('/login')

    else:
        user = User.query.get(user_id)
        return render_template("profile.html", user=user)

########################################################################


@app.route('/addnewreport', methods=['GET'])
def report_form():
    """Show add new report form."""

    # print session["user_id"]

    user_id = session.get("user_id")

    if not user_id:
        flash("Sorry log in required before adding a report.")
        return redirect('/login')

    else:
        return render_template("add_new_report_form.html")

#########################################################################


@app.route('/userreport', methods=['POST'])
def report_process():
    """Process new report."""

    # Get form variables
    # zipcode = request.form["zipcode"]
    address = request.form["address"]
    report = request.form["report"]
    user_id = session["user_id"]
    date_now = datetime.now()
    # print str(i)
    date_added = date_now.strftime('%Y/%m/%d %H:%M:%S')
    # print time_now
    # latitude = request.form["latitude"]
    # longitude = request.form["longitude"]
    #convert address to lat long
    # geolocator = GoogleV3()
    # address, (latitude, longitude) = geolocator.geocode(address)
    # print address
    # latitude, longitude = (latitude, longitude)

    ##geocode the address

    payload = {'address': address}

    r = requests.get("https://maps.googleapis.com/maps/api/geocode/json", params=payload)

    jdict = r.json()

    stuff_list = jdict["results"]
    for i_dict in stuff_list:
        return i_dict

    add_components_list = i_dict["address_components"]

    city_dict = add_components_list[3]
    city = city_dict["long_name"]

    state_dict = add_components[5]
    state = state_dict["long_name"]
    state_code = state_dict["short_name"]

    zipcode_dict = add_components[7]
    zipcode = zipcode_dict["long_name"]

    latlng_dict = i_dict["geometry"]
    location_dict = latlon["location"]
    latitide = location["lat"]
    longitude = location["lng"]

    new_userreport = Userreport(address=address, zipcode=zipcode,
                                report=report, date_added=date_added,
                                user_id=user_id, latitude=latitude, longitude=longitude)

    db.session.add(new_userreport)
    db.session.commit()

#     flash("Thank you %s, your report was added. Click the Search link to search for reports" % firstname)

    user_id = session.get("user_id")

    # user = User.query.filter_by(email=email).first()
    user = User.query.get(user_id)
    print "*********************** user is %s" % user
    userreport_list = Userreport.query.filter_by(user_id=user_id).all()

    print "*********************** userreport is %s" % userreport_list

    return render_template("userreport.html", userreport_list=userreport_list, user=user)

#########################################################################


@app.route('/alerts', methods=['GET'])
def alerts_signup_form():
    """Show alerts sign up form."""

    user_id = session.get("user_id")

    if not user_id:
        flash("Sorry log in required before signing up for alerts.")
        return redirect('/login')

    else:
        return render_template("alerts_signup.html")

#########################################################################

#TO DO COMPLETE ROUTE


# @app.route('/alerts', methods=['POST'])
# def alerts_process():
#     """Process alerts sign up."""

#     # Get form variables
#     email = request.form["email"]
#     password = request.form["password"]

#     user = User.query.filter_by(email=email).first()

#     if not user:
#         flash("Sorry that email was not found on our system. Please check the email address or register as a new user")
#         return redirect("/login")

#     if user.password != password:
#         flash("Incorrect password")
#         return redirect("/login")

#     session["user_id"] = user.user_id

#     flash("You logged in successfully")
#     return redirect("/profile/%s" % user.user_id)

#########################################################################


@app.route("/symptom/<int:sym_id>")
def show_symptoms(sym_id):
    """Return page showing more information about a given symtom.
    """
    # user = User.query.filter_by(email=email).first()
    symptom = Symptom.query.get(sym_id)
    print symptom
    return render_template("symptom_details.html",
                           symptom=symptom)

#########################################################################
#TO DO COMPLETE THE ROUTE
#enter queries


@app.route('/illnessform', methods=['GET'])
def show_illness_form():
    '''Displays a form so user can search for illnesses by zip'''

    return render_template("illness_form.html")


@app.route('/illnessmap', methods=['POST'])
def process_illness_result():
    """Display list of illnesses for given zipcode."""

    # Get form variables
    newzip = request.form.get("zipcode")
    # print ("userzip is %s") % userzip

    print "user entered this zipcode %s" % newzip

    all_reports = db.session.query(Userreport.report, Userreport.date_added)
    newzip_illness_list = all_reports.filter(Userreport.zipcode == newzip).all()
    print newzip_illness_list

    # for r in newzip_illness_list:
    #     print r.report
    #    ...:
    # fever, sweats
    # chills...
#########################################################################

# def process_weather_result():
#     """Display weather conditions for given zipcode."""

    # openweather_api = os.environ['openweather_api']
    api_key = 'appid=' + openweather_api
    # Get form variables
    print newzip
    shortened_url = 'http://api.openweathermap.org/data/2.5/weather'
    payloadwet = "&" + 'zip=' + newzip + ',us' + "&units=imperial"
    print payloadwet

    r = requests.get(shortened_url, params=api_key + payloadwet)
    # print r   # gives resposnse 200 everythings ok

    jdict = r.json()
    # print jdict

    i = datetime.now()
    # print str(i)
    time_now = i.strftime('%Y/%m/%d %H:%M:%S')
    # print time_now

    city = jdict['name']
    # print city

    coordinates = jdict['coord']
    print coordinates

    weather_conditions = jdict['weather']
    # print weather_conditions
    # type(weather_conditions)  # list

    for w in weather_conditions:
        # print w
        # type(w)  # dict
        # cloud_cover = w['description']
        weather_summary = w['main']
        # print cloud_cover

    atmospheric_conditions = jdict['main']
    # print atmospheric_conditions
    # type(atmospheric_conditions)  # dict

    humidity_level = atmospheric_conditions['humidity']
    # print humidity_level

    temperature = atmospheric_conditions['temp']

    lows = atmospheric_conditions['temp_min']
    # print lows

    highs = atmospheric_conditions['temp_max']
    # print highs
    if weather_summary == "Rain":
            message = "Do not forget your raincoat or umbrella"

    if temperature > "85":
            message = "Remember to rehydrate"
    else:
        message = "Stay warm"

    # print ("Current time is %s" % time_now)

    # weather_report = '''Weather in %s, %s, temperature is %s, with lows of %s,
    #           highs of %s, humidity is %d''' % (city, cloud_cover, temperature, lows, highs, humidity_level)
    #print weather_report

############################################################################

############################################################################
    return render_template("illnessmap.html",
                           newzip=newzip, newzip_illness_list=newzip_illness_list,
                           city=city, weather_summary=weather_summary, temperature=temperature,
                           lows=lows, highs=highs, humidity_level=humidity_level, message=message)
    # return render_template("illnessmap.html", newzip=newzip, newzip_illness_list=newzip_illness_list)

# ##########################################################################


@app.route('/illness-trends')
def illness_trends():
    """Show illness charts"""

    return render_template("illness_chart.html")


@app.route('/illness-trends.json')
def illness_trends_data():
    """Return trends of illnesses as a chart."""

    # all_reports = db.session.query(Userreport.report)
    # cold = all_reports.filter(Userreport.report.like('%cold%'))
    # cold.all()
    # [(u'cold, flu, cough'), (u'cold, flu, cough')]
    #cold.count()
    # 2
    # justzip_12345 = all_reports.filter(Userreport.zipcode ==12345)
    all_reports = db.session.query(Userreport.report)
    cold = all_reports.filter(Userreport.report.like('%cold%')).count()
    cough = all_reports.filter(Userreport.report.like('%cough%')).count()
    flu = all_reports.filter(Userreport.report.like('%flu%')).count()
    fever = all_reports.filter(Userreport.report.like('%fever%')).count()
    sweats = all_reports.filter(Userreport.report.like('%sweats%')).count()
    chills = all_reports.filter(Userreport.report.like('%chills%')).count()
    sneezing = all_reports.filter(Userreport.report.like('%sneezing%')).count()
    headache = all_reports.filter(Userreport.report.like('%headache%')).count()
    #cold, cough, flu, fever, sweats, chills,  sneezing, severeheadache
    data_list_of_dicts = {
        'userreports': [
            {
                "value": cold,
                "color": "#F7464A",
                "highlight": "#FF5A5E",
                "label": "cold"
            },
            {
                "value": cough,
                "color": "#46BFBD",
                "highlight": "#5AD3D1",
                "label": "cough"
            },
            {
                "value": flu,
                "color": "#FDB45C",
                "highlight": "#FFC870",
                "label": "flu"
            },
            {
                "value": fever,
                "color": "#F7464A",
                "highlight": "#FF5A5E",
                "label": "fever"
            },
            {
                "value": sweats,
                "color": "#46BFBD",
                "highlight": "#5AD3D1",
                "label": "sweats"
            },
            {
                "value": chills,
                "color": "#FDB45C",
                "highlight": "#FFC870",
                "label": "chills"
            },
            {
                "value": sneezing,
                "color": "#46BFBD",
                "highlight": "#5AD3D1",
                "label": "sneezing"
            },
            {
                "value": headache,
                "color": "#FDB45C",
                "highlight": "#FFC870",
                "label": "severe headaches"
            }
        ]
    }
    return jsonify(data_list_of_dicts)

########################################################################


# @app.route('/illnessmarkers')
# def illnessmarkers():
#     """Show map of illnesses with markers. Use this route to show users who is sick in their area using pins"""

#     return render_template("illnessmarkers_map.html")


@app.route('/illnessmarkers.json')
def illnessmarkers_info():
    """JSON information about markers that will be parsed to the map."""

    userreports = {
        userreport.urep_id: {
            "latitude": userreport.latitude,
            "longitude": userreport.longitude,
            "report": userreport.report
        }

        for userreport in Userreport.query.limit(50)}

    return jsonify(userreports)

#########################################################################


# @app.route('/weathermap', methods=['GET'])
# def show_weather_form():
    # '''Displays a form so user can get weather by zip'''

    # return render_template("weathermap.html")


# @app.route('/weathermap', methods=['POST'])
# def process_weather_result():
#     """Display weather conditions for given zipcode."""

#     # openweather_api = os.environ['openweather_api']
#     api_key = 'appid=' + openweather_api
#     # Get form variables
#     userzip = request.form.get("userzip")
#     print userzip

#     # api_key = 'appid=' + openweather_api

#     # print api_key

#     # url2 = 'http://api.openweathermap.org/data/2.5/weather?
#     shortened_url = 'http://api.openweathermap.org/data/2.5/weather'
#     # print shortened_url
#     # final_url = 'http://api.openweathermap.org/data/2.5/weather?{}'.format(api_key)

#     # print final_url
#     # print "please type in your zipcode"
#     # zipcode = '33511'  # hardcode zip for now
#     # zipcode = request.form.get('user_zip')
#     payload = "&" + 'zip=' + userzip + ',us' + "&units=imperial"
#     # print payload

#     r = requests.get(shortened_url, params=api_key + payload)
#     # print r   # gives resposnse 200 everythings ok

#     jdict = r.json()
#     # print jdict

#     # for thing in jdict:
#     #     print thing

#        #  for r in jdict:
#        # ....:     print r
#        # ....:
#        #  clouds
#        #  name
#        #  coord
#        #  sys
#        #  weather
#        #  cod
#        #  base
#        #  dt
#        #  main
#        #  id
#        #  wind

#     i = datetime.now()
#     # print str(i)
#     time_now = i.strftime('%Y/%m/%d %H:%M:%S')
#     # print time_now

#     city = jdict['name']
#     # print city

#     coordinates = jdict['coord']
#     print coordinates

#     weather_conditions = jdict['weather']
#     # print weather_conditions
#     # type(weather_conditions)  # list

#     for w in weather_conditions:
#         # print w
#         # type(w)  # dict
#         cloud_cover = w['description']
#         # print cloud_cover

#     atmospheric_conditions = jdict['main']
#     # print atmospheric_conditions
#     # type(atmospheric_conditions)  # dict

#     humidity_level = atmospheric_conditions['humidity']
#     # print humidity_level

#     temperature = atmospheric_conditions['temp']

#     lows = atmospheric_conditions['temp_min']
#     # print lows

#     highs = atmospheric_conditions['temp_max']
#     # print highs

#     print ("Current time is %s" % time_now)

#     print '''Weather in %s, %s, temperature is %s, with lows of %s,
#               highs of %s, humidity is %d''' % (city, cloud_cover, temperature, lows, highs, humidity_level)
#     weather_report = '''Weather in %s, %s, temperature is %s, with lows of %s,
#               highs of %s, humidity is %d''' % (city, cloud_cover, temperature, lows, highs, humidity_level)

#     return weather_report
#     # return render_template("weathermap.html", weather_report=weather_report)
#     print weather_report


##########################################################################

@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("You have logged out successfully.")
    return redirect("/")


#########################################################################


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
