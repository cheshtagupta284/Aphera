from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(20))

    bloods = db.relationship('BloodModel', lazy='dynamic')
    requests = db.relationship('RequestModel', lazy='dynamic')

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('UserModel')

    def __init__(self, user_id, name, city):
        self.name = name
        self.city = city
        self.user_id = user_id

    def json(self):

        return {'id': self.id,
                'name': self.name,
                'user_id': self.user_id,
                'city': self.city,
                'bloods': [blood.json() for blood in self.bloods.all()],
                'requests': [request.json() for request in self.requests.all()]
                }

    @classmethod
    def find_store_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_store_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def find_store_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_stores_by_city(cls, city):
        return cls.query.filter_by(city=city).all()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
