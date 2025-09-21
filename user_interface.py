import streamlit as st
import pandas as pd



st.markdown("""
<style>
/* default state */
.stButton > button {
  background-color: #E50914;   /* your color */
  color: #ffffff;
  border: 1px solid #E50914;
  border-radius: 10px;
}
/* hover */
.stButton > button:hover {
  background-color: #bf0811;
  border-color: #bf0811;
}
/* disabled state */
.stButton > button:disabled {
  background-color: #333333 !important;
  border-color: #333333 !important;
  color: #888888 !important;
}
</style>
""", unsafe_allow_html=True)

df = pd.read_csv("movies.csv")
movie_list = df["title"].tolist()

st.session_state.setdefault("movies", [])
st.session_state.setdefault("genre", [])
st.session_state.setdefault("movie_name", "")
st.session_state.setdefault("movie_rating", 1)
st.session_state.setdefault("locked", False)
st.session_state.setdefault("results", None)



def add_movie():
    name = st.session_state["movie_name"]
    rating = st.session_state["movie_rating"]

    if not name.strip(): return

    name_norm = str(name).strip().lower()
    if any(m["name"].strip().lower() == name_norm for m in st.session_state["movies"]):
        st.toast("Already added that movie")
        return
    
    st.session_state["movies"].append({"name": name, "rating": rating})
    st.session_state["movie_name"] = ""

def remove_movie():
    st.session_state["movies"].clear()
    st.session_state["movie_name"] = ""
    st.session_state["movie_rating"] = 1

def run_recommend():
    st.session_state["locked"] = True
    st.session_state["results"] = {"Placeholder A": 1, "Placeholder B": 2, "Placeholder C": 3, "Placeholder D": 4, "Placeholder E": 5}

def restart():
    st.session_state["locked"] = False
    st.session_state["movies"].clear()
    st.session_state["genre"] = []
    st.session_state["movie_name"] = ""
    st.session_state["movie_rating"] = 1
    st.session_state["results"] = None



st.title("Movie Recommender")

st.write(
    "#### Input the genres of movies you want to watch, "
    "at least 2 movies you have watched from those genres, and your rating for each movie.\n"
    "#### Once you have done this, we will recommend 5 movies that you might enjoy watching."
)

genres = st.multiselect("Enter a genre:", [
    'Action', 'Adventure', 'Animation', 'Comedy', 
    'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 
    'History', 'Horror', 'Music', 'Mystery', 'Romance', 
    'Science Fiction', 'TV Movie', 'Thriller', 'War', 'Western'
    ], key="genre", disabled=st.session_state["locked"])
# movie_name = st.selectbox("Enter a movie name:", movie_list, key="movie_name", disabled=st.session_state["locked"])
movie_name = st.selectbox("Enter a movie name:", movie_list, key="movie_name", disabled=st.session_state["locked"])
movie_rating = st.slider("Rate the movie:", 1, 10, 1, key="movie_rating", disabled=st.session_state["locked"])

col1, col2, _ = st.columns([1.5, 1.5, 7])
with col1:
    st.button("Add Movie", use_container_width=True, on_click=add_movie, disabled=st.session_state["locked"])
with col2:
    st.button("Remove All Movies", use_container_width=True, on_click=remove_movie, disabled=st.session_state["locked"] or not st.session_state["movies"])

if st.session_state["movies"]:
    st.subheader("Movies:")
    for m in st.session_state["movies"]:
        st.write(f"{m['name']} - {m['rating']}/10")

if len(st.session_state["movies"]) >= 2 and genres:
    st.button(f"Recommend Me 5 Movies", on_click=run_recommend, disabled=st.session_state["locked"])

if st.session_state["results"]:
    st.subheader("Recommendations:")

    df = pd.DataFrame(
        list(st.session_state["results"].items()),
        columns=["Movie", "Score"]
    )

    st.dataframe(df, use_container_width=True)

if st.session_state["locked"]:
    st.button("Restart", on_click=restart)