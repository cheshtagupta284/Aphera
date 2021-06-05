from db import db
from models.user import UserModel
from models.store import StoreModel


class RequestModel (db.Model):

    __tablename__ = 'requests'

    id = db.Column(db.Integer, primary_key=True)
    types = db.Column(db.String(5))
    status = db.Column(db.String(10))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('UserModel')

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, types, user_id, store_id, status="none"):
        self.user_id = user_id
        self.store_id = store_id
        self.types = types
        self.status = status

    def json(self):
        store = StoreModel.find_store_by_id(self.store_id)
        if not(store):
            return

        user = UserModel.find_user_by_id(store.user_id)
        receiver = UserModel.find_user_by_id(self.user_id)

        return {'id': self.id,
                'types': self.types,
                'store_id': self.store_id,
                'contact': user.contact,
                'email': user.email,
                'name': store.name,
                'user_id': self.user_id,
                'receiver_name': receiver.name,
                'receiver_mail': receiver.email,
                'receiver_contact': receiver.contact,
                'status': self.status
                }

    @classmethod
    def find_requests_by_store_and_type_and_status(cls, store_id, types, status):
        return cls.query.filter_by(store_id=store_id, types=types, status=status).all()

    @classmethod
    def find_requests_by_store_and_type(cls, store_id, types):
        return cls.query.filter_by(store_id=store_id, types=types).all()

    @classmethod
    def find_requests_by_store_and_type_and_id(cls, store_id, types, _id):
        return cls.query.filter_by(store_id=store_id, types=types, id=_id).all()

    @classmethod
    def find_request_in_store(cls, store_id):
        return cls.query.filter_by(store_id=store_id).all()

    @classmethod
    def find_request_of_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def find_request_of_user_in_store(cls, user_id, store_id):
        return cls.query.filter_by(user_id=user_id, store_id=store_id).first()

    @classmethod
    def find_request_by_types(cls, types):
        return cls.query.filter_by(types=types).first()

    @classmethod
    def find_request_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
