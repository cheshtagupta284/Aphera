from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity, jwt_optional
from models.store import StoreModel
from models.blood import BloodModel
from models.request import RequestModel
from models.user import UserModel

class StoreRegister(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument('city', 
        required = True, 
        type = str, 
        help = "This field cannot be left blank"
    )
    parser.add_argument('name', 
        required = True, 
        type = str, 
        help = "This field cannot be left blank"
    )

    @jwt_required
    def post(self):
        user_id = get_jwt_identity()
        # print(user_id)
        data = self.parser.parse_args()
        user = UserModel.find_user_by_id(user_id)
        if not(user) or user.role != 'registrar':
            return {"message" : "User not found"}, 404
        
        if StoreModel.find_store_by_user_id(user_id):
            # call '/auth' end point and return
            return {'message' : "One store per registrar"}, 400

        if StoreModel.find_store_by_name(data['name']):
            # call '/auth' end point and return
            return {'message' : "Name already exists."}, 400

        store = StoreModel(user_id=user_id,**data) #remember **kwargs is a dictionary?
        store.save_to_db()
        
        return {'message' : "Store created successfully"}, 201


class Store(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('store_id', type=int)
    @jwt_required
    def delete(self):

        user_id = get_jwt_identity()
        store = StoreModel.find_store_by_user_id(user_id)

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
            return {'message' : 'Store deleted'}, 200
            
        return {'message' : 'Store does not exist'}, 404 

    @jwt_required
    def get(self):
        data = self.parser.parse_args()
        store = StoreModel.find_store_by_id(data['store_id'])
        if store:
            return {'store' : store.json()}, 200
        return {'message' : 'Store does not exist'}, 404


class StoreList (Resource):
    def get(self):
        stores = [store.json() for store in StoreModel.find_all()]
        return {'stores' : stores}, 200
        

class StoreListCity (Resource):

    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        user = UserModel.find_user_by_id(user_id)
        stores = [store.json() for store in StoreModel.find_stores_by_city(user.city)]
        return {'stores' : stores}, 200