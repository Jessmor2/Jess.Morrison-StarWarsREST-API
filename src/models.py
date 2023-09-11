from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(30), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
        }
    
class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    persons_name = db.Column(db.String(50), nullable=False)
    height = db.Column(db.String(30), nullable=True)
    mass = db.Column(db.String(30), nullable=True)
    hair_color = db.Column(db.String(30), nullable=True)
    skin_color = db.Column(db.String(30), nullable=True)
    eye_color = db.Column(db.String(30), nullable=True)
    gender = db.Column(db.String(30), nullable=True)
    # planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    # vehicles_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'))
    # planets = db.relationship(Planets)
    # vehicles = db.relationship(Vehicles)


    def serialize(self):
        return {
            "name": self.persons_name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "gender": self.gender,
            # "planets_id": self.planets_id,
            # "vehicles_id": self.vehicles_id
        }
    
class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planets_name = db.Column(db.String(50), nullable=False)
    diameter = db.Column(db.String(30), nullable=False)
    rotation_period = db.Column(db.String(30), nullable=True)
    orbital_period = db.Column(db.String(30), nullable=True)
    gravity = db.Column(db.String(30), nullable=True)
    population = db.Column(db.String(30), nullable=True)
    climate = db.Column(db.String(30), nullable=True)
    terrain = db.Column(db.String(30), nullable=True)
    description = db.Column(db.String(100), nullable=True)

    def serialize(self):
        return {
            "name": self.planets_name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "description": self.description,
        }
    
class Vehicles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicles_name = db.Column(db.String(80), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    vehicle_class = db.Column(db.String(50), nullable=True)
    manufacturer = db.Column(db.String(50), nullable=True)
    cost_in_credits = db.Column(db.String(50), nullable=True)
    length = db.Column(db.String(50), nullable=True)
    crew = db.Column(db.String(50), nullable=True)
    passengers = db.Column(db.String(50), nullable=True)

    def serialize(self):
        return {
            "vehicles_name": self.vehicles_name,
            "model": self.model,
            "vehicle_class": self.vehicle_class,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "crew": self.crew,
            "passengers": self.passengers,
        }


    
class Favorites(db.Model):
    __tablename__ = "favorites"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=True)
    planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=True)
    vehicles_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=True)
    user = db.relationship(User)
    people = db.relationship(People)
    planets = db.relationship(Planets)
    vehicles = db.relationship(Vehicles)

    def serialize(self):
        return {
            "user_id": self.user_id,
            "people_id": self.people_id,
            "vehicles_id": self.vehicles_id,
            "planets_id": self.planets_id,
        }