import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from stateCode2state import name2code, code2name
import numpy as np

@st.cache
def convert_df(df):
     return df.to_csv().encode('utf-8')

def calcuateAveragePrice(localCar):
    n = len(localCar)
    totalYear = localCar['year'].sum(axis = 0)
    totalPrice = localCar['price'].sum(axis = 0)
    averagePrice = totalPrice // n
    averageYear = totalYear // n
    return n, averagePrice, averageYear

def selectedDataVisualization(area, state_df, localCar, stateCode):
    if type(stateCode) == str:
        n, averagePrice, averageYear = calcuateAveragePrice(localCar)
        state_name = code2name(stateCode)
        st.markdown(f"There are **{n}** cars in **{area}{state_name}** that match the price in this dataset. The average model year is **{averageYear}**. The average price is **{averagePrice}** USD($).")
        with st.expander("Click to view data"):
            st.dataframe(localCar,1000,500)
            st.download_button("Click here to download data", convert_df(localCar), file_name = f"{area}{state_name}.csv", help = "Download the data as shown above. Named by area(if selected) and state. In CSV format")
    if type(stateCode) == list:
        with st.expander("Click to view data"):
            sName = []
            sN = []
            sAverageYear = []
            sAveragePrice = []
            for c in stateCode:
                oneState = state_df[state_df['state'] == c]
                localCar[c] = oneState
                n, averagePrice, averageYear = calcuateAveragePrice(oneState)
                state_name = code2name(c)
                sName.append(state_name)
                sN.append(n)
                sAverageYear.append(averageYear)
                sAveragePrice.append(averagePrice)
                st.markdown(f"There are **{n}** cars in **{area}{state_name}** that match the price in this dataset. The average model year is **{averageYear}**. The average price is **{averagePrice}** USD($).")
                st.dataframe(oneState,1000,500)
                st.download_button("Click here to download data", convert_df(oneState), file_name = f"{area}{state_name}.csv", help = "Download the data as shown above. Named by state. In CSV format")
            dataMatrix = np.array([sN, sAverageYear, sAveragePrice])
            dataMatrix = np.transpose(dataMatrix)
        barPlot(sName, dataMatrix)

def barPlot(sName, dataMatrix):
    parameters = ['Number of Cars', 'Average Model Year', 'Average Car Price in dollars($)']
    fig = go.Figure()
    for idn, n in enumerate(dataMatrix):
        fig.add_trace(go.Bar(
            x = parameters,
            y = n,
            name = sName[idn],
        ))
    fig.update_layout(barmode = 'group')
    fig.update_xaxes(
        tickfont = {"size": 20},)
    fig.update_yaxes(
        tickfont = {"size": 20},)
    fig.show()
    st.plotly_chart(fig, use_container_width = True)