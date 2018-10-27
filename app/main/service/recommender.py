from surprise import Reader, Dataset
from surprise import KNNBasic, KNNWithMeans, KNNWithZScore, KNNBaseline
from surprise import SVD, SVDpp, NMF
from surprise import BaselineOnly
from surprise import CoClustering, SlopeOne
import pandas as pd
from app.main.database.database import Database
import random


def prepare_data():

    db = Database()
    data_pre = db.findAllRatings()

    user_id = []
    item_id = []
    rating = []

    for row in data_pre:
        user_id.append(row['user_id'])
        item_id.append(row['place_id'])
        rating.append(row['rate'])

    ratings_dict = {'itemID': item_id, 'userID': user_id, 'rating': rating}

    df = pd.DataFrame(ratings_dict)

    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(df[['userID', 'itemID', 'rating']], reader)

    items_length = len(df['itemID'].unique())

    return (data, items_length)


def get_recommendations(user_id):
    data, items_length = prepare_data()

    name_algorithm, algorithm = randomize()

    trainset = data.build_full_trainset()
    algo = algorithm
    algo.fit(trainset)

    ratings = []
    db = Database()
    places = db.findAllPlaces()
    formated_ratings = []

    for i in range(1, (items_length) + 1):
        predict = algo.predict(user_id, i, r_ui=4)
        dictionary = {
            'user': user_id,
            'item': i,
            'est_rating': float(predict.est),
            'impossible': predict.details['was_impossible']
        }
        ratings.append(dictionary)

    formated_ratings = create_dict(ratings, places, name_algorithm)

    return formated_ratings


def create_dict(ratings, places, algorithm):
    formated_ratings = []

    for i in range(len(ratings)):
        if not ratings[i]['impossible']:
            dict_ = {
                'placeId': ratings[i]['item'],
                'userId': ratings[i]['user'],
                'rate_prevision': ratings[i]['est_rating'],
                'name': places[i]['name'],
                'photoUrl': places[i]['photoUrl'],
                'rate_user': 0,
                'algorithm': algorithm
            }
            formated_ratings.append(dict_)

    return formated_ratings


def randomize():
    sim_options_cosine = {'name': 'cosine', 'user_based': False}
    sim_options_msd = {'name': 'msd', 'user_based': False}
    sim_options_pearson = {'name': 'pearson', 'user_based': False}
    sim_options_baseline = {
        'name': 'pearson_baseline',
        'user_based': False,
        'shrinkage': 0
    }

    algorithms = [
        (
            'kNN Basic - Cosine',
            KNNBasic(sim_options=sim_options_cosine, verbose=False)
        ),
        (
            'kNN Basic - MSD',
            KNNBasic(sim_options=sim_options_msd, verbose=False)
        ),
        (
            'kNN Basic - Pearson',
            KNNBasic(sim_options=sim_options_pearson, verbose=False)
        ),
        (
            'kNN Basic - Pearson B',
            KNNBasic(sim_options=sim_options_baseline, verbose=False)
        ),
        (
            'kNN Means - Cosine',
            KNNWithMeans(sim_options=sim_options_cosine, verbose=False)
        ),
        (
            'kNN Means - MSD',
            KNNWithMeans(sim_options=sim_options_msd, verbose=False)
        ),
        (
            'kNN Means - Pearson',
            KNNWithMeans(sim_options=sim_options_pearson, verbose=False)
        ),
        (
            'kNN Means - Pearson B',
            KNNWithMeans(sim_options=sim_options_baseline, verbose=False)
        ),
        (
            'kNN Z - Cosine',
            KNNWithZScore(sim_options=sim_options_cosine, verbose=False)
        ),
        (
            'kNN Z - MSD',
            KNNWithZScore(sim_options=sim_options_msd, verbose=False)
        ),
        (
            'kNN Z - Pearson',
            KNNWithZScore(sim_options=sim_options_pearson, verbose=False)
        ),
        (
            'kNN Z - Pearson B',
            KNNWithZScore(sim_options=sim_options_baseline, verbose=False)
        ),
        (
            'kNN Baseline - Cosine',
            KNNBaseline(sim_options=sim_options_cosine, verbose=False)
        ),
        (
            'kNN Baseline - MSD',
            KNNBaseline(sim_options=sim_options_msd, verbose=False)
        ),
        (
            'kNN Baseline - Pearson',
            KNNBaseline(sim_options=sim_options_pearson, verbose=False)
        ),
        (
            'kNN Baseline - Pearson B',
            KNNBaseline(sim_options=sim_options_baseline, verbose=False)
        ), ('SVD', SVD(verbose=False)), ('SVDpp', SVDpp(verbose=False)),
        ('Baseline Only', BaselineOnly(verbose=False)),
        ('CoClustering', CoClustering(verbose=False)),
        ('SlopeOne', SlopeOne()), ('NMF', NMF(verbose=False))
    ]

    random_ = random.randint(0, len(algorithms)-1)

    return algorithms[random_]


def get_top_n_recommendations(user_id, n):
    data, items_length = prepare_data()

    # Modelo de recomendação
    trainset = data.build_full_trainset()
    algo = SVD()
    algo.fit(trainset)

    ratings_pre = []
    ratings = []
    for i in range(1, (items_length) + 1):
        predict = algo.predict(user_id, i, r_ui=4)
        if not predict.details['was_impossible']:
            dictionary = {
                'user': user_id,
                'item': i,
                'rating': float(predict.est)
            }
            ratings_pre.append(dictionary)

    ratings_pre = sorted(ratings_pre, key=lambda x: x['rating'], reverse=True)

    for i in range(0, n):
        ratings.append(ratings_pre[i])

    places = []
    db = Database()
    for place in ratings:
        places.append(db.findByIdPlaces(place['item']))

    listRecommendations = []
    for i in range(0, n):
        dict_ = {
            'userId': ratings[i]['user'],
            'name': places[i]['name'],
            'photoUrl': places[i]['photoUrl'],
            'rate_prevision': round(ratings[i]['rating'], 2),
            'rate_user': 0
        }

        listRecommendations.append(dict_)

    return listRecommendations
