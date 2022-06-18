import pandas as pd
import plotly.express as px
import streamlit as st

def listingMap(df):
    lmap = px.scatter_mapbox(df, lat="lat", lon="long", hover_name="model", hover_data=["price", "year", "odometer", "manufacturer"],
                            color_discrete_sequence=["fuchsia"], zoom=3, height=300)
    st.plotly_chart(lmap, use_container_width=False, sharing="streamlit")