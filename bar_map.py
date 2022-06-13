import streamlit as st
import pandas as pd
import numpy as np

def listingMap(data):
    import pydeck as pdk
    view = pdk.ViewState(latitude = 39.155726, longitude = -98.030561, pitch = 50, zoom = 3.5)
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