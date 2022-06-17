import streamlit as st
import pandas as pd
import numpy as np
import dask.dataframe as dd
import pydeck as pdk

def state2Coor(stateName):
    if (type(stateName) == list and len(stateName) > 1) or stateName == "All States":
        return 38.155726, -98.030561, 3.5
    else:
        path = "./statelatlong.csv"
        dask = dd.read_csv(path, dtype = {"State":str, "Name": str, "Latitude": float, "Longitude": float})
        df = dask.compute()
        if type(stateName) == list and len(stateName) == 1:
            stateName = stateName[0]
        stateDf = df.loc[df['Name'] == stateName]
        latitude = float(stateDf['Latitude'])
        Longitude = float(stateDf['Longitude'])
        return latitude, Longitude, 5

def listingMap(data, stateName):
    latitude, longitude, zoom = state2Coor(stateName)
    view = pdk.ViewState(latitude = latitude, longitude = longitude, pitch = 50, zoom = zoom)
    column_layer = pdk.Layer('ColumnLayer',
                             data = data,
                             get_position = ['long', 'lat'],
                             get_elevation = 'price',
                             elevation_scale = 1,
                             radius = 1000,
                             get_fill_color = [255, 153, 0, 80],
                             pickable = True,
                             auto_highlight = True)
    column_layer_map = pdk.Deck(layers = column_layer, 
                                initial_view_state = view)
    st.pydeck_chart(column_layer_map)