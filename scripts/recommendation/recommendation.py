from scipy.sparse import csr_matrix
import pandas as pd
import joblib
import random

movies_path = "/home/oanalavinia/Documents/Master/WADe/Disertatie/HandGestureAnalyser/scripts/recommendation/movies.csv"
ratings_path = "/home/oanalavinia/Documents/Master/WADe/Disertatie/HandGestureAnalyser/scripts/recommendation/ratings.csv"
model_path = "/home/oanalavinia/Documents/Master/WADe/Disertatie/HandGestureAnalyser/scripts/recommendation/movies_model.pkl"

# Prepare data.
movies = pd.read_csv(movies_path)
ratings = pd.read_csv(ratings_path)
dataset = ratings.pivot(index='movieId', columns='userId', values='rating')
dataset.fillna(0, inplace=True)

no_user_voted = ratings.groupby('movieId')['rating'].agg('count')
no_movies_voted = ratings.groupby('userId')['rating'].agg('count')
dataset = dataset.loc[no_user_voted[no_user_voted > 10].index, :]
dataset = dataset.loc[:, no_movies_voted[no_movies_voted > 50].index]

csr_data = csr_matrix(dataset.values)
dataset.reset_index(inplace=True)

# Pretrained model.
movies_model = joblib.load(model_path)


def get_recommendation_ids(movie_name):
    n_movies_to_recommend = 3
    movie_list = movies[movies['title'].str.contains(movie_name)]
    movie_idx = movie_list.iloc[0]['movieId']
    movie_idx = dataset[dataset['movieId'] == movie_idx].index[0]
    neigh_dist, neigh_ind = movies_model.kneighbors(csr_data[movie_idx], n_neighbors=n_movies_to_recommend + 1)
    rec_movies = sorted(list(zip(neigh_ind.squeeze().tolist(), neigh_dist.squeeze().tolist())), key=lambda x: x[1])[
                 :0:-1]

    return rec_movies


def get_movie_name_by_id(database_movie_id):
    movie_id = dataset.iloc[database_movie_id]['movieId']
    movie_line = movies[movies['movieId'] == movie_id]
    return movie_line['title'].values[0]


def get_recommendation_titles(rec_movies):
    movies = []
    for movie in rec_movies:
        movie_title = get_movie_name_by_id(movie[0])
        movies.append(movie_title)

    return movies


def get_recommendation(movie_name):
    ids = get_recommendation_ids(movie_name)
    return get_recommendation_titles(ids)


def get_random_movies():
    random_movies = []
    max_length = movies.shape[0]
    while len(random_movies) != 5:
        nr = random.randint(0, max_length)
        if nr not in random_movies:
            random_movies.append(get_movie_name_by_id(nr))

    return random_movies


# print(get_recommendation('Iron Man'))
#
# print(get_random_movies())
