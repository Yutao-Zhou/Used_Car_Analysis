import streamlit as st
import pandas as pd
import numpy as np
"""
st.set_page_config(
    page_title="Reletive words",
    page_icon="",
)

st.title("Reletive words finder")
selection, display = st.columns([1, 4])
"""
def sidebar():
    st.sidebar.button("")
def readData(path):
    data = pd.read_csv(path)
    print(data["id"])
    
"""
with selection:
    model = ["gensim"]

    text_input = st.text_input("Enter a word you want to query", 'good')
    s_station = st.selectbox('Select a modole', model, key = 'usedmodel', help = "Which model you want to use to search relevent words?")

    multi_select = st.multiselect('multiselection',model, default=["gensim"])
    slider_input = st.slider('Lowest relevent score', 0.01, 1.00, 0.01)
    n = st.number_input("Number words")

with display:
    st.write("Hello world")
#sidebar()
"""
readData("/home/yutao/Downloads/vehicles.csv")
