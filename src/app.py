"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, Vehicles, Favorites

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user/<int:user_id>', methods=['GET'])
def handle_user(user_id):
    user1 = User.query.get(user_id)
    return jsonify(user1.serialize()), 200

@app.route('/people', methods=['GET'])
def handle_people():
    if request.method == 'GET':
        allPeople = People.query.all()
        people_serialize = [character.serialize()for character in allPeople]
        return jsonify(people_serialize), 200

@app.route('/people/<int:person_id>', methods=['PUT', 'GET'])
def get_single_person(person_id):
    if request.method == 'GET':
        person1 = People.query.get(person_id)
        return jsonify(person1.serialize()), 200
    
    return "Person not found", 404

@app.route('/planets', methods=['GET'])
def handle_planets():
    allPlanets = Planets.query.all()
    planet_serialize = [world.serialize()for world in allPlanets]
    return jsonify(planet_serialize), 200

@app.route('/planets/<int:planets_id>', methods=['PUT', 'GET'])
def get_single_planet(planets_id):
    if request.method == 'GET':
        planet1 = Planets.query.get(planets_id)
        return jsonify(planet1.serialize()), 200
    
    return "Person not found", 404


@app.route('/vehicles', methods=['GET'])
def handle_vehicles():
    allvehicles = Vehicles.query.all()
    vehicle_serialize = [machine.serialize()for machine in allvehicles]
    return jsonify(vehicle_serialize), 200
     
@app.route('/vehicles/<int:vehicles_id>', methods=['PUT', 'GET'])
def get_single_vehicle(vehicles_id):
    if request.method == 'GET':
        vehicle1 = Vehicles.query.get(vehicles_id)
        return jsonify(vehicle1.serialize()), 200
    
    return "Person not found", 404

@app.route('/favorites', methods=['GET'])
def handle_favorites():
    allFavorites = Favorites.query.all()
    favorite_serialize = [saved.serialize()for saved in allFavorites]
    return jsonify(favorite_serialize), 200

@app.route('/favorites/planets/<int:planets_id>', methods=['POST'])
def add_fav_planet(planets_id):
    data = request.get_json()
    new_Fav_Planet = Favorites(user_id=data["user_id"], planets_id = planets_id)
    db.session.add(new_Fav_Planet)
    db.session.commit()
    return jsonify(new_Fav_Planet.serialize()), 200
@app.route('/favorites/people/<int:people_id>', methods=['POST'])
def add_fav_person(person_id):
    data = request.get_json()
    new_Fav_Person = Favorites(user_id=data["user_id"], person_id = person_id)
    db.session.add(new_Fav_Person)
    db.session.commit()
    return jsonify(new_Fav_Person.serialize()), 200
@app.route('/favorites/vehicles/<int:vehicles_id>', methods=['POST'])
def add_fav_vehicle(vehicles_id):
    data = request.get_json()
    new_Fav_Vehicle = Favorites(user_id=data["user_id"], vehicles_id = vehicles_id)
    db.session.add(new_Fav_Vehicle)
    db.session.commit()
    return jsonify(new_Fav_Vehicle.serialize()), 200
    
@app.route('/favorites/planets/<int:planets_id>', methods=['DELETE'])
def delete_fav_planet(planets_id):
    data = request.get_json()
    user_id = data["user_id"]
    remove_planet = Favorites.query.filter_by(planets_id=planets_id, user_id=user_id).first()
    db.session.delete(remove_planet)
    db.session.commit()
    return jsonify("removed planet successfully"), 200
@app.route('/favorites/vehicles/<int:vehicles_id>', methods=['DELETE'])
def delete_fav_vehicle(vehicles_id):
    data = request.get_json()
    user_id = data["user_id"]
    remove_vehicle = Favorites.query.filter_by(vehicles_id=vehicles_id, user_id=user_id).first()
    db.session.delete(remove_vehicle)
    db.session.commit()
    return jsonify("removed vehicle successfully"), 200
@app.route('/favorites/people/<int:person_id>', methods=['DELETE'])
def delete_fav_person(person_id):
    data = request.get_json()
    user_id = data["user_id"]
    remove_person = Favorites.query.filter_by(person_id=person_id, user_id=user_id).first()
    db.session.delete(remove_person)
    db.session.commit()
    return jsonify("removed person successfully"), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
