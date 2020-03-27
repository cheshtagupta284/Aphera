from flask_restful import reqparse
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.store import StoreModel
from models.blood import BloodModel
from models.user import UserModel
from models.request import RequestModel


class Request(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('types', type=str, required=True,
                        help='This field is required')
    parser.add_argument('_id', type=int)

    # status made pending
    @jwt_required
    def post(self):

        data = self.parser.parse_args()
        user_id = get_jwt_identity()
        user = UserModel.find_user_by_id(user_id)

        if user.role != 'registrar':
            return {'message': 'This request is not allowed'}, 400

        stores = user.json()['stores']
        if stores == []:
            return {'message': 'No store avaialable'}, 404

        requests = RequestModel.find_requests_by_store_and_type_and_status(
            stores[0]['id'], data['types'], 'pending')
        # If requests is not an empty list
        if requests != []:
            return {'message': 'Request already Exists'}, 400

        blood = BloodModel.find_blood_by_store_and_type(
            stores[0]['id'], data['types'])
        # If blood type already there in the store
        if blood:
            return {'message': 'Blood {} already exists in database'.format(data['types'])}, 400

        # Request sent to users with status other than accepted and registrars having blood in their store
        users_none = UserModel.find_users_by_city_types_role_status(
            stores[0]['city'], data['types'], 'user', 'pending')
        users_pending = UserModel.find_users_by_city_types_role_status(
            stores[0]['city'], data['types'], 'user', 'none')
        stores_city = StoreModel.find_stores_by_city(user.city)

        u_id = []
        for s in stores_city:
            if s.name != stores[0]['name']:
                bloods = s.json()['bloods']
                for blood in bloods:
                    if blood['types'] == data['types']:
                        store_blood = StoreModel.find_store_by_id(
                            blood['store_id'])
                        user = UserModel.find_user_by_id(store_blood.user_id)
                        u_id.append(store_blood.user_id)

        if users_none == [] and users_pending == [] and u_id == []:
            return {'message': 'No users or stores available'}, 404

        for user in users_none:
            user.status = 'pending'
            user.save_to_db()
            request = RequestModel(
                data['types'], status='pending', user_id=user.id, store_id=stores[0]['id'])
            request.save_to_db()

        for user in users_pending:
            user.status = 'pending'
            user.save_to_db()
            request = RequestModel(
                data['types'], status='pending', user_id=user.id, store_id=stores[0]['id'])
            request.save_to_db()

        for u in u_id:
            user = UserModel.find_user_by_id(u)
            user.status = 'pending'
            user.save_to_db()
            request = RequestModel(
                data['types'], status='pending', user_id=user.id, store_id=stores[0]['id'])
            request.save_to_db()

        return {'message': 'Request created successfully'}, 201

    @jwt_required
    def put(self):
        # A refresh button
        data = self.parser.parse_args()
        user_id = get_jwt_identity()
        user = UserModel.find_user_by_id(user_id)

        if user.role != 'registrar':
            return {'message': 'This request is not allowed'}, 400

        stores = user.json()['stores']
        for store in stores:
            store_id = store['id']

        requests = RequestModel.find_requests_by_store_and_type_and_id(
            store_id, data['types'], data['_id'])

        if requests == []:
            return {'message': 'Request does not exist'}, 404

        for request in requests:
            u = UserModel.find_user_by_id(request.user_id)
            if u.status == 'accepted':
                request.status = 'accepted'
                request.save_to_db()
                return {'request': request.json()}, 201

        return {'request': requests[0].json()}, 201


class RequestListStore(Resource):

    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        user = UserModel.find_user_by_id(user_id)
        if user.role != 'registrar':
            return {'message': 'This request is not allowed'}, 400

        stores = user.json()['stores']
        store_id = 0
        for store in stores:
            store_id = store['id']

        return {'requests': [request.json() for request in RequestModel.find_request_in_store(store_id)]}


class RequestListUser(Resource):
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        return {'requests': [request.json() for request in RequestModel.find_request_of_user(user_id) if request]}


class RequestList(Resource):
    # @jwt_required
    def get(self):
        return {'requests': [request.json() for request in RequestModel.find_all()]}
