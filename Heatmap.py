import dask.dataframe as dd
import leafmap.foliumap as leafmap
import streamlit as st

def state2Coor(stateName):
    if (type(stateName) == list and len(stateName) > 1) or stateName == "All States":
        return 39.155726, -98.030561, 3.5
    else:
        path = "C:/Users/13520/Documents/GitHub/Used_Car_Analysis/statelatlong.csv"
        dask = dd.read_csv(path, dtype = {"State":str, "Name": str, "Latitude": float, "Longitude": float})
        df = dask.compute()
        if type(stateName) == list and len(stateName) == 1:
            stateName = stateName[0]
        stateDf = df.loc[df['Name'] == stateName]
        latitude = float(stateDf['Latitude'])
        Longitude = float(stateDf['Longitude'])
        return latitude, Longitude, 5

def heatmap(data, stateName):
    latitude, longitude, zoom = state2Coor(stateName)
    m = leafmap.Map(center = [latitude, longitude], zoom = zoom, tiles = "stamentoner")
    m.add_heatmap(
        data,
        latitude = "lat",
        longitude = "long",
        value = "price",
        name = "Listing cars heatmap",
        radius = 20,
    )
    m.to_streamlit()