import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

px.defaults.template = "plotly_dark"
# import sql database for access

engine = create_engine("sqlite:///data/final/tv_database.db")

# query all columns needed for dashboard
shows_query = """
    SELECT shows.id, title, start_year, end_year, status, run_time, rating_tvmaze, rating_imdb, votes, language
    FROM shows
    LEFT JOIN languages
    ON shows.language_id = languages.id
"""

df = pd.read_sql_query(shows_query, engine, dtype={"start_year":"Int64", "end_year": "Int64"})

# Fill unknown values for categorical columns:
df["language"] = df["language"].fillna("Unknown")

df["rating_diff"] = abs(df["rating_imdb"] - df["rating_tvmaze"])

# genres in separate df
genre_query = """
	SELECT shows.id, genre
	FROM shows
	LEFT JOIN shows_genres
	ON shows.id = shows_genres.show_id
	LEFT JOIN genres
	ON shows_genres.genre_id = genres.id 
"""

genre_df = pd.read_sql_query(genre_query, engine)
genre_df["genre"] = genre_df["genre"].fillna("Unknown")

# sidebar
st.sidebar.write("Navigation")
page = st.sidebar.radio("Choose section", ["Overview", "Ratings", "Popular Show Trends", "Genre Co-occurrence"])
st.sidebar.write("Categorical filters")

# Filter logic
# genre
all_genres = sorted(genre_df["genre"].unique())
genre_options = ["All"] + all_genres
selected_genres = st.sidebar.multiselect("Genres:", genre_options, default=["All"])

if "All" in selected_genres:
	filtered_genres = all_genres
else:
	filtered_genres = selected_genres

# Language
all_languages = sorted(df["language"].unique())
language_options = ["All"] + all_languages
selected_languages = st.sidebar.multiselect("Languages", language_options, default=["All"])

if "All" in selected_languages:
	filtered_languages = all_languages
else:
	filtered_languages = selected_languages

# Status
all_status = sorted(df["status"].unique())
status_options = ["All"] + all_status
selected_status = st.sidebar.multiselect("Show status", status_options, default=["All"])

if "All" in selected_status:
	filtered_status = all_status
else:
	filtered_status = selected_status

df_language = df[df["language"].isin(filtered_languages)]
df_status = df[df["status"].isin(filtered_status)]
df_genres = genre_df[genre_df["genre"].isin(filtered_genres)]

filtered_df = df[df["language"].isin(filtered_languages) &
				df["status"].isin(filtered_status) &
				df["id"].isin(df_genres["id"])
				]

# Dashboard title
st.title("Television Show Dashboard")

# Overview section
if page == "Overview":

	st.header("Overview")
	st.markdown("This dashboard is based on a cleaned and enriched dataset of TV shows, originally scraped from IMDb and updated with data from TVMaze.")
	st.markdown("[See full project on Github](https://github.com/markus-pettersen/television_cleaning)")
	st.markdown("Use the filters in the sidebar to explore how language and genre influence the charts.")

	col1, col2 = st.columns(2)
	try:
		episode_length = round(filtered_df["run_time"].mean())
	except:
		episode_length = filtered_df["run_time"].mean()
	with col1:
		st.metric(value=len(filtered_df), label="Total shows")
	with col2:
		st.metric(value=f"{episode_length} minutes", label="Average episode length")

	# graphic 1 - histogram
	histogram = px.histogram(filtered_df, x="start_year", nbins=30, title="Distribution of TV shows by start year", labels={"start_year": "year"})
	st.plotly_chart(histogram)

	# graphic 2 - bar chart
	filtered_genres = df_genres[df_genres["id"].isin(filtered_df["id"])]
	genre_counts = filtered_genres["genre"].value_counts().reset_index()
	
	genre_counts.columns = ["genre", "count"]
	bar_chart = px.bar(
		genre_counts,
		x="genre",
		y="count",
		title="Number of titles by genre",
		hover_name="genre",
		hover_data = {"genre": False, "count": True})

	st.plotly_chart(bar_chart, use_container_width=True)

	st.write("Underyling data:")
	st.dataframe(filtered_df[["title", "start_year", "end_year", "run_time", "language", "status"]], height=250)

# Ratings section
elif page == "Ratings":
	st.header("Ratings")
	st.markdown("For an accurate comparison, only shows rated by both platforms are included.")

	equal_rating_df = filtered_df[filtered_df["rating_imdb"].notna() & filtered_df["rating_tvmaze"].notna()]
	col1, col2, col3 = st.columns(3)
	with col1:
		st.metric(value=round(equal_rating_df["rating_imdb"].mean(), 1), label="Average Rating IMDb")
	with col2:
		st.metric(value=round(equal_rating_df["rating_tvmaze"].mean(), 1), label="Average Rating TVMaze")
	with col3:
		st.metric(value=equal_rating_df["rating_imdb"].notna().sum(), label="Rated titles")
	
	melted_rating_df = equal_rating_df.melt(value_vars=["rating_imdb", "rating_tvmaze"],
											var_name="Source",
											value_name="Rating",)

	box_plot = px.box(melted_rating_df, x="Source", y="Rating", color="Source", title="Boxplots of rating: IMDb and TVMaze")
	st.plotly_chart(box_plot, use_container_width=True)
	st.write("Underlying data:")
	st.dataframe(equal_rating_df[["title", "rating_imdb", "rating_tvmaze", "rating_diff"]], height=250)

# Popular shows section
elif page == "Popular Show Trends":
	st.header("Popular Show Trends")
	st.markdown("Select a genre and number of shows to see their runtimes over the years.")
	st.markdown("For simplicity, this visualisation does not use the sidebar filters.")
	genre_select = st.selectbox("Choose genre:", all_genres)
	number_select = st.slider("Top n entries:", min_value=1, max_value=10, value=5)

	gantt_genres = genre_df[genre_df["genre"] == genre_select]
	
	gantt_df = df[df["id"].isin(gantt_genres["id"])]
	gantt_df = gantt_df.sort_values(by="votes", ascending=False).reset_index(drop=True)
	gantt_df = gantt_df.iloc[0:number_select]
	gantt_df["end_year"] = gantt_df["end_year"].fillna(datetime.now().year)

	gantt_df["start_year"] = pd.to_datetime(gantt_df["start_year"], format="%Y")
	gantt_df["end_year"] = pd.to_datetime(gantt_df["end_year"], format="%Y")


	timeline = px.timeline(gantt_df.sort_values(by="start_year"), x_start="start_year", x_end="end_year", y="title", title="Top TV shows durations", hover_name="title",
		hover_data={"start_year": True, "end_year": False, "title": True, "status": True, "language": True})
	timeline.update_traces(hovertemplate="<b>Show:</b> %{y}<br><b>Status:</b> %{customdata[0]}<br><b>Language:</b> %{customdata[1]}<extra></extra>")
	st.plotly_chart(timeline, use_container_width=True)

# Genre co-occurrence section
elif page == "Genre Co-occurrence":
	st.header("Genre Co-occurrence")
	st.markdown("Select at least two genres to see how often they appear in the same show.")
	st.markdown("For simplicity, this visualisation does not use the sidebar filters.")

	heatmap_selector = st.multiselect("Genres", all_genres, default=["Action", "Adventure", "Animation"])
	heatmap_genres = genre_df[genre_df["genre"].isin(heatmap_selector)]

	if not heatmap_selector:
		st.warning("Please select at least one genre")
		st.stop()
    
	genre_matrix = pd.crosstab(heatmap_genres["id"], heatmap_genres["genre"])
	co_occurr = genre_matrix.T @ genre_matrix
	normalised = co_occurr.div(np.diag(co_occurr), axis=0)
	normalised = normalised.round(2)

	heat_map = px.imshow(normalised, text_auto=True, title="Genre co-occurrence matrix")
	heat_map.update_coloraxes(showscale=False)
	heat_map.update_traces(hovertemplate="%{z:.1%} of  <i>%{y}</i> shows have the tag <i>%{x}</i>")

	st.plotly_chart(heat_map, use_container_width=True)
