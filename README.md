# ScoutLab ⚽

A professional football player intelligence dashboard built with Python and Streamlit.
Pulls live squad data from Transfermarkt, clusters players by playing style using KMeans,
and presents everything in a clean scouting UI.

## Features
- Live data from Transfermarkt for 60+ clubs across 9 leagues
- KMeans clustering to group players by playing style
- Player photos, market values, and position badges
- Filter by position and age range
- Interactive charts — scatter, bar, heatmap

## Tech Stack
Python · Pandas · Scikit-learn · Plotly · Seaborn · Streamlit · BeautifulSoup

## Setup
```bash
git clone https://github.com/YOURUSERNAME/scoutlab.git
cd scoutlab
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Usage
1. Select a team from the sidebar
2. Choose position and age filters
3. Click Analyse Squad