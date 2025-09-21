import streamlit as st
import pandas as pd



st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

st.markdown("""
<style>

.stButton > button {
  background-color: #0A84FF;
  color: #ffffff;
  border: 1px solid #0A84FF;
  border-radius: 10px;
}

.stButton > button:hover {
  background-color: #006DDB;
  border-color: #006DDB;
}

.stButton > button:disabled {
  background-color: #333333 !important;
  border-color: #333333 !important;
  color: #888888 !important;
}

.movie-overview{
  white-space: normal !important;
  overflow-wrap: anywhere;     /* modern */
  word-break: break-word;      /* fallback */
  line-height: 1.4;
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
        st.write(f"**{m['name']}** --- {m['rating']}/10")

if len(st.session_state["movies"]) >= 2 and genres:
    st.button(f"Recommend Me 5 Movies", on_click=run_recommend, disabled=st.session_state["locked"])

if st.session_state["results"]:
    st.subheader("Recommendations:")

    movies = [
        {
            "title": "Demon Slayer: Infinity Castle",
            "rating": 7.7,
            "poster": "https://image.tmdb.org/t/p/w200/sUsVimPdA1l162FvdBIlmKBlWHx.jpg",
            "overview": "The Demon Slayer Corps are drawn into the Infinity Castle, where Tanjiro, Nezuko, and the Hashira face terrifying Upper Rank demons..."
        },
        {
            "title": "War of the Worlds",
            "rating": 4.3,
            "poster": "https://image.tmdb.org/t/p/w200/yvirUYrva23IudARHn3mMGVxWqM.jpg",
            "overview": "Will Radford is a top analyst for Homeland Security who tracks threats through surveillance, until one day an attack by an unknown entity changes everything..."
        },
        {
            "title": "The Conjuring: Last Rites",
            "rating": 6.6,
            "poster": "https://image.tmdb.org/t/p/w200/29ES27icY5CzTcMhlz1H4SdQRod.jpg",
            "overview": "Paranormal investigators Ed and Lorraine Warren take on one last terrifying case involving mysterious entities..."
        },
        {
            "title": "Inception",
            "rating": 8.8,
            "poster": "https://image.tmdb.org/t/p/w200/qmDpIHrmpJINaRKAfWQfftjCdyi.jpg",
            "overview": "A skilled thief enters people's dreams to steal secrets, but gets one final mission: to plant an idea instead."
        },
        {
            "title": "Interstellar",
            "rating": 8.6,
            "poster": "https://image.tmdb.org/t/p/w200/rAiYTfKGqDCRIIqo664sY9XZIvQ.jpg",
            "overview": "A team of explorers travel through a wormhole in space to ensure humanity's survival."
        }
    ]

    for movie in movies:

        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(movie["poster"], width=140)
        with col2:
            st.markdown(f"**{movie['title']}**")
            st.markdown(f"⭐ Rating: {movie['rating']}/10")
            st.markdown(f'<div class="movie-overview">{movie["overview"]}</div>', unsafe_allow_html=True)
        st.divider()

if st.session_state["locked"]:
    st.button("Restart", on_click=restart)