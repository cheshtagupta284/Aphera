from db import db

class BloodModel (db.Model):
    __tabletypes__ = 'bloods'

    id = db.Column(db.Integer, primary_key = True)
    types = db.Column(db.String(5))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')


    def __init__(self, types, store_id):        
        self.types = types
        self.store_id = store_id

    def json(self):
        return  {'id' : self.id,
                 'types' : self.types, 
                 'store_id' : self.store_id
                }
        
    @classmethod
    def find_blood_by_store_and_type(cls, store_id, types):
        return cls.query.filter_by(store_id=store_id, types = types).first()
    
    @classmethod
    def find_blood_in_store(cls, store_id):
        return cls.query.filter_by(store_id=store_id).all()

    @classmethod
    def find_blood_by_types(cls, types):
        return cls.query.filter_by(types=types).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()