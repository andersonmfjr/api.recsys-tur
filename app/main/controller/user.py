from flask_restplus import Resource, reqparse
from app.main.database.database import Database
import json

parser = reqparse.RequestParser()
parser.add_argument('email')


class User(Resource):
    def get(self, user_id=None):
        db = Database()

        if not user_id:
            result = db.findAllUsers()
            return json.dumps(result)

        result = db.findUserById(user_id)
        return json.dumps(result)

    def post(self):
        args = parser.parse_args()
        db = Database()
        user = db.insertUser(args.email)
        return json.dumps(user)
