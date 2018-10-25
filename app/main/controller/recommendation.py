from flask_restplus import Resource, reqparse
from ..service.recommender import get_recommendations
from ..service.recommender import get_top_n_recommendations
from app.main.database.database import Database
import json
import ast

parser = reqparse.RequestParser()
parser.add_argument('ratings', action='append')


class Recommentation(Resource):
    def get(self, user_id=None):
        if not user_id:
            db = Database()
            result = db.findAllPlaces()
            return json.dumps(result)

        recommendations = get_recommendations(user_id)
        return recommendations

    def post(self):
        args = parser.parse_args()
        ratings = args.get('ratings')
        for rtUser in ratings:
            rtUserDict = ast.literal_eval(rtUser)
            db = Database()
            db.insertRating(
                rtUserDict['userId'], rtUserDict['placeId'], rtUserDict['rate']
            )

        return


class TopRecommendation(Resource):
    def get(self, user_id, n=4):
        recommendations = get_top_n_recommendations(user_id, n)

        return recommendations

    def post(self):
        args = parser.parse_args()
        ratings = args.get('ratings')

        for rtUser in ratings:
            rtUserDict = ast.literal_eval(rtUser)
            db = Database()
            db.insertSugestion(
                rtUserDict['userId'], rtUserDict['placeId'],
                rtUserDict['rate_prevision'], rtUserDict['rate_user'],
                rtUserDict['algorithm']
            )

        return


class Ratings(Resource):
    def get(self):
        db = Database()
        result = db.findAllRatings()
        return result
