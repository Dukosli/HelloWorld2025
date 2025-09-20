import pandas as pd
import tmdbsimple as tmdb
tmdb.API_KEY = '3dd5f096f8f0bfcfd63b8a8f3d5cb7dd'

df = pd.read_csv('movies.csv')
df = df[['id', 'genre_ids']]

print(df.head())

genres = tmdb.Genres()
genre_names_id_df = pd.DataFrame(genres.movie_list()['genres'])
