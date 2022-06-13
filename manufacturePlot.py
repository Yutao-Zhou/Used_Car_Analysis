import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from stateCode2state import name2code, code2name

def manufacture(localCar, area, statename):
	if type(localCar) != dict:
		allManufacture = localCar.manufacturer.unique()
		allManufacture = np.sort(allManufacture)
		l = len(localCar)
		largeManufacture = []
		numberOfCars = []
		others = 0
		for m in allManufacture:
			n = len(localCar[localCar['manufacturer'] == m])
			if n / l < 0.01:
				others += n
			else:
				numberOfCars.append(n)
				largeManufacture.append(m)
		numberOfCars.append(others)
		largeManufacture.append("others")
		d = {"Manufacture": largeManufacture, "Number of Car": numberOfCars}
		market = pd.DataFrame(data = d)
		fig = px.pie(market, values='Number of Car', names = 'Manufacture', title = f'Mareket share of each manufacture in <b>{area}{statename}</b>')
		st.plotly_chart(fig, use_container_width = True)
	if type(localCar) == dict:
		for state in localCar.keys():
			allManufacture = localCar[state].manufacturer.unique()
			allManufacture = np.sort(allManufacture)
			l = len(localCar[state])
			largeManufacture = []
			numberOfCars = []
			others = 0
			for m in allManufacture:
				n = len(localCar[state][localCar[state]['manufacturer'] == m])
				if n / l < 0.01:
					others += n
				else:
					numberOfCars.append(n)
					largeManufacture.append(m)
			numberOfCars.append(others)
			largeManufacture.append("others")
			d = {"Manufacture": largeManufacture, "Number of Car": numberOfCars}
			market = pd.DataFrame(data = d)
			fig = px.pie(market, values='Number of Car', names = 'Manufacture', title = f'Mareket share of each manufacture in <b>{code2name(state)}</b>')
			st.plotly_chart(fig, use_container_width = True)