import pandas as pd
import plotly.express as px
import streamlit as st

def listingMap(df, latitude, longitude):
    basemap = st.selectbox("Choose a base map", ['open-street-map', 'white-bg', 'carto-positron', 'carto-darkmatter', 'stamen- terrain', 'stamen-toner', 'stamen-watercolor'], help = "Choose to change basemap")
    cScatter = st.color_picker("Pick a color for the scatter", value = "#48D1EA")
    with st.spinner("Plotting Listings cars"):
        fig = px.scatter_mapbox(df, lat = "lat", lon = "long", hover_name = "model", hover_data = ["price", "year", "manufacturer", "odometer", 'condition', 'cylinders', 'fuel', 'title_status', 'transmission', 'VIN', 'drive', 'size', 'type', 'paint_color', "region", "state", 'posting_date'],
                            center = {'lat': latitude, 'lon': longitude}, opacity = 0.8, color_discrete_sequence = [cScatter], zoom = 5, height = 800)
        fig.update_layout(mapbox_style = basemap)
        fig.show()
        st.plotly_chart(fig, use_container_width = True)
        st.write("* Note: There might be data points that are on top of each other because there are listing from dealership.")