import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Reletive words",
    page_icon="",
)

st.title("Used Car Analyzer")
selection, display = st.columns([1, 4])
def sidebar():
    st.sidebar.button("Home")
    st.sidebar.button("Link to my personal website")
    st.sidebar.button("Download my CV")
    with selection:
        # model = ["gensim"]
        #
        # text_input = st.sidebar.text_input("Enter a word you want to query", 'good')
        # s_station = st.sidebar.selectbox('Select a modole', model, key='usedmodel',
        #                          help="Which model you want to use to search relevent words?")
        #
        # multi_select = st.sidebar.multiselect('multiselection', model, default=["gensim"])
        # slider_input = st.sidebar.slider('year', 0.01, 1.00, 0.01)
        minPrice = st.sidebar.number_input("Minimum Listing Price", min_value = 0, value = 1000, step = 1000)
        maxPrice = st.sidebar.number_input("Maximum Listing Price", min_value = 0, value = 1000000, step = 1000)
    return minPrice, maxPrice
def readData(path):
    df = pd.read_csv(path)
    print(df.columns)
    df = df[['id',"state",'region','year','odometer','price','manufacturer', 'model']]
    df = df.loc[df['price'] != 0]
    print(df.head(400))
    CAdf = df.loc[df["state"] == "ca"]
    CAdf.drop(columns=["state"])
    return CAdf
    print(CAdf)
def visualization(CAdf, minPrice, maxPrice):
    allRegionInCA = set(CAdf["region"])
    print(allRegionInCA)
    for area in allRegionInCA:
        localCar = CAdf.loc[CAdf["region"] == area]
        print(len(localCar))
        print(len(localCar), localCar)
        year = localCar['year'].tolist()
        price = localCar['price'].tolist()
        i = 0
        while i < len(price):
            if price[i] == 0 or price[i] < minPrice or price[i] > maxPrice:
                year.pop(i)
                price.pop(i)
            else:
                try:
                    year[i] = int(year[i])
                except:
                    year.pop(i)
                    price.pop(i)
                i += 1
        averagePrice = sum(price) // len(price)
        averageYear = sum(year) // len(year)
        st.write(f"The average price of used car in {area} is {averagePrice}$")
        st.write(f"The average year of make of used car in {area} is {averageYear}$")
        yearVSprice = pd.DataFrame(price,year)
        st.dataframe(localCar,1000,500)
        st.line_chart(yearVSprice)

#
with display:
    pass
minPrice, maxPrice = sidebar()
CAdf = readData("C:/Users/13520/Documents/GitHub/Used_Car_Analysis/used_car_california.csv")
visualization(CAdf, minPrice, maxPrice)
