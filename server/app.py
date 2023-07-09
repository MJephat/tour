#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import db, Hotel, Traveller, Activity


app = Flask(__name__)
cor_s = CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def hotels1():
    return 'welcome to hotels'
    
@app.route('/hotels')
def hotels():

    hotels =  []
    for hotel in   Hotel.query.all():
        hotel_dict = {
            "id": hotel.id,
            "name": hotel.name,
            "address": hotel.address,
        }
        hotels.append(hotel_dict)
    response =make_response(
        jsonify(hotels),
        200
    )
    return response
    
@app.route('/hotels/<int:id>')
def hotel_by_id(id):
    hotel = Hotel.query.filter_by(id=id).first()

    hotel_dict = hotel.to_dict()

    response = make_response(
        jsonify(hotel_dict),
        200
    )
    response.headers["Content-Type"] = "application/json"

    return response

@app.route('/hotels', methods=['POST','DELETE','PATCH'])
def post_hotels():
    if request.method == 'POST':
        new_hotel = Hotel(
            name=request.form.get("name"),
            address=request.form.get("address"),
            image = request.form.get("image_url"),
            traveller_id=request.form.get("traveller_id"),
            activity_id=request.form.get("activity_id"),
        )

        db.session.add(new_hotel)
        db.session.commit()

        hotel_dict = new_hotel.to_dict()

        response = make_response(
            jsonify(hotel_dict),
            201
        )

        return response


@app.route('/travellers', methods=['POST','DELETE','PATCH'])
def post_travellers1():
    if request.method == 'POST':
        new_traveller = Traveller(
            name=request.form.get("name"),
            # gender=request.form.get("gender"),
            email=request.form.get("email"),
            date=request.form.get("date"),
        )

        db.session.add(new_traveller)
        db.session.commit()

        traveller_dict = new_traveller.to_dict()

        response = make_response(
            jsonify(traveller_dict),
            201
        )

        return response

@app.route('/travellers')
def travellers():

    travellers =  []
    for traveller in   Traveller.query.all():
        traveller_dict = {
            "id": traveller.id,
            "name": traveller.name,
            "gender": traveller.gender,
            "date": traveller.date
        }
        travellers.append(traveller_dict)
    response =make_response(
        jsonify(travellers),
        200
    )
    return response



@app.route('/travellers/<int:id>', methods=[  'PATCH', 'DELETE'])
def traveller_by_id(id):
    traveller = Traveller.query.filter_by(id=id).first()

    if traveller == None:
        response_body = {
            "message": "This record does not exist in our database. Please try again."
        }
        response = make_response(jsonify(response_body), 404)

        return response

    else:
        if request.method == 'PATCH':
            traveller = Traveller.query.filter_by(id=id).first()

            for attr in request.form:
                setattr(traveller, attr, request.form.get(attr))

            db.session.add(traveller)
            db.session.commit()

            traveller_dict = traveller.to_dict()

            response = make_response(
                jsonify(traveller_dict),
                200
            )

            return response

        elif request.method == 'DELETE':
            db.session.delete(traveller)
            db.session.commit()

            response_body = {
                "delete_successful": True,
                "message": "Traveller deleted."    
            }

            response = make_response(
                jsonify(response_body),
                200
            )

            return response

@app.route('/activities')
def activities():

    activities =  []
    for activity in   Activity.query.all():
        activity_dict = {
            "id": activity.id,
            "exploit": activity.exploit,
            "description": activity.description,
            "time": activity.time
        }
        activities.append(activity_dict)
    response =make_response(
        jsonify(activities),
        200
    )
    return response


if __name__ == '__main__':
     app.run(port=5555)