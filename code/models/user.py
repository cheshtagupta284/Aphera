from db import db
# NOT a resource because we dont acces it by endpoints yet


class UserModel(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80))
    password = db.Column(db.String(80))
    name = db.Column(db.String(80))
    city = db.Column(db.String(20))
    role = db.Column(db.String(10))
    contact = db.Column(db.Integer, unique=True)
    age = db.Column(db.Integer)
    types = db.Column(db.String(5))
    status = db.Column(db.String(20))
    requests = db.relationship('RequestModel', lazy='dynamic')
    stores = db.relationship('StoreModel', lazy='dynamic')

    def __init__(self, email, name, password, city, contact, role, types="", age=0, status='none'):
        self.email = email
        self.name = name
        self.contact = contact
        self.age = age
        self.city = city
        self.role = role
        self.password = password
        self.types = types
        self.status = status

    def json(self):
        return {'id': self.id,
                'role': self.role,
                'email': self.email,
                'name': self.name,
                "password": self.password,
                'age': self.age,
                'types': self.types,
                'city': self.city,
                'status': self.status,
                'contact': self.contact,
                'stores': [store.json() for store in self.stores.all()],
                'requests': [request.json() for request in self.requests.all()]
                }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # A mapping to retreive data from the database using email
    # A classmethod decorator to allow not to hardcode class name
    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_users_by_city_types_status(cls, city, types, status):
        return cls.query.filter_by(city=city, types=types, status=status).all()

    @classmethod
    def find_users_by_city_types_role_status(cls, city, types, role, status):
        return cls.query.filter_by(city=city, types=types, role=role, status=status).all()

    @classmethod
    def find_users_by_city_types_role(cls, city, types, role):
        return cls.query.filter_by(city=city, types=types, role=role).all()

    @classmethod
    def find_users_by_city_types(cls, city, types):
        return cls.query.filter_by(city=city, types=types).all()

    @classmethod
    def find_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    # A mapping to retreive data from the database using email
    @classmethod
    def find_user_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
