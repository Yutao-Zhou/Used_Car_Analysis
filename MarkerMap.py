import dask.dataframe as dd
import leafmap.foliumap as leafmap
import streamlit as st

def markerCluster(Data):
    m = leafmap.Map(center=[40, -100], zoom=4)
    regions = 'https://raw.githubusercontent.com/giswqs/leafmap/master/examples/data/us_regions.geojson'
    m.add_geojson(regions, layer_name='US Regions')

    m.add_points_from_xy(
        Data,
        x="lat",
        y="long",
        color_column='US Regions',
    )
    m.to_streamlit(height=700)