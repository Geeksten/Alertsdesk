# openweather api
from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Userreport, Reportsymptom
from model import Symptom, State, Staterecall, Fdarecall
import requests
import pprint
from datetime import datetime
import os

openweather_api = os.environ['openweather_api']
api_key = 'appid=' + openweather_api

# openweather_api = '27300f2017feaf811a4170ce642bc5f1'
# api_key = 'appid=' + openweather_api

# print api_key

# url2 = 'http://api.openweathermap.org/data/2.5/weather?appid=27300f2017feaf811a4170ce642bc5f1&zip=33511,us'
shortened_url = 'http://api.openweathermap.org/data/2.5/weather'
# print shortened_url
# final_url = 'http://api.openweathermap.org/data/2.5/weather?{}'.format(api_key)

# print final_url
# print "please type in your zipcode"
zipcode = '33511'  # hardcode zip for now
# zipcode = request.form.get('user_zip')
payload = "&" + 'zip=' + zipcode + ',us'
# print payload

r = requests.get(shortened_url, params=api_key + payload)
# print r   # gives resposnse 200 everythings ok

jdict = r.json()
# print jdict

# for thing in jdict:
#     print thing

   #  for r in jdict:
   # ....:     print r
   # ....:
   #  clouds
   #  name
   #  coord
   #  sys
   #  weather
   #  cod
   #  base
   #  dt
   #  main
   #  id
   #  wind

i = datetime.now()
# print str(i)
time_now = i.strftime('%Y/%m/%d %H:%M:%S')
# print time_now

city = jdict['name']
# print city

coordinates = jdict['coord']
# print coordinates

weather_conditions = jdict['weather']
# print weather_conditions
# type(weather_conditions)  # list

for w in weather_conditions:
    # print w
    # type(w)  # dict
    cloud_cover = w['description']
    # print cloud_cover

atmospheric_conditions = jdict['main']
# print atmospheric_conditions
# type(atmospheric_conditions)  # dict

humidity_level = atmospheric_conditions['humidity']
# print humidity_level

lows = atmospheric_conditions['temp_min']
# print lows

highs = atmospheric_conditions['temp_max']
# print highs


print ("Current time is %s" % time_now)

print '''Weather in %s, %s, with lows of %s,
          highs of %s, humidity is %d''' % (city, cloud_cover, lows, highs, humidity_level)



#     artistName = jdict['results'][i].get('artistName')

# num_results = jdict['resultCount']

# for i in range(num_results):
#     trackName = jdict['results'][i].get('trackName')
#     artistName = jdict['results'][i].get('artistName')
#     print "%s : %s" % (trackName, artistName)
######################################################################
#r = requests.get("https://itunes.apple.com/search?term=watermelon")
# payload = {'term': 'watermelon'}
# r = requests.get("https://itunes.apple.com/search", params=payload)

# jdict = r.json()

# num_results = jdict['resultCount']

# for i in range(num_results):
#     trackName = jdict['results'][i].get('trackName')
#     artistName = jdict['results'][i].get('artistName')
#     print "%s : %s" % (trackName, artistName)
