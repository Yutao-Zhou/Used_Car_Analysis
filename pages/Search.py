import streamlit as st
import pandas as pd
import numpy as np
import dask.dataframe as dd
import pickle
import streamlit_authenticator as stauth
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
import Home as H

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

def filterRange(df, latitude, longitude, rangeInKM): #Filter to a square
	minlat = latitude - rangeInKM / 111.699
	maxlat = latitude + rangeInKM / 111.699		#@ poles
	minlong = longitude - rangeInKM / 111.321	#@ equator
	maxlong = longitude + rangeInKM / 111.321	#@ equator
	preFiltedDf = df[(df['lat'] <= maxlat) & (df['lat'] >= minlat) & (df['long'] <= maxlong) & (df['long'] >= minlong)]
	return preFiltedDf

def filterPrice(preFiltedDf, minPrice, maxPrice): 
	priceMatchedDf = preFiltedDf[(preFiltedDf['price'] <= maxPrice) & (preFiltedDf['price'] >= minPrice)]
	return priceMatchedDf

def queryedData(priceMatchedDf, rangeInKM, latitude, longitude):
	for i in range(len(priceMatchedDf)):
		coords_2 = (priceMatchedDf["lat"].iloc[i], priceMatchedDf["long"].iloc[i])
		if GD((latitude, longitude), coords_2).km > rangeInKM:
			priceMatchedDf.at[i, "lat"] = -90
			priceMatchedDf.at[i, "long"] = -180
	queryDf = priceMatchedDf[(priceMatchedDf['lat'] != -90) & (priceMatchedDf['long'] != -180)]
	return queryDf

st.title("Used Car Analyzer")
streetAddress = st.text_area("Enter a location that is convient for you", help = "City name, County name, or Landmark is good enough. (e.g. Columbia University)")
geolocator = Nominatim(user_agent="streamlit")
location = geolocator.geocode(streetAddress)
if location:
	st.markdown("### Query result")
	col1, col2 = st.columns([1,20])
	with col1:
		st.image(location.raw['icon'])
	with col2:
		st.write(location.address)
	if len(location.address.split(",")) < 3:
		st.warning("Please be more specific!")
	else:
		stateName = location.address.split(",")[-2]
		latitude, longitude = location.latitude, location.longitude
		col1, col2, col3, col4 = st.columns(4)
		with col1:
			unit = st.radio("Choose a Unit", options = ["MI", "KM"], index = 0, horizontal = True, help = "Click to change unit")
			with col2:
				if unit == "MI":
					rangeInMI = st.number_input("Listing within MI", min_value = 0.0, max_value = 300.0, step = 10.0, value = 50.0)
					rangeInKM = rangeInMI * 1.6
				if unit == "KM":
					rangeInKM = st.number_input("Listing within KM", min_value = 0.0, max_value = 480.0, step = 10.0, value = 80.0)
		with col3:
			minPrice = st.number_input("Minimum Price", min_value = 1, value = 1000, step = 1000)
		with col4:
			maxPrice = st.number_input("Maximum Price", min_value = minPrice, value = 100000, step = 1000)
		preFiltedDf = filterRange(H.df, latitude, longitude, rangeInKM)
		priceMatchedDf = filterPrice(preFiltedDf, minPrice, maxPrice)
		queryDf = queryedData(priceMatchedDf, rangeInKM, latitude, longitude)
		st.dataframe(queryDf)
		# listingMap(queryDf)
		heatmap(queryDf, "California")