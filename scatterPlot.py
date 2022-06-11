import streamlit as st
import pandas as pd
import plotly.express as px
def scatterTrend(localCar):
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