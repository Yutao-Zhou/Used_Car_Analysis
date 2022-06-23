import spacy
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud, STOPWORDS
from PIL import Image

def getKeyPhrase(text):
	description = text[:]
	nlp = spacy.load("en_core_web_lg")
	nounTag = {}
	if len(text.split(" ")) < 200:
		doc = nlp(text)
		for chunk in doc.noun_chunks:
			keyPhase = chunk.text
			splited = keyPhase.split(" ")
			if len(splited) > 1:
				if keyPhase in nounTag:
					nounTag[keyPhase] += 1
				else:
					nounTag[keyPhase] = 1
	if len(text.split(" ")) >= 200:
		text = text.split(" ")
		for i in range(200, len(text), 200):
			doc = nlp(" ".join(text[i - 200: i]))
			for chunk in doc.noun_chunks:
				keyPhase = chunk.text
				keyPhase = keyPhase.strip()
				splited = keyPhase.split(" ")
				if len(splited) > 1:
					if keyPhase in nounTag:
						nounTag[keyPhase] += 1
					else:
						nounTag[keyPhase] = 1
	st.markdown("### AI generated keywords")
	with st.spinner('AI is working hard, please wait!'):
		n = 0
		noun = nounTag.copy()
		noun = noun.keys()
		noun = sorted(noun, key = len, reverse = True)
		cols = st.columns(8)
		while noun:
			for col in cols:
				with col:
					d = noun.pop()
					st.write(d)
					n += 1
					if not noun:
						break
				if not n % 8:
					cols = st.columns(8)
		wordCloud(description)
	
def wordCloud(wcText):
	if type(wcText) == dict:
		stopwords = set(STOPWORDS)
		mask = np.array(Image.open("car.jpeg"))
		wc = WordCloud(
			stopwords = stopwords,
			mask = mask,
			background_color = "white",
			contour_color = "black",
			contour_width = 3,
			max_words = 50,
			repeat = True,
			max_font_size = 100
			)
		wc.generate_from_frequencies(frequencies = wcText)
		plt.imshow(wc)
		plt.axis("off")
		st.pyplot(plt, use_container_width = True)
	if type(wcText) == str:
		stopwords = set(STOPWORDS)
		mask = np.array(Image.open("car.jpeg"))
		wc = WordCloud(
			stopwords = stopwords, 
			mask = mask,
			background_color = "white",
			contour_color = "mint",
			contour_width = 0,
			max_words = 100,
			repeat = True,
			)
		wc.generate(wcText)
		plt.imshow(wc)
		plt.axis("off")
		st.pyplot(plt, use_container_width = True)
	st.markdown("### Original description")
	st.write(wcText)