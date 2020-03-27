# Resource class
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.blood import BloodModel
from models.store import StoreModel
from models.user import UserModel


class Blood(Resource):
    # Make a parser common to a class
    # Access it to get data using data = <class_types>.<parser_types>.parse_args()
    parser = reqparse.RequestParser()
    # Add arguments to the parser
    parser.add_argument('types',
                        type=str,
                        required=True,
                        help="This field cannot be left blank"
                        )

    # Create a new blood
    @jwt_required
    def post(self):
        data = self.parser.parse_args()

        user_id = get_jwt_identity()
        user = UserModel.find_user_by_id(user_id)

        if user.role != 'registrar':
            return {'message': 'This request is not allowed'}, 400

        stores = user.json()['stores']
        if stores == []:
            return {'message': 'Store is not created'}, 404

        blood = BloodModel.find_blood_by_store_and_type(
            stores[0]['id'], data['types'])
        if blood:
            return {'message': "The blood '{}' already exists".format(blood.types)}, 400

        new_blood = BloodModel(data['types'], stores[0]['id'])
        try:
            new_blood.save_to_db()
        except:
            return {'message': "An unknown error occurred"}, 500

        return new_blood.json(), 201

    @jwt_required
    def delete(self):
        data = Blood.parser.parse_args()

        user_id = get_jwt_identity()
        user = UserModel.find_user_by_id(user_id)

        if user.role != 'registrar':
            return {'message': 'This request is not allowed'}, 400

        stores = user.json()['stores']
        blood = BloodModel.find_blood_by_store_and_type(
            stores[0]['id'], data['types'])
        if blood:
            blood.delete_from_db()
            return {'message': "Blood deleted"}, 200

        return {'message': "Blood not found"}, 200

    def put(self, types):
        data = Blood.parser.parse_args()
        blood = BloodModel.find_blood_by_types(types)

        if blood is None:
            blood = BloodModel(types, **data)
        else:
            blood.types = data['types']

        try:
            blood.save_to_db()
        except:
            return {'message': "An unknown error occurred while updating"}, 500

        return blood.json(), 201


# Resource bloodsList
class BloodList(Resource):
    @jwt_required
    def get(self):
        return {'bloods': [blood.json() for blood in BloodModel.find_all()]}


class BloodListStore(Resource):

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
        return {'bloods': [blood.json() for blood in BloodModel.find_blood_in_store(store_id)]}
