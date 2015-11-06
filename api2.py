import urllib2
import json

openfda_api = 'XhE8osyrHnhov4iRz5W2dRaffDODrRoJqeDEHGr6'


def fda_search(query):
    api_key = openfda_api
    url = 'https://api.fda.gov/food/enforcement.json?api_key=' + api_key

    reason_for_recall = query.replace(' ', '%20')
    # count = report_date
    final_url = url + "&search=" + "&reason_for_recall:" + reason_for_recall + "&count=report_date"
    json_obj = urllib2.urlopen(final_url)
    data = json.load(json_obj)

    for item in data["results"]:
         # print "item is :" + str(item)
        date = item['time']
        print "date of recall:" + date


fda_search("ice cream")

# urllib2.urlopen('https://api.fda.gov/food/enforcement.json?search=reason_for_recall:%22ice%20cream%22&count=report_date')

# print json.load(urllib2.urlopen('https://api.fda.gov/food/enforcement.json?search=reason_for_recall:%22ice%20cream%22&count=report_date'))

# url = ('https://api.fda.gov/food/enforcement.json?search=reason_for_recall:%22ice%20cream%22&count=report_date')

################################################################################
#declare my variables
# url = ('https://api.fda.gov/food/enforcement.json?api_key=XhE8osyrHnhov4iRz5W2dRaffDODrRoJqeDEHGr6&search=reason_for_recall:%22ice%20cream%22&count=report_date')
# json_obj = urllib2.urlopen(url)
# data = json.load(json_obj)
# # print data["results"]
# #############################################################################
# #iterate over my results
# for item in data["results"]:
#          # print "item is :" + str(item)
#         date = item['time']
#         print "date of recall:" + date

##################################################################################


# def fda_search(query):
#     api_key = openfda_api
#     url = 'https://api.fda.gov/food/enforcement.json?api_key=' + api_key

#     reason_for_recall = query.replace(' ', '%20')
#     # count = report_date
#     final_url = url + "&search=" + "&reason_for_recall:" + reason_for_recall + "&count=report_date"
#     json_obj = urllib2.urlopen(final_url)
#     data = json.load(json_obj)

#     for item in data["results"]:
#          # print "item is :" + str(item)
#         date = item['time']
#         print "date of recall:" + date

# fda_search(ice cream)
