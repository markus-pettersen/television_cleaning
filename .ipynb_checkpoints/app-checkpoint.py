import streamlit as st
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("sqlite:///data/final/tv_database.db")

shows_query = """
    SELECT *
    FROM shows
    LEFT JOIN languages
    ON shows.language_id = languages.id
"""

df = pd.read_sql_query(shows_query, engine, dtype={"start_year":"Int64", "end_year": "Int64", "language_id": "Int64"})
hist_select = st.radio("Pick distribution", ["start_year", "end_year"])

fig = px.histogram(
	df,
	x=hist_select,
	nbins=20,
	title="Distribution of TV show by start year",
	labels = {"start_year": "Year"}
	)

st.title("Television Show Dashboard")
st.write("Hello, this is my dashboard for TV shows")

st.plotly_chart(fig)