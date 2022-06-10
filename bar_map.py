import streamlit as st
import pandas as pd
import numpy as np

def pydeckMap(data):
    # data
    # in this example, the population was scaled down
    # to change visualization, try changing the elevation_scale and radius arguments
    import pydeck as pdk
    data['price'] = data['price']/1_000
    # view (location, zoom level, etc.)
    view = pdk.ViewState(latitude = 39.155726, longitude = -98.030561, pitch = 50, zoom = 6)

    # layer
    column_layer = pdk.Layer('ColumnLayer',
                             data=data,
                             get_position = ['long', 'lat'],
                             get_elevation = 'price',
                             elevation_scale = 100,
                             radius = 1000,
                             get_fill_color=[255, 165, 0, 80],
                             pickable = True,
                             auto_highlight = True)
    # render map
    # with no map_style, map goes to default
    column_layer_map = pdk.Deck(layers=column_layer, 
                                initial_view_state=view)
    # display and save map (to_html(), show())
    st.pydeck_chart(column_layer_map)