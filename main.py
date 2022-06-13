import streamlit as st
import pandas as pd
import numpy as np
import dask.dataframe as dd
# import leafmap.foliumap as leafmap
from stateCode2state import name2code, code2name
from scatterPlot import scatterTrend
from bar_map import listingMap
from manufacturePlot import manufacture

st.set_page_config(
    page_title="Used Car Analyzer",
    page_icon="",
    layout = "wide",
    initial_sidebar_state = "auto",
    menu_items = {"About": "Personal project by Yutao Zhou"}
)

st.title("Used Car Analyzer")

def sidebar(allRegionInState, stateCode):
    with st.sidebar:
        if stateCode == "United States":
            area = "Entire state"
            minPrice = st.number_input("Minimum Price", min_value = 0, value = 1000, step = 1000)
            maxPrice = st.number_input("Maximum Price", min_value = 0, value = 100000, step = 1000)
        else:
            area = st.selectbox("Select a region you want to view", (allRegionInState))
            minPrice = st.number_input("Minimum Price", min_value = 0, value = 1000, step = 1000)
            maxPrice = st.number_input("Maximum Price", min_value = 0, value = 100000, step = 1000)
    return minPrice, maxPrice, area

def readData(path):
    with st.spinner("Loading, Please Wait!"):
        dtypes = {
                'state': 'str',
                'region': 'str',
                'lat': 'float32', 
                'long': 'float32',
                'year': 'Int64',
                'odometer': 'Int64',
                'manufacturer': 'str',
                'model': 'str'
                }
        dask = dd.read_csv(path, skip_blank_lines=True, usecols = ['state','region','lat', 'long','year','odometer','price','manufacturer', 'model'], dtype = dtypes)
        df = dask.compute()
        df.dropna(inplace = True)
        df = df[df['price'] != 0]
        allStateCode = df.state.unique()
        allState = []
        for stateCode in allStateCode:
            allState.append(code2name(stateCode))
        allState = sorted(allState)
        allState = ["All States"] + allState
    return df, allState

def selectState(stateCode):
    if type(stateCode) == str:
        state_df = df[df["state"] == stateCode]
    if type(stateCode) == list:
        state_df = df.loc[df['state'].isin(stateCode)]
    return state_df

def countyDataVisualization(state_df, stateCode):
    if type(stateCode) == str:
        allRegionInState = sorted(list(set(state_df["region"])) + ['Entire state'])
        minPrice, maxPrice, area = sidebar(allRegionInState, stateCode)
        if area == "Entire state":
            localCar = state_df
            area = ""
        else:
            localCar = state_df[state_df["region"] == area]
            area = area + ", "
        localCar = localCar[(localCar['price'] != 0) & (localCar['price'] < maxPrice) & (localCar['price'] > minPrice)]
        n, averagePrice, averageYear = calcuateAveragePrice(localCar)
        state_name = code2name(stateCode)
        st.markdown(f"There are **{n}** listed car in **{area}{state_name}**. The average model year is **{averageYear}**. The average price is **{averagePrice}** USD($).")
        with st.expander("Click to view data"):
            st.dataframe(localCar,1000,500)
    if type(stateCode) == list:
        area = ""
        localCar = {}
        minPrice = st.sidebar.number_input("Minimum Price", min_value = 0, value = 1000, step = 1000)
        maxPrice = st.sidebar.number_input("Maximum Price", min_value = 0, value = 100000, step = 1000)
        state_df = state_df[(state_df['price'] != 0) & (state_df['price'] < maxPrice) & (state_df['price'] > minPrice)]
        for c in stateCode:
            oneState = state_df[state_df['state'] == c]
            localCar[c] = oneState
            n, averagePrice, averageYear = calcuateAveragePrice(oneState)
            state_name = code2name(c)
            st.markdown(f"There are **{n}** listed car in **{area}{state_name}**. The average model year is **{averageYear}**. The average price is **{averagePrice}** USD($).")
            with st.expander("Click to view data"):
                st.dataframe(oneState,1000,500)
    return localCar, area, minPrice, maxPrice

def calcuateAveragePrice(localCar):
    n = len(localCar)
    totalYear = localCar['year'].sum(axis= 0)
    totalPrice = localCar['price'].sum(axis = 0)
    averagePrice = totalPrice // n
    averageYear = totalYear // n
    return n, averagePrice, averageYear

def mapOfAveragePrice():
    m = leafmap.Map(center = (38, -122), zoom = 6, locate_control = True)
    m.add_basemap("OpenStreetMap")
    m.to_streamlit(weight = 1000, height = 600)

@st.cache(allow_output_mutation = True, show_spinner = False)
def load_model(path):
    df, allState = readData(path)
    return df, allState

df, allState = load_model("C:/Users/13520/Documents/GitHub/Used_Car_Analysis/used_car_us.csv")
viewMode = st.sidebar.select_slider(label = "Viewing Mode", options = ['Single Mode', 'Compare Mode'], value = 'Compare Mode')
if viewMode == "Single Mode":
    stateName = st.sidebar.selectbox("Select a state you want to view", (allState), index = 5)
if viewMode == "Compare Mode":
    stateName = st.multiselect("Select states that you want to compare", (allState), default = None)
if stateName == []:
    st.markdown("## Choose one state to begin compare!")
if stateName != []:
    if stateName == "All States":
        with st.container():
            localCar, area, minPrice, maxPrice = countyDataVisualization(df, "United States")
            listingMap(localCar)
        with st.container():
            scatterTrend(localCar, minPrice, maxPrice, viewMode)
        with st.container():
            manufacture(localCar, area, stateName)
            
    else:
        stateCode = name2code(stateName)
        state_df = selectState(stateCode)
        with st.container():
            localCar, area, minPrice, maxPrice = countyDataVisualization(state_df, stateCode)
            if viewMode == "Single Mode":
                listingMap(localCar)
            if viewMode == "Compare Mode":
                listingMap(state_df)
        with st.container():
            scatterTrend(state_df, minPrice, maxPrice, viewMode)
        with st.container():
            manufacture(localCar, area, stateName)
            
# mapOfAveragePrice()
# geocoder("santa barbara", "ca")