import streamlit as st
import pandas as pd
import numpy as np
import leafmap.foliumap as leafmap
import plotly.express as px

st.set_page_config(
    page_title="Used Car Analyzer",
    page_icon="",
    layout = "wide",
    initial_sidebar_state = "auto",
    menu_items = {"About": "Personal project by Yutao Zhou"}
)

st.title("Used Car Analyzer")

def sidebar(allRegionInCA):
    with st.sidebar:
        # model = ["gensim"]
        #
        # text_input = st.sidebar.text_input("Enter a word you want to query", 'good')
        # s_station = st.sidebar.selectbox('Select a modole', model, key='usedmodel',
        #                          help="Which model you want to use to search relevent words?")
        #
        # multi_select = st.sidebar.multiselect('multiselection', model, default=["gensim"])
        # slider_input = st.sidebar.slider('year', 0.01, 1.00, 0.01)
        minPrice = st.number_input("Minimum Listing Price", min_value = 0, value = 1000, step = 1000)
        maxPrice = st.number_input("Maximum Listing Price", min_value = 0, value = 1000000, step = 1000)
        area = st.selectbox("select a region you want to view", (allRegionInCA))
    return minPrice, maxPrice, area

def readData(path):
    df = pd.read_csv(path, nrows = 50000, usecols = ['id','state','region','lat', 'long','year','odometer','price','manufacturer', 'model'], dtype = {'price': "int64"})
    print(df.columns)
    df.dropna(inplace = True)
    df = df.loc[df['price'] != 0]
    df['year'] = df['year'].astype('int64')
    print(df.head(400))
    CAdf = df.loc[df["state"] == "ca"]
    CAdf = CAdf.drop(columns=["state"])
    return CAdf
    print(CAdf)

def countyDataVisualization(CAdf):
    allRegionInCA = set(CAdf["region"])
    minPrice, maxPrice, area = sidebar(allRegionInCA)
    localCar = CAdf.loc[CAdf["region"] == area]
    n = len(localCar)
    year = localCar['year'].tolist()
    price = localCar['price'].tolist()
    i = 0
    while i < len(price):
        if price[i] == 0 or price[i] < minPrice or price[i] > maxPrice:
            year.pop(i)
            price.pop(i)
        else:
            i += 1
    averagePrice = sum(price) // len(price)
    averageYear = sum(year) // len(year)
    st.write(f"There are {n} listing car in {area}. The average model year is {averageYear}. The average listing price is {averagePrice} USD($).")
    yearVSprice = pd.DataFrame(data = {"Year of Make":year, "Listing Price of Car in USD($)":price})
    with st.expander("Click to view data"):
        st.dataframe(localCar,1000,500)
    fig = px.scatter(yearVSprice, x = "Year of Make", y = "Listing Price of Car in USD($)", trendline="lowess", trendline_options=dict(frac=0.8))
    st.plotly_chart(fig, use_container_width = True)

def listingMap(df):
    from bar_map import *
    pydeckMap(data)


def mapOfAveragePrice():
    m = leafmap.Map(center = (38, -122), zoom = 6, locate_control = True)
    m.add_basemap("OpenStreetMap")
    m.to_streamlit(weight = 1000, height = 600)

def geocoder(county, state):
    import requests
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
    import csv
    with open('county2latitude.csv', 'w', newline='') as csvFilePath:
        spamwriter = csv.writer(csvFilePath, delimiter=',')
        spamwriter.writerow(['county', 'state', 'latitude', 'longitude'])
        spamwriter.writerow([county, state, latitude, longtitude])


CAdf = readData("C:/Users/13520/Documents/GitHub/Used_Car_Analysis/used_car_us.csv")
with st.container():
    countyDataVisualization(CAdf)

# mapOfAveragePrice()
# geocoder("santa barbara", "ca")