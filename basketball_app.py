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
player_stats = load_data(selected_year)

# Sidebar - Team selection
sorted_unique_team = sorted(player_stats.Tm.unique())
selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

# Sidebar - Position selection
unique_pos = ['C','PF','SF','PG','SG']
selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

# Filtering data
df_selected_team = player_stats[(player_stats.Tm.isin(selected_team)) & (player_stats.Pos.isin(selected_pos))]
#### Error appears when .astype(str) below is not used. See link below for more details.
#### https://stackoverflow.com/questions/69578431/how-to-fix-streamlitapiexception-expected-bytes-got-a-int-object-conver
df_selected_team = df_selected_team.astype(str)

st.header('Display Player Stats of Selected Team(s)')
st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
st.dataframe(df_selected_team)

# Download NBA player stats data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)

