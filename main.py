import streamlit as st
import pandas as pd
import numpy as np
import dask.dataframe as dd
# import leafmap.foliumap as leafmap
from stateCode2state import name2code, code2name

st.set_page_config(
    page_title="Used Car Analyzer",
    page_icon="",
    layout = "wide",
    initial_sidebar_state = "auto",
    menu_items = {"About": "Personal project by Yutao Zhou"}
)

st.title("Used Car Analyzer")

def sidebar(allRegionInCA, stateCode):
    with st.sidebar:
        if stateCode == "USA":
            area = "Entire state"
            minPrice = st.number_input("Minimum Price", min_value = 0, value = 1000, step = 1000)
            maxPrice = st.number_input("Maximum Price", min_value = 0, value = 100000, step = 1000)
        else:
            area = st.selectbox("Select a region you want to view", (allRegionInCA))
            minPrice = st.number_input("Minimum Price", min_value = 0, value = 1000, step = 1000)
            maxPrice = st.number_input("Maximum Price", min_value = 0, value = 100000, step = 1000)
    return minPrice, maxPrice, area

def readData(path):
    with st.spinner("Loading, Please Wait!"):
        from google.oauth2 import service_account
        from google.cloud import storage

        # Create API client.
        credentials = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"]
        )
        client = storage.Client(credentials=credentials)

        # Retrieve file contents.
        # Uses st.experimental_memo to only rerun when the query changes or after 10 min.
        @st.experimental_memo(ttl=600)
        def read_file(bucket_name, file_path):
            bucket = client.bucket(bucket_name)
            content = bucket.blob(file_path).download_as_string().decode("utf-8")
            return content

        bucket_name = "us_used_car_data"
        file_path = "used_car_us.csv"

        content = read_file(bucket_name, file_path)

        # dtypes = {'id': 'uint8',
        #         'state': 'str',
        #         'region': 'str',
        #         'lat': 'float32', 
        #         'long': 'float32',
        #         'manufacturer': 'str',
        #         'model': 'str'
        #         }
        # dask = dd.read_csv(path, skip_blank_lines=True, usecols = ['id','state','region','lat', 'long','year','odometer','price','manufacturer', 'model'], dtype = dtypes)
        # df = dask.compute()
        df = content
        df.dropna(inplace = True)
        df = df.loc[df['price'] != 0]
        df['year'] = df['year'].astype('int64')
        allStateCode = list(set(df["state"]))
        allState = []
        for stateCode in allStateCode:
            allState.append(code2name(stateCode))
        allState = sorted(allState)
        allState = ["All States"] + allState
    return df, allState

def selectState(stateCode):
    state_df = df[df["state"] == stateCode]
    return state_df

def countyDataVisualization(state_df, stateCode):
    allRegionInState = sorted(list(set(state_df["region"])) + ['Entire state'])
    minPrice, maxPrice, area = sidebar(allRegionInState, stateCode)
    if area == "Entire state":
        localCar = state_df
        area = ""
    else:
        localCar = state_df[state_df["region"] == area]
        area = area + ", "
    localCar = localCar[(localCar['price'] != 0) & (localCar['price'] < maxPrice) & (localCar['price'] > minPrice)]
    n = len(localCar)
    totalYear = localCar['year'].sum(axis= 0)
    totalPrice = localCar['price'].sum(axis = 0)
    averagePrice = totalPrice // n
    averageYear = totalYear // n
    st.write(f"There are {n} listed car in {area}{stateCode}. The average model year is {averageYear}. The average price is {averagePrice} USD($).")
    with st.expander("Click to view data"):
        st.dataframe(localCar,1000,500)
    scatterTrend(localCar)
    return localCar

def scatterTrend(localCar):
    import plotly.express as px
    yearVSprice = pd.DataFrame(data = {"Year of Make":localCar['year'], "Price of Car in USD($)":localCar['price']})
    trendoptions = ["Ordinary Least Squares", "Locally Weighted Scatterplot Smoothing", "Moving Averages", "Expanding mean", "Expanding Maximum"]
    col1, col2, col3 = st.columns(3)
    with col1:
        trendSelected = st.selectbox("Select a trandline you want to use", (trendoptions), index  = 1, )
    with col2:
        cScatter = st.color_picker("Pick a color for the scatter", value = "#48D1EA")
    with col3:
        cTrend = st.color_picker("Pick a color for the trendline", value = "#FF0000")
    if trendSelected == "Ordinary Least Squares":
        fig = px.scatter(yearVSprice, x = "Year of Make", y = "Price of Car in USD($)", color_discrete_sequence=[cScatter], trendline = "ols", trendline_color_override = cTrend)
    if trendSelected == "Locally Weighted Scatterplot Smoothing":
        frac = st.slider("Choose a fraction numer for your LOWESS", value = 0.5, min_value = 0.01, max_value = 0.99, step = 0.01, help = "Lowering this fraction will give a line that more closely follows the data")
        fig = px.scatter(yearVSprice, x = "Year of Make", y = "Price of Car in USD($)", color_discrete_sequence=[cScatter], trendline = "lowess", trendline_options = dict(frac = frac), trendline_color_override = cTrend)
    if trendSelected == "Moving Averages":
        window = st.slider("Choose a window numer for your Moving Averages", value = 5, min_value = 1, max_value = 10, step = 1)
        fig = px.scatter(yearVSprice, x = "Year of Make", y = "Price of Car in USD($)", color_discrete_sequence=[cScatter],  trendline="rolling", trendline_options=dict(window = window), trendline_color_override = cTrend)
    if trendSelected == "Expanding mean":
        fig = px.scatter(yearVSprice, x = "Year of Make", y = "Price of Car in USD($)", color_discrete_sequence=[cScatter], trendline = "expanding", trendline_color_override = cTrend)
    if trendSelected == "Expanding Maximum":
        fig = px.scatter(yearVSprice, x = "Year of Make", y = "Price of Car in USD($)", color_discrete_sequence=[cScatter], trendline = "expanding", trendline_options=dict(function="max"), trendline_color_override = cTrend)
    st.plotly_chart(fig, use_container_width = True)

def listingMap(data):
    from bar_map import pydeckMap
    pydeckMap(data)

def mapOfAveragePrice():
    m = leafmap.Map(center = (38, -122), zoom = 6, locate_control = True)
    m.add_basemap("OpenStreetMap")
    m.to_streamlit(weight = 1000, height = 600)

@st.cache(allow_output_mutation = True, show_spinner = False)
def load_model(path):
    df, allState = readData(path)
    return df, allState

df, allState = load_model("C:/Users/13520/Documents/GitHub/Used_Car_Analysis/used_car_us.csv")
stateName = st.sidebar.selectbox("Select a state you want to view", (allState))
if stateName == "All States":
    with st.container():
        localcar = countyDataVisualization(df, "USA")
        listingMap(localcar)
else:
    stateCode = name2code(stateName)
    state_df = selectState(stateCode)
    with st.container():
        localcar = countyDataVisualization(state_df, stateName)
        listingMap(localcar)
# mapOfAveragePrice()
# geocoder("santa barbara", "ca")