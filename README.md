# TV Series Data Cleaning & Dashboard

This project explores trends and patterns in a curated dataset of television shows. Starting from raw, scraped data, the dataset was cleaned, updated, and enriched using a second data source. Exploratory analysis was carried out in a Jupyter notebook, and key insights were turned into an interactive dashboard using Streamlit and Plotly.

## Features

### Data Cleaning and Enrichment

- Based on a 2021 Kaggle dataset scraped from **IMDb**.
- Enriched with up-to-date data from **TVMaze API** (2025).
- Normalised and structured for SQL and pandas analysis.

### EDA Highlights

- Ratings comparison between IMDb and TVMaze.
- Genre frequency and co-occurrence.
- Gantt charts detailing the run periods of shows.

### Interactive Dashboard

Built with Streamlit and Plotly, the dashboard features:

- Filters for language, show status and genre.
- KPI summary cards.
- Dynamic charts.

### Key Insights

- **Recent bias:** The majority of the shows in the dataset began airing after 2010, limiting longitundal analysis.
- **Platform differences:** Ratings on TVMaze tend to be lower than IMDb’s, potentially due to timing (2025 vs. 2021) or user demographics.
- **Reach vs reception:** Shows with the highest vote counts are not always the highest rated.


### Links

- [EDA notebook](https://github.com/markus-pettersen/television_cleaning/blob/main/notebooks/06_eda.ipynb)
- [Dashboard](blank)
- [Original dataset](https://www.kaggle.com/datasets/bharatnatrayn/movies-dataset-for-feature-extracion-prediction/data)
- [IMDb](https://www.imdb.com/)
- [TVMaze API](https://www.tvmaze.com/api)

### Future plans

 - Use the co-occurrence matrix to develop a **genre prediction model** from show descriptions.
 - Use up-to-date IMDb database to eliminate bias from when the data was collected.
 - Expand scope to also include movies and episodes present in the original dataset.

 ### Author

**Markus Saint-Pettersen**

[Github](http://github.com/markus-pettersen) [LinkedIn](linkedin.com/in/m-saint-pettersen)
