import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def scatterTrend(localCar, minPrice, maxPrice, viewMode):
    with st.spinner("Loading scatter plot"):
        if viewMode == "Single Mode":
            yearVSprice = pd.DataFrame(data = {"Year of Make":localCar['year'], "Price of Car in USD($)":localCar['price']})
            trendoptions = ["Locally Weighted Scatterplot Smoothing", "Moving Averages", "Expanding mean", "Expanding Maximum"]
            col1, col2, col3, col4 = st.columns([2,1,1,1])
            with col1:
                trendSelected = st.selectbox("Select a trendlines you want to use", (trendoptions), index  = 0, )
            with col2:
                cScatter = st.color_picker("Pick a color for the scatter", value = "#48D1EA")
            with col3:
                cTrend = st.color_picker("Pick a color for the trendline", value = "#FF0000")
            if trendSelected == "Locally Weighted Scatterplot Smoothing":
                frac = st.slider("Choose a fraction numer for your LOWESS", value = 0.5, min_value = 0.01, max_value = 0.99, step = 0.01, help = "Lowering this fraction will give a line that more closely follows the data")
                fig = px.scatter(yearVSprice, x = "Year of Make", y = "Price of Car in USD($)", color_discrete_sequence=[cScatter], trendline = "lowess", trendline_options = dict(frac = frac), trendline_color_override = cTrend)
                with col4:
                    if st.checkbox("Hide date points in the scatter plot", value = True, help = "Uncheck to see data points"):
                        fig.update_traces(visible = False, selector = dict(mode = "markers"))
            if trendSelected == "Moving Averages":
                window = st.slider("Choose a window numer for your Moving Averages", value = 5, min_value = 1, max_value = 10, step = 1)
                fig = px.scatter(yearVSprice, x = "Year of Make", y = "Price of Car in USD($)", color_discrete_sequence=[cScatter],  trendline="rolling", trendline_options=dict(window = window), trendline_color_override = cTrend)
                with col4:
                    if st.checkbox("Hide date points in the scatter plot", value = True, help = "Uncheck to see data points"):
                        fig.update_traces(visible = False, selector = dict(mode = "markers"))
            if trendSelected == "Expanding mean":
                fig = px.scatter(yearVSprice, x = "Year of Make", y = "Price of Car in USD($)", color_discrete_sequence=[cScatter], trendline = "expanding", trendline_color_override = cTrend)
                with col4:
                    if st.checkbox("Hide date points in the scatter plot", value = True, help = "Uncheck to see data points"):
                        fig.update_traces(visible = False, selector = dict(mode = "markers"))
            if trendSelected == "Expanding Maximum":
                fig = px.scatter(yearVSprice, x = "Year of Make", y = "Price of Car in USD($)", color_discrete_sequence=[cScatter], trendline = "expanding", trendline_options=dict(function="max"), trendline_color_override = cTrend)
                with col4:
                    if st.checkbox("Hide date points in the scatter plot", value = True, help = "Uncheck to see data points"):
                        fig.update_traces(visible = False, selector = dict(mode = "markers"))
            st.plotly_chart(fig, use_container_width = True)
        if viewMode == "Compare Mode":
            trendoptions = ["Locally Weighted Scatterplot Smoothing", "Moving Averages", "Expanding mean", "Expanding Maximum"]
            col1, col2, col3 = st.columns(3)
            with col1:
                trendSelected = st.selectbox("Select a trendlines you want to use", (trendoptions), index  = 0, help = "The selected trendline will been used to fit the scatter plot")
            plotData = localCar[(localCar['price'] != 0) & (localCar['price'] < maxPrice) & (localCar['price'] > minPrice)]
            plotData = plotData.rename({'year': "Year of Make", 'price': "Price of Car in USD($)"}, axis = 'columns')
            if trendSelected == "Locally Weighted Scatterplot Smoothing":
                with col2:
                    frac = st.slider("Choose a fraction numer for your LOWESS", value = 0.5, min_value = 0.01, max_value = 0.99, step = 0.01, help = "Lowering this fraction will give a line that more closely follows the data")
                fig = px.scatter(plotData, y = "Price of Car in USD($)", x = "Year of Make", color = "state", symbol = "state", trendline = "lowess", trendline_options = dict(frac = frac))
                with col3:
                    if st.checkbox("Hide date points in the scatter plot", value = True, help = "Uncheck to see data points"):
                        fig.update_traces(visible = False, selector = dict(mode = "markers"))
            if trendSelected == "Moving Averages":
                with col2:
                    window = st.slider("Choose a window numer for your Moving Averages", value = 5, min_value = 1, max_value = 10, step = 1)
                fig = px.scatter(plotData, x = "Year of Make", y = "Price of Car in USD($)", color = "state", symbol = "state",  trendline = "rolling", trendline_options = dict(window = window))
                with col3:
                    if st.checkbox("Hide date points in the scatter plot", value = True, help = "Uncheck to see data points"):
                        fig.update_traces(visible = False, selector = dict(mode = "markers"))
            if trendSelected == "Expanding mean":
                fig = px.scatter(plotData, x = "Year of Make", y = "Price of Car in USD($)", color = "state", symbol = "state", trendline = "expanding")
                with col2:
                    if st.checkbox("Hide date points in the scatter plot", value = True, help = "Uncheck to see data points"):
                        fig.update_traces(visible = False, selector = dict(mode = "markers"))
            if trendSelected == "Expanding Maximum":
                fig = px.scatter(plotData, x = "Year of Make", y = "Price of Car in USD($)", color = "state", symbol = "state", trendline = "expanding", trendline_options = dict(function="max"))
                with col2:
                    if st.checkbox("Hide date points in the scatter plot", value = True, help = "Uncheck to see data points"):
                        fig.update_traces(visible = False, selector = dict(mode = "markers"))
            st.plotly_chart(fig, use_container_width = True)