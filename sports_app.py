# Execution cmd - streamlit run basketball_app.py

import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from PIL import Image
from io import BytesIO
import json

@st.cache		# python decorator
def load_data(year):
	url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
	html = pd.read_html(url, header=0)
	df = html[0]
	raw = df.drop(df[df.Age == 'Age'].index)
	raw = raw.fillna(0)
	player_stats = raw.drop(['Rk'], axis=1)
	return player_stats

# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
	csv = df.to_csv(index=False)
	b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
	href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
	return href

# Convert matplotlib figure to PIL image
def fig2img(fig):
	buf = BytesIO()
	fig.savefig(buf)
	buf.seek(0)
	img = Image.open(buf)
	return img

def heatmap_download(img, filename, text):
	buffered = BytesIO()
	img.save(buffered, format="PNG")
	img_str = base64.b64encode(buffered.getvalue()).decode()
	href =  f'<a href="data:file/txt;base64,{img_str}" download="{filename}">{text}</a>'
	return href

st.sidebar.header("User Input Features")

# Sidebar - Sport selection
with open('sport_url_data.json') as json_file:
	json_data = json.load(json_file)
sport_list = list(json_data.keys())
selected_sport = st.sidebar.selectbox('Sport', sport_list)

sport_site_name = json_data[selected_sport]['sport_site_name']
sport_url = json_data[selected_sport]['sport_url']
sport_root_url = json_data[selected_sport]['sport_root_url']

# Sidebar - Year selection
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950,2020))))

# Web scraping of NBA player stats
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


st.title("NBA Player Stats Explorer")

st.markdown(f"""
Simple webscraping of NBA player stats data
* **Python libraries:** base64, pandas, streamlit
* **Data source:** [{sport_site_name}]({sport_root_url}).
""")

st.header('Display Player Stats of Selected Team(s)')
st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
st.dataframe(df_selected_team)

# Link to download NBA player stats data
st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)

# Display Heatmap
if st.button('Intercorrelation Heatmap'):
	st.header('Intercorrelation Matrix Heatmap')
	#### Adding 'output.csv' as shown below auto-saves the csv file locally into project file
	df_selected_team.to_csv('output.csv', index=False)
	df = pd.read_csv('output.csv')

	corr = df.corr()
	mask = np.zeros_like(corr)
	mask[np.triu_indices_from(mask)] = True
	with sns.axes_style("white"):
		f, ax = plt.subplots(figsize=(7, 5))
		ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
		st.pyplot(f)

	# Saving heatmap locally into project file
	heatmap_name = 'heatmap.png'
	plt.savefig(heatmap_name)

	# Link to download NBA player stats heatmap.png
	fig = plt.gcf()		# grabs current figure
	img = fig2img(fig)
	st.markdown(heatmap_download(img, heatmap_name,'Download '+heatmap_name), unsafe_allow_html=True)



