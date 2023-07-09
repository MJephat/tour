from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import MetaData

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)



class Hotel(db.Model, SerializerMixin):
    __tablename__ = 'hotels'

    serialize_rules = ('-traveller.hotels', '-activity.hotels',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(255))
    address = db.Column(db.String(100), nullable=False)
    traveller_id = db.Column(db.Integer, db.ForeignKey('travellers.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'))

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    # updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    
    
class Traveller(db.Model, SerializerMixin):
    __tablename__ = 'travellers'

    serialize_rules = ('-hotels.traveller',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    gender = db.Column(db.String(50))
    email = db.Column(db.String(50))
    date = db.Column(db.String(20))

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    # updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    hotels = db.relationship('Hotel', backref='traveller')

class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    serialize_rules = ('-hotels.activity',)

    id = db.Column(db.Integer, primary_key=True)
    exploit = db.Column(db.String(100))
    description = db.Column(db.String(100))
    time = db.Column(db.String(50))

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    # updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    hotels = db.relationship('Hotel', backref='activity')
    
