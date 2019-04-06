## Alertsdesk webapp

This app was built in 4 weeks during the Fall 2015 cohort of Hackbright Academy's Software Engineering Fellowship.

Learn more about the developer: www.linkedin.com/in/christinebabu/

### Synopsis

*Alertsdesk is a fullstack web application designed for tracking user generated info about illnesses and other health related alerts

*Integration of Google Maps API allows users to dynamically display the location of each alert

*Users can also get a list of alerts by zipcode

*A dynamic chart summarizes the illness trends using the number of reports querying by reported symptoms

*Alertsdesk uses the OpenWeather API to provide current weather information for given zipcode

### Technology Stack

* [SQLite] - Database contains Users and Userreports
* [SQLAlchemy] - Streamlines database queries
* [Python] - Backend code that manipulates incoming data, controls access to the database, and serves data to the webpage through a framework
* [Flask] - Lightweight web framework which also provides support for jinja templating and unittests
* [Javascript] - Frontend code which allows for dynamic webpages, used to map reports by latitude and longitude
* [jQuery] - A Javascript library that simplifies DOM manipulation, including creating event handlers for user interaction
* [AJAX] - Gets information from server without reloading the page, allowing for more dynamic pages and faster loading    times
* [OpenWeather API] - Uses JSON to provide weather information
* [Google Maps API] - Uses geoJSON passed from the server to create dynamic reports.
* [HTML] - Displays information on the web
* [CSS] - Styles webpages
* [Twitter Bootstrap] - Frontend UI framework for quick styling


### MVP Core Functionality

![alertsdesk_home_page](/static/img/homepage.png)

#### Register new users

*Check registration information against the SQLite database before adding new users to prevent multiple accounts under one email address

![alertsdesk_register_page](/static/img/register.gif)

#### Login/Logout

*Store login information in the session. Log in required to access app features

![alertsdesk_login_page](/static/img/login.gif)

#### Add new report

*Logged in users (verified through session) can add reports to db, see reports they have added, search reports from db, browse map and view illness trends on dynamic chart

*Uses Google Maps API to geocode address on new reports, extracting latitude and longitude for plotting on google maps

![alertsdesk_add_new_report_page](/static/img/addnewreport.gif)

#### Search functionality using zipcode

*Displays current weather data for given zipcode derived from OpenWeather API

*Displays list of reports for given zipcode by querying the database.

![alertsdesk_search_by_zip_page](/static/img/searchbyzip.gif)

#### View illnesses using to Google Maps API:
    
*Users can browse through map to see what illnesses were reported in different areas

![alertsdesk_browse_map](/static/img/browsemap.gif)


#### View trends on Chart

*Users can view dynamic chart plotted using Chart.js to see what illnesses are common

![alertsdesk_view_chart](/static/img/viewchart.gif)

#### Logout

*User logs out of their flask session. All actions performed within their flask session are committed and stored within the database. Reports added during the session can be seen under user profile.

![alertsdesk_logout](/static/img/logout.gif)


### Clone or fork this repo: 
* You will need a secrets.sh file containing api keys for open weather and googlemaps.
* You will also need an app key for the app
```
https://github.com/Geeksten/Alertsdesk.git
```
Create and activate a virtual environment inside your project directory:
```
virtualenv env

source env/bin/activate

source secrets.sh
```
Install the requirements:
```
pip install -r requirements.txt
```
Create the database:
```
python -i model.py

db.create_all()

quit()
```
Run you local server:
```
python server.py
```
Navigate to ```localhost:5000```

### Version 2.0: Add-on Features (in no order):

*Option to sign up for email and/or text alerts

*Option to text a specific number and get top three reports (by count) for specific zipcode

*Integrate with twitter for log in (Oauth) and post to twitter

*Integrate with facebook for log in (Oauth) and post to facebook

*Twilio integration for option to add reports by text

### Contributors

Christine Babu www.linkedin.com/in/christinebabu/
