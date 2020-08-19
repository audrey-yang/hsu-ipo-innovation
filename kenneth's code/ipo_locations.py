########################################################################################################################
# IPO Get Location Data
#
# Kenneth Shinn
# kshinn@seas.upenn.edu
#
# Directions: put the ipo data in a folder called 'firms'.
# This script should be in its own folder (and this folder can be called whatever).
# Creates a new file called "IPO" locations that is the same as initial data set with the location data
#
# NOTE: the locations returned by this script are not good. Probably useless for the project, but could 
#       be useful in another application
#
########################################################################################################################

import csv
import requests
import json

ipo_file = open('../firms/ipo.csv', encoding='utf-8-sig')
ipo = csv.DictReader(ipo_file, delimiter=",")

# create an output file
output = open('../outputs/ipo_with_locations.csv', 'w', newline="\n", encoding='utf-8-sig')
name_matches = csv.writer(output, delimiter=',')
header = ['ipo_date', 'firm', 'ticker', 'offer_price', 'opening_price', 'first_day_close',
          'latitude', 'longitude', 'country', 'city', 'confidence']
name_matches.writerow(header)


ipo_size = len([1 for i in ipo])
print('ipo size: ' + str(ipo_size))
ipo_file.seek(0)  # rewind file
ipo.__next__()

# count for progress
cnt = 0
previous_percent = 0

for row in ipo:
    firm = row['firm'].strip()
    ticker = row['ticker'].strip()
    offer_price = row['offer_price'].strip()
    opening_price = row['opening_price'].strip()
    first_day_close = row['first_day_close'].strip()
    ipo_date = row['ipo_date'].strip()

    # query = firm + ' headquarters'
    query = 'Google headquarters'
    print(query)
    response = requests.get("http://dev.virtualearth.net/REST/v1/Locations/" + query + "?",
                            params={"include": "queryParse",
                                    "key": "AgUSM867a3r-7GFqCUQ81nvWLngFtrbanaBzA41qVEDoN-PFSEQiCTtx0eY9aJ--"})

    data = response.json()
    location_data = data['resourceSets'][0]['resources'][0]
    lat = location_data['point']['coordinates'][0]
    lng = location_data['point']['coordinates'][1]
    country = location_data['address']['countryRegion']
    city = location_data['address']['locality']
    confidence = location_data['confidence']

    print(firm)
    print(lat)
    print(lng)
    print(country)
    print(city)
    print(confidence)

    print(json.dumps(data, indent=4, sort_keys=True))

    break







