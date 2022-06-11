import streamlit as st
import pandas as pd
import numpy as np

def pydeckMap(data):
    import pydeck as pdk
    view = pdk.ViewState(latitude = 39.155726, longitude = -98.030561, pitch = 50, zoom = 4)
    column_layer = pdk.Layer('ColumnLayer',
                             data = data,
                             get_position = ['long', 'lat'],
                             get_elevation = 'price',
                             elevation_scale = 1,
                             radius = 1000,
                             get_fill_color = [204, 255, 255, 80],
                             pickable = True,
                             auto_highlight = True)
    column_layer_map = pdk.Deck(layers = column_layer, 
                                initial_view_state = view)
    st.pydeck_chart(column_layer_map)