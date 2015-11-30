##Alertsdesk webapp
Learn more about the developer: www.linkedin.com/in/christinebabu/

##Synopsis
*Alertsdesk is a fullstack web application designed for tracking user generated info about illnesses and other health related alerts

*Integration of Google Maps API allows users to dynamically display the location of each alert

*Users can also get a list of alerts by zipcode

*A dynamic chart summarizes the illness trends using the number of reports querying by reported symptoms

*Alertsdesk uses the OpenWeather API to provide current weather information for given zipcode


##MVP Core Functionality

*Register new users
    Check registration information against the database before adding new users to prevent multiple accounts under one email address

*Login/Logout:
    Store login information in the session. Log in required to access app features

*Add reports
    Logged in users can add reports, search reports nad view trends on chart

*Connect to Google Maps API
    Provides geolocation and helps map user-added reports using latitude and longitude

*Search functionality
    Allows users to search for reports using zipcode
   
*Connect to OpenWeather API
    When user searches for illness reports by zipcode, the app also displays current weather for the given zipcode


##Add-on Features (in no order):

*Option to sign up for email and/or text alerts

*Option to text a specific number and get top three reports (by count) for specific zipcode

*Integrate with twitter for log in (Oauth) and post to twitter

*Integrate with facebook for log in (Oauth) and post to facebook

*Twilio integration for option to add reports by text

##API Reference

*Google Maps
*OpenWeather

##Contributors

Christine Babu www.linkedin.com/in/christinebabu/