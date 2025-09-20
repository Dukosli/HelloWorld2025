import os
from pathlib import Path
import pandas as pd
import streamlit as st

# app config
st.set_page_config(page_title="🎬 Movie Recs", layout="wide")
DATA_PATH_DEFAULT = Path("data/recs.csv")     # teammates overwrite this
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w342"  # used if you only have poster_path like "/abc.jpg"

REQUIRED_COLS = {
    "movie_id", "title", "year", "score", "wr",
    "why_tags", "poster_url", "genres"
}

st.title("Movie Recommender")
st.write("# Input")
