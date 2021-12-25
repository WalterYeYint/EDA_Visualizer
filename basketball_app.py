# Execution cmd - streamlit run basketball_app.py

import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title("NBA Player Stats Explorer")

st.markdown("""
Simple webscraping of NBA player stats data
* **Python libraries:** base64, pandas, streamlit
* **Data source:** [Basketball-reference.com](https://www.basketball-reference.com/).
""")

st.sidebar.header("User Input Features")
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950,2020))))

# Web scraping of NBA player stats
@st.cache		# python decorator
def load_data(year):
	url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
	html = pd.read_html(url, header=0)
	df = html[0]
	raw = df.drop(df[df.Age == 'Age'].index)
	raw = raw.fillna(0)
	player_stats = raw.drop(['Rk'], axis=1)
	return player_stats


