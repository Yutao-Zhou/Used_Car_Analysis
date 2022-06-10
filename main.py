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
        area = st.selectbox("select a region you want to view", (allRegionInCA))
        minPrice = st.number_input("Minimum Listing Price", min_value = 0, value = 1000, step = 1000)
        maxPrice = st.number_input("Maximum Listing Price", min_value = 0, value = 1000000, step = 1000)
    return minPrice, maxPrice, area

def readData(path):
    with st.spinner("Loading, Please Wait!"):
        df = pd.read_csv(path, usecols = ['id','state','region','lat', 'long','year','odometer','price','manufacturer', 'model'], dtype = {'price': "int64"})
        df.dropna(inplace = True)
        df = df.loc[df['price'] != 0]
        df['year'] = df['year'].astype('int64')
        allState = list(set(df["state"]))
        allState.append("All States")
        allState = sorted(allState)
    return df, allState

def selectState(stateCode):
    state_df = df.loc[df["state"] == stateCode]
    state_df = state_df.drop(columns=["state"])
    return state_df

def countyDataVisualization(state_df):
    allRegionInCA = set(state_df["region"])
    minPrice, maxPrice, area = sidebar(allRegionInCA)
    localCar = state_df.loc[state_df["region"] == area]
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

def listingMap(data):
    from bar_map import pydeckMap
    pydeckMap(data)

def mapOfAveragePrice():
    m = leafmap.Map(center = (38, -122), zoom = 6, locate_control = True)
    m.add_basemap("OpenStreetMap")
    m.to_streamlit(weight = 1000, height = 600)

@st.cache(allow_output_mutation = True)
def load_model(path):
    df, allState = readData(path)
    return df, allState

# df, allState = readData("C:/Users/13520/Documents/GitHub/Used_Car_Analysis/used_car_us.csv")
df, allState = load_model("C:/Users/13520/Documents/GitHub/Used_Car_Analysis/used_car_us.csv")

stateCode = st.sidebar.selectbox("select a region you want to view", (allState))
if stateCode == "All States":
    state_df = df
else:
    state_df = selectState(stateCode)
with st.container():
    countyDataVisualization(state_df)
    listingMap(state_df)
# mapOfAveragePrice()
# geocoder("santa barbara", "ca")