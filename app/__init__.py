import os
from flask import Flask
from flask_restplus import Api
from flask_cors import CORS
import app.config

from app.main.controller.recommendation import Recommentation, TopRecommendation, Ratings
from app.main.controller.user import User

app = Flask(__name__, static_folder=None)
CORS(app)
app.secret_key = config.SECRET_KEY
api = Api(app)

api.add_resource(Recommentation, '/evaluation', '/evaluation/<int:user_id>')
api.add_resource(TopRecommendation, '/suggestion', '/suggestion/<int:user_id>')
api.add_resource(User, '/users', '/users/<int:id>')
api.add_resource(Ratings, '/ratings')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
