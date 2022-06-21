import streamlit as st
import pandas as pd
import numpy as np
import dask.dataframe as dd
import pickle
import streamlit_authenticator as stauth
import requests
from geopy.geocoders import Nominatim
from geopy.distance import geodesic as GD
from pathlib import Path
from stateCode2state import name2code, code2name
from scatterPlot import scatterTrend
from bar_map import state2Coor, listingMap
from manufacturePlot import manufacture
from time import process_time
from Heatmap import heatmap
from ListingMap import listingMap

st.set_page_config(
    page_title = "Used Car Analyzer",
    page_icon = "🏎",
    layout = "wide",
    initial_sidebar_state = "collapsed",
    menu_items = {"About": "Personal project by Yutao Zhou", "Report a Bug": "https://github.com/Yutao-Zhou", "Get help": "https://yutao-zhou.github.io/CV/"}
)
hide_footer = """
            <style>
            footer {visibility:hidden;}
            </style>
            """
st.markdown(hide_footer, unsafe_allow_html = True)

def readData(path):
    with st.spinner("Loading Data, Please Wait!"):
        dtypes = {
                'state': 'str',
                'region': 'str',
                'lat': 'float32', 
                'long': 'float32',
                'year': 'Int64',
                'odometer': 'Int64',
                'manufacturer': 'str',
                'model': 'str',
                'VIN': 'str', 
                'condition': 'str',
                'cylinders': 'str',
                'drive': 'str',
                'fuel': 'str',
                'paint_color': 'str',
                'size': 'str',
                'title_status': 'str',
                'transmission': 'str',
                'type': 'str'
                }
        dask = dd.read_csv(path, skip_blank_lines=True, usecols = ['state','region','lat', 'long','year','odometer','price','manufacturer', 'model', 'condition', 'cylinders', 'fuel', 'title_status', 'transmission', 'VIN', 'drive', 'size', 'type', 'paint_color'], dtype = dtypes) # more detailed data
        df = dask.compute()
        df.dropna(inplace = True)
        df = df[df['price'] != 0]
        allStateCode = df.state.unique()
        allState = []
        for stateCode in allStateCode:
            allState.append(code2name(stateCode))
        allState = sorted(allState)
        allState = ["All States"] + allState
        totalNumberOfListing = len(df)
    return df, allState, totalNumberOfListing

@st.cache(allow_output_mutation = True, show_spinner = False)
def load_Data(path):
    df, allState, totalNumberOfListing = readData(path)
    return df, allState, totalNumberOfListing

def filterRange(df, latitude, longitude, rangeInKM): #Filter to a square
	minlat = latitude - rangeInKM / 111.699
	maxlat = latitude + rangeInKM / 111.699		#@ poles
	minlong = longitude - rangeInKM / 111.321	#@ equator
	maxlong = longitude + rangeInKM / 111.321	#@ equator
	preFiltedDf = df[(df['lat'] <= maxlat) & (df['lat'] >= minlat) & (df['long'] <= maxlong) & (df['long'] >= minlong)]
	return preFiltedDf

def filterPriceAndBrand(preFiltedDf, minPrice, maxPrice, brand): 
	if "All Brands" in brand:
		priceAndBrandMatchedDf = preFiltedDf[(preFiltedDf['price'] <= maxPrice) & (preFiltedDf['price'] >= minPrice)]
	else:
		priceAndBrandMatchedDf = preFiltedDf[(preFiltedDf['price'] <= maxPrice) & (preFiltedDf['price'] >= minPrice) & (preFiltedDf['manufacturer'].isin(brand))]
	return priceAndBrandMatchedDf

@st.cache(allow_output_mutation = True, show_spinner = False)
def queryedData(priceAndBrandMatchedDf, rangeInKM, latitude, longitude):
	distance = []
	for i in range(len(priceAndBrandMatchedDf)):
		coords_2 = (priceAndBrandMatchedDf["lat"].iloc[i], priceAndBrandMatchedDf["long"].iloc[i])
		distance.append(GD((latitude, longitude), coords_2).km)
	priceAndBrandMatchedDf["distance"] = distance
	queryDf = priceAndBrandMatchedDf[(priceAndBrandMatchedDf["distance"] <= rangeInKM)]
	return queryDf

def advanceModeOptions(queryDf):
	col1, col2, col3, col4, col5 = st.columns(5)
	with col1:
		fuelType = st.radio("Choose fuel type", options = ["Any", "Gasoline", "Diesel", "Other"], index = 0, help = "Click to choose a fuel type of vehicale")
		if fuelType != "Any":
			fuelType = fuelType.lower()
	with col2:
		titleType = st.radio("Choose a title status", options = ["Any", "Clean title", "Rebuilt title", "Salvage title"], index = 0, help = "Click to choose a tilte status")
		conver = {"Any": "Any", "Clean title": "clean", "Rebuilt title": "rebuilt", "Salvage title": "salvage"}
		titleType = conver[titleType]
	with col3:
		transmissionType = st.radio("Choose a transmission type", options = ["Any", "Automatic", "Manual"], index = 0, help = "Click to choose a transmission type")
		if transmissionType != "Any":
			transmissionType = transmissionType.lower()
	with col4:
		driveType = st.radio("Choose a drive type", options = ["Any", "Front Wheel Drive", "Rear Wheel Drive", "All Wheel Drive/4 Wheel Drive"], index = 0, help = "Click to choose a drive type")
		conver = {"Any": "Any", "Front Wheel Drive": "fwd", "Rear Wheel Drive": "rwd", "All Wheel Drive/4 Wheel Drive": "4wd"}
		driveType = conver[driveType]
	with col5:
		nOfCylinders = st.multiselect("Number of cylinders", ["Any", "3 cylinders", "4 cylinders", "5 cylinders", "6 cylinders", "8 cylinders", "10 cylinders", "12 cylinders", "16 cylinders"], default = "Any", help = "Click to choose the number of cinlinders for the engine")
		if "Any" in nOfCylinders:
			nOfCylinders = ["3 cylinders", "4 cylinders", "5 cylinders", "6 cylinders", "8 cylinders", "10 cylinders", "12 cylinders", "16 cylinders"]
	col1, col2, col3, col4 = st.columns([1, 1, 2, 1])
	with col1:
		carCondition = st.radio("Car Condition", options = ["Any", "Excellent", "New", "Like New", "Good", "Fair"], index = 0, help = "Click to choose the current condition of the vehicale")
		if carCondition != "Any":
			carCondition = carCondition.lower()
	with col2:
		bodySize = st.radio("Bodysize of the vehicale", options = ["Any", "Full-Size", "Mid-Size", "Compact", "Sub-Compact"], index = 0, help = "Click to choose a bodysize of the vehicale")
		if bodySize != "Any":
			bodySize = bodySize.lower()
	with col3:
		carType = st.radio("Type of vehicale", options = ["Any", "Sedan", "Coupe", "Convertible", "Wagon", "SUV", "Hatchback", "Pickup", "Truck", "Van", "Mini-Van", "Offroad", "Bus","Other"], index = 0, horizontal = True, help = "Click to choose a type of the vehicale")
		if carType != "Any":
			carType = carType.lower()
	with col4:
		allColor = list(set(queryDf['paint_color'])) + ["Any"]
		allColor = sorted(allColor)
		allColor = [c.capitalize() for c in allColor]
		color = st.multiselect("Choose color of cars that you prefer", allColor, default = "Any")
	return fuelType, nOfCylinders, transmissionType, driveType, titleType, carCondition, bodySize, carType, color

def applyAdvanceFilter(queryDf, fuelType, nOfCylinders, transmissionType, driveType, titleType, carCondition, bodySize, carType, color):
	advanceDf = queryDf.copy(deep = True)
	if "Any" not in nOfCylinders:
		advanceDf = advanceDf[(advanceDf['cylinders'].isin(nOfCylinders))]
	if fuelType != "Any":
		advanceDf = advanceDf[(advanceDf['fuel'] == fuelType)]
	if transmissionType != "Any":
		advanceDf = advanceDf[(advanceDf['transmission'] == transmissionType)]
	if driveType != "Any":
		advanceDf = advanceDf[(advanceDf['drive'] == driveType)]
	if titleType != "Any":
		advanceDf = advanceDf[(advanceDf['title_status'] == titleType)]
	if carCondition != "Any":
		advanceDf = advanceDf[(advanceDf['condition'] == carCondition)]
	if bodySize != "Any":
		advanceDf = advanceDf[(advanceDf['size'] == bodySize)]
	if carType != "Any":
		advanceDf = advanceDf[(advanceDf['type'] == carType)]
	if "Any" not in color:
		advanceDf = advanceDf[(advanceDf['paint_color'].isin(color))]
	return advanceDf


st.title("Used Car Analyzer")
df, allState, totalNumberOfListing = load_Data("./used_car_us.csv")
streetAddress = st.text_area("Enter a location that is convient for you",  value = "nyc", help = "City name, County name, or Landmark is good enough. (e.g. Columbia University)")
geolocator = Nominatim(user_agent="streamlit")
location = geolocator.geocode(streetAddress)
if streetAddress:
	if not location:
		st.info("No location founded!")
	if location:
		st.markdown("### Query result")
		col1, col2 = st.columns([1,20])
		if "icon" in location.raw:
			with col1:
				st.image(location.raw['icon'])
		with col2:
			st.write(location.address)
		if len(location.address.split(",")) < 3:
			st.warning("Please be more specific!")
		else:
			stateName = location.address.split(",")[-2]
			latitude, longitude = location.latitude, location.longitude
			col1, col2, col3, col4, col5 = st.columns(5)
			with col1:
				unit = st.radio("Choose a Unit", options = ["Miles", "Kilometers"], index = 0, horizontal = True, help = "Click to change unit")
				with col2:
					if unit == "Miles":
						rangeInMI = st.number_input("Listing within MI", min_value = 0.0, max_value = 300.0, step = 10.0, value = 50.0)
						rangeInKM = rangeInMI * 1.6
					if unit == "Kilometers":
						rangeInKM = st.number_input("Listing within KM", min_value = 0.0, max_value = 480.0, step = 10.0, value = 80.0)
			with col3:
				minPrice = st.number_input("Minimum Price", min_value = 1, value = 1000, step = 1000)
			with col4:
				maxPrice = st.number_input("Maximum Price", min_value = minPrice, value = 100000, step = 1000)
			with col5:
				brandName = ["All Brands"] + sorted(list(set(df["manufacturer"])))
				brand = st.multiselect("Carb Brand(s)", brandName, default = "All Brands")
			detailedFilter = st.checkbox("Advanced mode(more detailed filters)", help = "Click to show more filter like cylinder, drive type, body type, etc.")
			preFiltedDf = filterRange(df, latitude, longitude, rangeInKM)
			priceAndBrandMatchedDf = filterPriceAndBrand(preFiltedDf, minPrice, maxPrice, brand)
			queryDf = queryedData(priceAndBrandMatchedDf, rangeInKM, latitude, longitude)
			if not detailedFilter:
				if len(queryDf) == 0:
					st. warning("No car match! Please change the query.")
				if len(queryDf) > 0:
					metric1, metric2 = st.columns(2)
					with metric1:
						st.metric("Numer of cars mathced", len(queryDf))
					with metric2:
						st.metric("Proportion to entire Data Set", f"{round(len(queryDf) * 100 / totalNumberOfListing, 2)}%")
				st.dataframe(queryDf)
				listingMap(queryDf)
			if detailedFilter:
				fuelType, nOfCylinders, transmissionType, driveType, titleType, carCondition, bodySize, carType, color = advanceModeOptions(queryDf)
				if len(queryDf) == 0:
					st. warning("No car match! Please change the query.")
				if len(queryDf) > 0:
					advanceDf = applyAdvanceFilter(queryDf, fuelType, nOfCylinders, transmissionType, driveType, titleType, carCondition, bodySize, carType, color)
					metric1, metric2 = st.columns(2)
					with metric1:
						st.metric("Numer of cars mathced", len(queryDf))
					with metric2:
						st.metric("Proportion to entire Data Set", f"{round(len(queryDf) * 100 / totalNumberOfListing, 2)}%")
				st.dataframe(advanceDf)
				listingMap(advanceDf)
			VIN = st.text_area("VIN Look Up tool. Enter the VIN of a vehicle that you are interested!", value = "1FD0X5HT6FEC65813")
			if VIN:
				URL = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/{VIN}?format=json"
				r = requests.get(URL)
				if r.status_code == 200:
					data = r.json()["Results"][0]
					for k, v in data.items():
						if v != "":
							st.write(f"{k}:{v}")
				else:
					st.warning("Wrong VIN please enter again")