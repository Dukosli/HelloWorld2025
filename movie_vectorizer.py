import pandas as pd
import tmdbsimple as tmdb
tmdb.API_KEY = '3dd5f096f8f0bfcfd63b8a8f3d5cb7dd'

df = pd.read_csv('movies.csv')
df = df[['id', 'genre_ids']]

print(df.head())

genres = tmdb.Genres()
genre_names_id_df = pd.DataFrame(genres.movie_list()['genres'])
# genre_list = genre_names_id_df['name'].tolist()
print(genre_names_id_df)

# The different genres are: 'Action' (28), 'Adventure' (12), 'Animation' (16), 'Comedy' (35), 'Crime' (80), 'Documentary' (99), 
# 'Drama' (18), 'Family' (10751), 'Fantasy' (14), 'History' (36), 'Horror' (27), 'Music' (10402), 'Mystery' (9648), 
# 'Romance' (10749), 'Science Fiction' (878), 'TV Movie' (10770), 'Thriller' (53), 'War' (10752), 'Western' (37)

print(df.dtypes)

def get_movie_id(movie_name):
    pass

def movie_vectorizer(movie_id):
    # movie_id should be an integer

    single_movie = df[df['id'] == movie_id]

    movie_genres_str = single_movie['genre_ids'].iloc[0] # This gives movie_genres as a string, like "[878, 53]"
    print(movie_genres_str)
    if "," in movie_genres_str:
        movie_genres_str = movie_genres_str[1:len(movie_genres_str)-2]
        movie_genres_str_list = movie_genres_str.split(",")
        movie_genres_int_list = [int(genre) for genre in movie_genres_str_list]
    else: 
        movie_genres_str = movie_genres_str[1:len(movie_genres_str)-2]
        movie_genres_int_list = [int(movie_genres_str)] 
    

    
    # Initialize all qualities
    qualities = {
        "Excitement": 0,
        "Pacing": 0,
        "Emotional Depth": 0,
        "Humor": 0,
        "Mental Stimulation": 0,
        "Darkness": 0,
        "World-Building": 0,
        "Artistry": 0,
        "Relatability": 0,
        "Epicness": 0
    }

    # Mapping: genre_code → quality modifications
    genre_effects = {
        28: {"Excitement": +3, "Pacing": +2, "Emotional Depth": -1, "Humor": 0,
            "Mental Stimulation": -2, "Darkness": 0, "World-Building": +1,
            "Artistry": 0, "Relatability": -1, "Epicness": +2},  # Action

        12: {"Excitement": +2, "Pacing": +1, "Emotional Depth": 0, "Humor": 0,
            "Mental Stimulation": 0, "Darkness": 0, "World-Building": +2,
            "Artistry": 0, "Relatability": +1, "Epicness": +3},  # Adventure

        16: {"Excitement": +1, "Pacing": +1, "Emotional Depth": +1, "Humor": +1,
            "Mental Stimulation": 0, "Darkness": -1, "World-Building": +2,
            "Artistry": +1, "Relatability": +2, "Epicness": +1},  # Animation

        35: {"Excitement": +1, "Pacing": +1, "Emotional Depth": -1, "Humor": +3,
            "Mental Stimulation": -1, "Darkness": -2, "World-Building": 0,
            "Artistry": 0, "Relatability": +2, "Epicness": 0},  # Comedy

        80: {"Excitement": +1, "Pacing": 0, "Emotional Depth": +1, "Humor": -1,
            "Mental Stimulation": +2, "Darkness": +2, "World-Building": 0,
            "Artistry": 0, "Relatability": -1, "Epicness": 0},  # Crime

        99: {"Excitement": 0, "Pacing": -1, "Emotional Depth": +2, "Humor": 0,
            "Mental Stimulation": +3, "Darkness": 0, "World-Building": +1,
            "Artistry": +1, "Relatability": +1, "Epicness": 0},  # Documentary

        18: {"Excitement": 0, "Pacing": -1, "Emotional Depth": +3, "Humor": 0,
            "Mental Stimulation": +2, "Darkness": +1, "World-Building": 0,
            "Artistry": +1, "Relatability": +1, "Epicness": +1},  # Drama

        10751: {"Excitement": 0, "Pacing": +1, "Emotional Depth": +1, "Humor": +1,
                "Mental Stimulation": 0, "Darkness": -2, "World-Building": +1,
                "Artistry": 0, "Relatability": +3, "Epicness": 0},  # Family

        14: {"Excitement": +2, "Pacing": +1, "Emotional Depth": +1, "Humor": 0,
            "Mental Stimulation": 0, "Darkness": 0, "World-Building": +3,
            "Artistry": +1, "Relatability": 0, "Epicness": +3},  # Fantasy

        36: {"Excitement": 0, "Pacing": -1, "Emotional Depth": +2, "Humor": 0,
            "Mental Stimulation": +2, "Darkness": +1, "World-Building": +1,
            "Artistry": +1, "Relatability": +1, "Epicness": +2},  # History

        27: {"Excitement": +2, "Pacing": +1, "Emotional Depth": 0, "Humor": -1,
            "Mental Stimulation": +1, "Darkness": +3, "World-Building": 0,
            "Artistry": 0, "Relatability": -2, "Epicness": 0},  # Horror

        10402: {"Excitement": 0, "Pacing": 0, "Emotional Depth": +1, "Humor": +1,
                "Mental Stimulation": 0, "Darkness": 0, "World-Building": 0,
                "Artistry": +3, "Relatability": +1, "Epicness": +1},  # Music

        9648: {"Excitement": +1, "Pacing": 0, "Emotional Depth": +1, "Humor": 0,
            "Mental Stimulation": +3, "Darkness": +2, "World-Building": 0,
            "Artistry": 0, "Relatability": 0, "Epicness": 0},  # Mystery

        10749: {"Excitement": 0, "Pacing": 0, "Emotional Depth": +3, "Humor": +1,
                "Mental Stimulation": 0, "Darkness": -1, "World-Building": 0,
                "Artistry": +1, "Relatability": +2, "Epicness": +1},  # Romance

        878: {"Excitement": +2, "Pacing": +1, "Emotional Depth": 0, "Humor": 0,
            "Mental Stimulation": +3, "Darkness": +1, "World-Building": +3,
            "Artistry": +1, "Relatability": 0, "Epicness": +3},  # Sci-Fi

        10770: {"Excitement": 0, "Pacing": 0, "Emotional Depth": +1, "Humor": 0,
                "Mental Stimulation": 0, "Darkness": 0, "World-Building": 0,
                "Artistry": 0, "Relatability": +1, "Epicness": 0},  # TV Movie

        53: {"Excitement": +3, "Pacing": +2, "Emotional Depth": 0, "Humor": -1,
            "Mental Stimulation": +2, "Darkness": +3, "World-Building": 0,
            "Artistry": 0, "Relatability": -1, "Epicness": +1},  # Thriller

        10752: {"Excitement": +2, "Pacing": 0, "Emotional Depth": +3, "Humor": 0,
                "Mental Stimulation": +1, "Darkness": +2, "World-Building": +1,
                "Artistry": +1, "Relatability": -1, "Epicness": +3},  # War

        37: {"Excitement": +2, "Pacing": +1, "Emotional Depth": +1, "Humor": 0,
            "Mental Stimulation": +1, "Darkness": +1, "World-Building": +1,
            "Artistry": 0, "Relatability": 0, "Epicness": +2}  # Western
    }

    for genre_code in movie_genres_int_list:
        if genre_code in genre_effects:
            for quality, value in genre_effects[genre_code].items():
                qualities[quality] += value
    

    returned_vector = [qualities["Excitement"], qualities["Pacing"], qualities["Emotional Depth"], qualities["Humor"],
    qualities["Mental Stimulation"], qualities["Darkness"], qualities["World-Building"], qualities["Artistry"], qualities["Relatability"],
    qualities["Epicness"]]
    
    return returned_vector

print(movie_vectorizer(1038392))






