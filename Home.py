import streamlit as st
import pandas as pd
import numpy as np
import dask.dataframe as dd
import pickle
import streamlit_authenticator as stauth
from pathlib import Path
from generalVisualization import selectedDataVisualization
from stateCode2state import name2code, code2name
from scatterPlot import scatterTrend
from bar_map import state2Coor, listingMap
from manufacturePlot import manufacture
from time import process_time
from Heatmap import heatmap

st.set_page_config(
    page_title = "Used Car Analyzer",
    page_icon = "🏎",
    layout = "wide",
    initial_sidebar_state = "auto",
    menu_items = {"About": "Personal project by Yutao Zhou", "Report a Bug": "https://github.com/Yutao-Zhou", "Get help": "https://yutao-zhou.github.io/CV/"}
)
hide_footer = """
            <style>
            footer {visibility:hidden;}
            </style>
            """
st.markdown(hide_footer, unsafe_allow_html = True)
def sidebar(allRegionInState, stateCode):
    with st.sidebar:
        if stateCode == "United States":
            area = "Entire state"
            minPrice = st.number_input("Minimum Price", min_value = 1, value = 1000, step = 1000)
            maxPrice = st.number_input("Maximum Price", min_value = minPrice, value = 100000, step = 1000)
        else:
            area = "Entire state"
            if type(stateCode) != list:
                area = st.selectbox("Select a region you want to view", (allRegionInState))
            minPrice = st.number_input("Minimum Price", min_value = 1, value = 1000, step = 1000)
            maxPrice = st.number_input("Maximum Price", min_value = minPrice, value = 100000, step = 1000)
    return minPrice, maxPrice, area

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
        totalNumberOfListing = len(df)
    return df, allState, totalNumberOfListing

def selectState(stateCode):
    if type(stateCode) == str:
        state_df = df[df["state"] == stateCode]
    if type(stateCode) == list:
        state_df = df.loc[df['state'].isin(stateCode)]
    return state_df

def dataPreprocessing(state_df, stateCode):
    if type(stateCode) == str:
        allRegionInState = sorted(list(set(state_df["region"])) + ['Entire state'])
        minPrice, maxPrice, area = sidebar(allRegionInState, stateCode)
        if area == "Entire state":
            localCar = state_df
            area = ""
        else:
            localCar = state_df[state_df["region"] == area]
            area = area + ", "
        localCar = localCar[(localCar['price'] <= maxPrice) & (localCar['price'] >= minPrice)]
    if type(stateCode) == list:
        area = ""
        localCar = {}
        minPrice = st.sidebar.number_input("Minimum Price", min_value = 1, value = 1000, step = 1000)
        maxPrice = st.sidebar.number_input("Maximum Price", min_value = minPrice, value = 100000, step = 1000)
        state_df = state_df[(state_df['price'] <= maxPrice) & (state_df['price'] >= minPrice)]
    return state_df, localCar, area, minPrice, maxPrice

def mapOfAveragePrice():
    m = leafmap.Map(center = (38, -122), zoom = 6, locate_control = True)
    m.add_basemap("OpenStreetMap")
    m.to_streamlit(weight = 1000, height = 600)

@st.cache(allow_output_mutation = True, show_spinner = False)
def load_Data(path):
    df, allState, totalNumberOfListing = readData(path)
    return df, allState, totalNumberOfListing

def queryResutls(localCar, totalNumberOfListing):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Numer of cars mathced", len(localCar), "")
    with col2:
        st.metric("Proportion to entire Data Set", f"{round(len(localCar) * 100 / totalNumberOfListing, 2)}%")

t1_start = process_time() 
df, allState, totalNumberOfListing = load_Data("./used_car_us.csv")
st.title("Used Car Analyzer")
#### User Authentication ####
names = ["Guest", "Yutao Zhou", "Ling Cai"]
usernames = ["guest", "yutaozhou", "lingcai"]
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)
authenticator = stauth.Authenticate(names, usernames, hashed_passwords, "Used_Car_Analyzer", "empty", cookie_expiry_days=30)
name, authentication_status, username = authenticator.login("Login", "main")
if authentication_status == False:
    if not username:
        st.warning("Username cannot be empty")
    else:
        st.error("Username and password pair is incorrect")
if authentication_status == None:
    st.info("Please enter your username and password")
if authentication_status:
#### Authentication Finished ####
    st.balloons()
    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome, {name}.")
    st.sidebar.title("Options")
    viewMode = st.sidebar.select_slider(label = "Viewing Mode", options = ['Single Mode', 'Compare Mode'], value = 'Single Mode')
    if viewMode == "Single Mode":
        stateName = st.sidebar.selectbox("Select a state you want to view", (allState), index = 5)
    if viewMode == "Compare Mode":
        onlyStates = allState.copy()
        onlyStates.remove("All States")
        col1, col2 = st.columns(2)
        with col1:
            stateName = st.multiselect("Select states that you want to compare", (onlyStates), help = "Choose as many state as you want", default = None)
    if stateName == []:
        st.markdown("### Choose one state to begin compare!")
    if stateName != []:
        if stateName == "All States":
            with st.container():
                state_df, localCar, area, minPrice, maxPrice = dataPreprocessing(df, "United States")
                queryResutls(localCar, totalNumberOfListing)
                selectedDataVisualization(area, state_df, localCar, "United States")
                mapChosen = st.radio("Map viewing mode", options = ['2D Heatmap', '3D Barmap', 'Both maps'], index = 0, horizontal = True, help = "Click to change view. Try it out!")
                if mapChosen == "3D Barmap":
                    with st.container():
                        listingMap(state_df, stateName)
                if mapChosen == "2D Heatmap":
                    with st.container():
                        heatmap(state_df, stateName)
                if mapChosen == "Both maps":
                    with st.container():
                        heatmap(state_df, stateName)
                    with st.container():
                        listingMap(state_df, stateName)
            with st.container():
                scatterTrend(state_df, minPrice, maxPrice, viewMode)
            with st.container():
                manufacture(state_df, area, stateName)
        else:
            stateCode = name2code(stateName)
            state_df = selectState(stateCode)
            with st.container():
                state_df, localCar, area, minPrice, maxPrice = dataPreprocessing(state_df, stateCode)
                if viewMode == "Single Mode":
                    queryResutls(localCar, totalNumberOfListing)
                    selectedDataVisualization(area, state_df, localCar, stateCode)
                    mapChosen = st.radio("Map viewing mode", options = ['2D Heatmap', '3D Barmap', 'Both maps'], index = 0, horizontal = True, help = "Click to change view. Try it out!")
                    if mapChosen == "3D Barmap":
                        with st.container():
                            listingMap(localCar, stateName)
                    if mapChosen == "2D Heatmap":
                        with st.container():
                            heatmap(localCar, stateName)
                    if mapChosen == "Both maps":
                        with st.container():
                            heatmap(localCar, stateName)
                        with st.container():
                            listingMap(localCar, stateName)
                if viewMode == "Compare Mode":
                    metric1, metric2, metric3 = st.columns(3)
                    with metric1:
                        st.metric("Number of states selected", f"{len(stateName)}/{len(allState)}")
                    with metric2:
                        st.metric("Numer of cars mathced", len(state_df))
                    with metric3:
                        st.metric("Proportion to entire Data Set", f"{round(len(state_df) * 100 / totalNumberOfListing, 2)}%")
                    selectedDataVisualization(area, state_df, localCar, stateCode)
                    with col2:
                        mapChosen = st.radio("Map viewing mode", options = ['2D Heatmap', '3D Barmap', 'Both maps'], index = 0, horizontal = True, help = "Click to change view. Try it out!")
                    if mapChosen == "3D Barmap":
                        with st.container():
                            listingMap(state_df, stateName)
                    if mapChosen == "2D Heatmap":
                        with st.container():
                            heatmap(state_df, stateName)
                    if mapChosen == "Both maps":
                        with st.container():
                            heatmap(state_df, stateName)
                        with st.container():
                            listingMap(state_df, stateName)
            with st.container():
                # p2 = multiprocessing.Process(target = scatterTrend, args = [state_df, minPrice, maxPrice, viewMode])
                # p2.start()
                scatterTrend(state_df, minPrice, maxPrice, viewMode)
            with st.container():
                # p3 = multiprocessing.Process(target = scatterTrend, args = [localCar, area, stateName])
                # p3.start()
                manufacture(localCar, area, stateName)
    t1_stop = process_time()
    st.write(f"Runtime: {round(t1_stop - t1_start, 2)} s")
    # mapOfAveragePrice()
    # geocoder("santa barbara", "ca")