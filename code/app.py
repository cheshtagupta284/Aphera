from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.blood import Blood, BloodList, BloodListStore
from resources.store import Store, StoreList, StoreRegister, StoreListCity
from resources.request import RequestList, RequestListStore, RequestListUser, Request
from resources.user import UserRegister, UserList, User, UserLogin, UserLogout, UserRequest
from flask_cors import CORS, cross_origin
from blacklist import BLACKLIST

# Create App
app = Flask(__name__)

# Create API
api = Api(app)
CORS(app)

# SQL Alchemy database connect
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

# Ask the flask modifications tracker to stop as we already have one in sqlalchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Allow JWT to raise its own exception
app.config['PROPAGATE_EXCEPTIONS'] = True

# Expiration for access token
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
# Important!! to have a security key
app.secret_key = 'tanishq'

# To create a database
@app.before_first_request
def create_tables():
    db.create_all()


# Make a JWT object
jwt = JWTManager(app)


@jwt.token_in_blacklist_loader
def token_in_blacklist_loader(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST


# Add resources to Api
api.add_resource(Blood, '/blood')
api.add_resource(BloodList, '/bloods')
api.add_resource(BloodListStore, '/bloods/store')

api.add_resource(StoreRegister, '/store/register')
api.add_resource(Store, '/store')
api.add_resource(StoreList, '/stores')
api.add_resource(StoreListCity, '/stores/city')

api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user')
api.add_resource(UserList, '/users')
api.add_resource(UserRequest, '/user/request')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')

api.add_resource(RequestList, '/requests')
api.add_resource(RequestListStore, '/requests/store')
api.add_resource(RequestListUser, '/requests/user')
api.add_resource(Request, '/request')

# Run the app
if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
