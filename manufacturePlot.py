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
		allFiger = []
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
			allFiger.append(fig)
		if len(allFiger) == 1:
			st.plotly_chart(allFiger.pop(), use_container_width = True)
		else:
			n = 0
			col1, col2 = st.columns(2)
			with col1:
				numberPerRow = st.slider("Number of chart per row", min_value = 1, max_value = len(allFiger), value = 2, help = "Adject the formating in the following pie chart section")	
			with col2:
				st.markdown("**Legend will auto hide when choose more than two charts per row**")
				if numberPerRow >= 3:
					legendVisibility = st.checkbox("show legend", value = False, help = "Check to show legend")
				if numberPerRow < 3:
					legendVisibility = st.checkbox("show legend", value = True, help = "Check to show legend")
			cols = st.columns(numberPerRow)
			while allFiger:
				for col in cols:
					with col:
						fig = allFiger.pop()
						if not legendVisibility:
							fig.update_layout(showlegend = False)
						st.plotly_chart(fig, use_container_width = True)
						if not allFiger:
							break
						n += 1
					if not n % numberPerRow:
						cols = st.columns(numberPerRow)