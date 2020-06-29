from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_raw_jwt
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST
from models.user import UserModel
from models.request import RequestModel
from models.store import StoreModel
from models.blood import BloodModel

# A resource to register users because users will be registered through an endpoint


class UserRegister(Resource):

    # Create a parser
    parser = reqparse.RequestParser()

    parser.add_argument('email',
                        required=True,
                        type=str,
                        help="This field cannot be left blank"
                        )
    parser.add_argument('password',
                        required=True,
                        type=str,
                        help="This field cannot be left blank"
                        )
    parser.add_argument('city',
                        required=True,
                        type=str,
                        help="This field cannot be left blank"
                        )
    parser.add_argument('contact',
                        required=True,
                        type=int,
                        help="This field cannot be left blank"
                        )
    parser.add_argument('role',
                        required=True,
                        type=str,
                        help="This field cannot be left blank"
                        )
    parser.add_argument('name',
                        required=True,
                        type=str,
                        help="This field cannot be left blank"
                        )
    parser.add_argument('types',
                        type=str,
                        )
    parser.add_argument('age',
                        type=int,
                        )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_user_by_email(data['email']):
            # call '/auth' end point and return
            return {'message': "email already exists."}, 400

        user = UserModel(**data)  # remember **kwargs is a dictionary?
        user.save_to_db()

        return {'message': "Sign up successful"}, 201


# A resource to list all users
class UserList(Resource):

    def get(self):
        return {'users': [user.json() for user in UserModel.find_all()]}, 200

# A resource to manage users


class User(Resource):

    @jwt_required
    def delete(self):
        user_id = get_jwt_identity()
        user = UserModel.find_user_by_id(user_id)

        if user:
            if user.role == 'registrar':
                store = StoreModel.find_store_by_user_id(user.id)
                if store:
                    blood_list = BloodModel.find_blood_in_store(store.id)
                    for blood in blood_list:
                        blood.delete_from_db()
                    request_list = RequestModel.find_request_in_store(store.id)
                    for request in request_list:
                        u = UserModel.find_user_by_id(request.user_id)
                        u.status = "none"
                        u.save_to_db()
                        request.delete_from_db()
                    store.delete_from_db()

            request_list = RequestModel.find_request_of_user(user.id)
            for request in request_list:
                request.delete_from_db()
            user.delete_from_db()
            jti = get_raw_jwt()['jti']
            BLACKLIST.add(jti)
            return {'message': 'User deleted successfully'}, 200

        return {'message': 'User not found'}, 404

    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        user = UserModel.find_user_by_id(user_id)
        if user:
            return {'user': user.json()}, 200
        return {'message': 'User not found'}, 404


class UserRequest(Resource):
    parser = reqparse.RequestParser()

    # status = accepted, denied
    parser.add_argument('status', type=str, required=True,
                        help="Required field")
    parser.add_argument('store_id', type=int,
                        required=True, help="Required field")
    parser.add_argument('types', type=str)

    @jwt_required
    def put(self):
        data = self.parser.parse_args()
        user_id = get_jwt_identity()
        user = UserModel.find_user_by_id(user_id)

        request = RequestModel.find_request_of_user_in_store(
            user_id, data['store_id'])
        if not(request):
            return {'message': 'No request found'}, 404

        user.status = data['status']
        user.save_to_db()

        if user.role == 'registrar':
            types = data['types']
        else:
            types = user.types

        if data['status'] == 'accepted':
            requests = RequestModel.find_requests_by_store_and_type(
                data['store_id'], types)
            for request in requests:
                if request.user_id != user.id:
                    u = UserModel.find_user_by_id(request.user_id)
                    if u.status != 'accepted':
                        u.status = 'none'
                        u.save_to_db()
                        r = RequestModel.find_request_by_id(request.id)
                        r.delete_from_db()

        return {'message': "Request status modified"}, 200


class UserLogin(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('email',
                        required=True,
                        type=str,
                        help='This field is required'
                        )

    parser.add_argument('password',
                        required=True,
                        type=str,
                        help='This field is required'
                        )

    def post(self):
        data = self.parser.parse_args()
        user = UserModel.find_user_by_email(data['email'])
        if user and safe_str_cmp(data['password'], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            return {
                'access_token': access_token
            }, 200

        return {'message': 'Invalid Credentials'}, 401


class UserLogout(Resource):

    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {'message': 'Logged out successfully'}, 200
