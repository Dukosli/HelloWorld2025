import pandas as pd
import tmdbsimple as tmdb
import ast
tmdb.API_KEY = '3dd5f096f8f0bfcfd63b8a8f3d5cb7dd'

df = pd.read_csv('movies.csv')
df = df[['id', 'genre_ids', 'title']]

# print(df.head())

genres = tmdb.Genres()
genre_names_id_df = pd.DataFrame(genres.movie_list()['genres'])
# genre_list = genre_names_id_df['name'].tolist()
# print(genre_names_id_df)

# The different genres are: 'Action' (28), 'Adventure' (12), 'Animation' (16), 'Comedy' (35), 'Crime' (80), 'Documentary' (99), 
# 'Drama' (18), 'Family' (10751), 'Fantasy' (14), 'History' (36), 'Horror' (27), 'Music' (10402), 'Mystery' (9648), 
# 'Romance' (10749), 'Science Fiction' (878), 'TV Movie' (10770), 'Thriller' (53), 'War' (10752), 'Western' (37)

# print(df.dtypes)

def get_movie_id(movie_name):
    df = pd.read_csv('movies.csv')
    single_movie = df[df['title'] == movie_name]
    movie_id = single_movie['id'].iloc[0]
    movie_id = int(movie_id)
    return movie_id

def movie_vectorizer(movie_id):
    # movie_id should be an integer
    df = pd.read_csv('movies.csv')
    df = df[['id', 'genre_ids', 'title', 'vote_average', 'genre_ids_str']]

    single_movie = df[df['id'] == movie_id]
    movie_genres_str = single_movie['genre_ids'].iloc[0] # This gives movie_genres as a string, like "[878, 53]"

    # if "," in movie_genres_str:
    #     movie_genres_str = movie_genres_str[1:len(movie_genres_str)-2]
    #     movie_genres_str_list = movie_genres_str.split(",")
    #     movie_genres_int_list = [int(genre) for genre in movie_genres_str_list]
    # else: 
    #     movie_genres_str = movie_genres_str.replace("[", "")
    #     movie_genres_str = movie_genres_str.replace("]", "")
    #     movie_genres_int_list = [int(movie_genres_str)] 
    

    
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

    # for genre_code in movie_genres_int_list:
    #     if genre_code in genre_effects:
    #         for quality, value in genre_effects[genre_code].items():
    #             qualities[quality] += value

    genre_codes_str = ["28", "12", "16", "35", "80", "99", "18", "10751", "14", "36", "27", "10402", "9648", "10749", 
    "878", "10770", "53", "10752", "37"]
    
    for genre_code_str in genre_codes_str:
        if genre_code_str in str(single_movie['genre_ids_str'].iloc[0]):
            for quality, value in genre_effects[int(genre_code_str)].items():
                qualities[quality] += value

    returned_vector = [qualities["Excitement"], qualities["Pacing"], qualities["Emotional Depth"], qualities["Humor"],
    qualities["Mental Stimulation"], qualities["Darkness"], qualities["World-Building"], qualities["Artistry"], qualities["Relatability"],
    qualities["Epicness"], ]
    returned_vector.append(float(single_movie['vote_average'].iloc[0]))
    
    return returned_vector

# print(movie_vectorizer(get_movie_id("The Conjuring: Last Rites")))

# Movie dictionaries to test the get_ideal_movie_vector function
movie_1 = {"name": "Demon Slayer: Kimetsu no Yaiba Infinity Castle", "rating": 8}
movie_2 = {"name": "War of the Worlds", "rating": 10}
movie_3 = {"name": "The Conjuring: Last Rites", "rating": 2}
movie_4 = {"name": "Weapons", "rating": 5}
movie_5 = {"name": "Nobody 2", "rating": 4}

def get_ideal_movie_vector(movies_dict_list):
    movie_names = []
    movie_ratings = []
    movie_vectors = []
    movie_vectors_adj = []
    

    for movie_dict in movies_dict_list:
        movie_names.append(movie_dict["name"])
        movie_ratings.append(movie_dict["rating"])
    
    for movie_name in movie_names:
        movie_vectors.append(movie_vectorizer(get_movie_id(movie_name)))

    movie_ratings_adj = [(movie_rating/10 -0.5) for movie_rating in movie_ratings]
    movie_rating_adj_sum = 0
    for movie_rating_adj in movie_ratings_adj:
        movie_rating_adj_sum += movie_rating_adj

    if movie_rating_adj_sum == 0:
        return [0,0,0,0,0,0,0,0,0,0,10]

    # for movie_rating_adj in movie_ratings_adj:
    #     for quality in movie_vector:
    #         movie-vectors_adj.append(movie_rating * quality)

    # for movie_rating_adj in movie_ratings_adj:
    #     movie_vectors_adj.append([(movie_rating_adj * quality) for quality in movie_vectors])

    # for movie_vector in movie_vectors:
    #     movie_vectors_adj.append([])

    for movie_rating_adj, movie_vector in zip(movie_ratings_adj, movie_vectors):
        movie_vectors_adj.append([movie_rating_adj * quality for quality in movie_vector])

    movie_vector_adj_sums = []
    for i in range(10):
        sum = 0
        for movie_vector_adj in movie_vectors_adj:
            sum += movie_vector_adj[i]
        movie_vector_adj_sums.append(sum)
    
    ideal_movie_vector = []

    for movie_vector_adj_sum in movie_vector_adj_sums:
        ideal_movie_vector.append((movie_vector_adj_sum)/ movie_rating_adj_sum)
    ideal_movie_vector.append(10)

    return ideal_movie_vector

def get_movieid_vector_dict(genres_asked): #genres_asked is a list of strings
    df = pd.read_csv('movies.csv')
    df = df[['id', 'genre_ids', 'title', 'genre_ids_str', 'movie_vector']]

    keys = ['Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'History', 'Horror', 
    'Music', 'Mystery', 'Romance', 'Science Fiction', 'TV Movie', 'Thriller', 'War', 'Western']
    values = [28, 12, 16, 35, 80, 99, 18, 10751, 14, 36, 27, 10402, 9648, 10749, 878, 10770, 53, 10752, 37]
    genre_ids_dict = dict(zip(keys, values))

    genres_asked_id = []
    for genre in genres_asked:
        genres_asked_id.append(str(genre_ids_dict[genre]))

    for genre_id in genres_asked_id:
        filtered_df = df[df["genre_ids_str"].str.contains(str(genre_id), na=False)]
    
    id_keys = filtered_df['id'].tolist()
    # movie_vector_values = ast.literal_eval(filtered_df['movie_vector'])
    movie_vector_strs = filtered_df['movie_vector'].tolist()
    movie_vector_values = []
    for movie_vector_str in movie_vector_strs:
        movie_vector_values.append(ast.literal_eval(movie_vector_str))

    movieid_vector_dict = dict(zip(id_keys, movie_vector_values))
    return movieid_vector_dict



list_of_test_movies = [movie_1, movie_2, movie_3, movie_4, movie_5]

# print(get_ideal_movie_vector(list_of_test_movies))

# list_of_genres = ['Action']
# print(get_movieid_vector_dict(list_of_genres))

df1 = pd.read_csv('movies.csv')
df1["movie_vector"] = df["id"].apply(lambda x: movie_vectorizer(x))
df1.to_csv('movies.csv', index=False)








