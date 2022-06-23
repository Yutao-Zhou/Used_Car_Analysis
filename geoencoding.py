import requests
import csv
from geopy.geocoders import Nominatim
import streamlit as st

def geocoder(county, state):
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {'sensor': 'false', 'address': f'{county}, {state}', "key": "AIzaSyCGzBsXrhvBlwQ8RO2dulq6A2Qv2nUgh-Y"}
    r = requests.get(url, params=params)
    results = r.json()['results']
    if results:
        location = results[0]['geometry']['location']
        latitude = location['lat']
        longtitude = location['lng']
        st.write(location['lat'], location['lng'])
        writeCSV(csvFilePath, county, state, latitude, longtitude)
        return location['lat'], location['lng']
    if not results:
        return "Location not found "

def writeCSV(csvFilePath, county, state, latitude, longtitude):
    
    with open('county2latitude.csv', 'w', newline='') as csvFilePath:
        spamwriter = csv.writer(csvFilePath, delimiter=',')
        spamwriter.writerow(['county', 'state', 'latitude', 'longitude'])
        spamwriter.writerow([county, state, latitude, longtitude])

def coordinate2Address(latitude, longtitude):
    coordinates = f"{latitude}, {longtitude}"
    geolocator = Nominatim(user_agent = "streamlit")
    location = geolocator.reverse(coordinates)
    return location.address