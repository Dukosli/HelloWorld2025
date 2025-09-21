import tmdbsimple as tmdb
import pandas as pd
import time
import ast
tmdb.API_KEY = '3dd5f096f8f0bfcfd63b8a8f3d5cb7dd'

discover = tmdb.Discover()

iterations = 0
movies_dict = discover.movie(sort_by='popularity.desc', page=1)
movies_df = pd.DataFrame(movies_dict['results'])

while iterations < 3:
    for i in range(50):
        movies_dict = discover.movie(sort_by='popularity.desc', page=(iterations)*(50)+i+2)
        new_movies_df = pd.DataFrame(movies_dict['results'])
        movies_df = pd.concat([movies_df, new_movies_df], ignore_index=True)
    iterations += 1
    time.sleep(1)


movies_df = movies_df.drop_duplicates(subset=['id'], keep='first')
movies_df["genre_ids_str"] = movies_df["genre_ids"].astype(str)
movies_df.to_csv('movies.csv', index=False)
print(movies_df['popularity'].head())



