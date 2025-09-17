from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    favorites = db.relationship("Favorite", back_populates="user", cascade="all, delete-orphan")

class People(db.Model):
    __tablename__ = "people"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    height = db.Column(db.String(20))
    mass = db.Column(db.String(20))
    hair_color = db.Column(db.String(20))
    skin_color = db.Column(db.String(20))
    eye_color = db.Column(db.String(20))
    birth_year = db.Column(db.String(20))
    gender = db.Column(db.String(20))

class Planet(db.Model):
    __tablename__ = "planet"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    climate = db.Column(db.String(80))
    terrain = db.Column(db.String(80))
    population = db.Column(db.String(30))
    diameter = db.Column(db.String(30))

class Favorite(db.Model):

    __tablename__ = "favorite"
    id = db.Column(db.Integer, primary_key=True)
    user_id   = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    people_id = db.Column(db.Integer, db.ForeignKey("people.id"), nullable=True)
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"), nullable=True)

    __table_args__ = (
        UniqueConstraint("user_id", "people_id", name="uq_user_people"),
        UniqueConstraint("user_id", "planet_id", name="uq_user_planet"),
    )

    user   = db.relationship("User", back_populates="favorites")
    people = db.relationship("People")
    planet = db.relationship("Planet")
