import os
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from .models import db, User, People, Planet, Favorite

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    Migrate(app, db)

    CURRENT_USER_ID = int(os.getenv("CURRENT_USER_ID", 1))

    @app.get("/people")
    def people_list():
        return jsonify([{"id": p.id, "name": p.name} for p in People.query.all()])

    @app.get("/people/<int:people_id>")
    def people_detail(people_id):
        p = People.query.get_or_404(people_id)
        return jsonify({
            "id": p.id, "name": p.name, "height": p.height, "mass": p.mass,
            "hair_color": p.hair_color, "skin_color": p.skin_color,
            "eye_color": p.eye_color, "birth_year": p.birth_year, "gender": p.gender
        })

    @app.get("/planets")
    def planets_list():
        return jsonify([{"id": pl.id, "name": pl.name} for pl in Planet.query.all()])

    @app.get("/planets/<int:planet_id>")
    def planets_detail(planet_id):
        pl = Planet.query.get_or_404(planet_id)
        return jsonify({
            "id": pl.id, "name": pl.name, "climate": pl.climate,
            "terrain": pl.terrain, "population": pl.population, "diameter": pl.diameter
        })

    @app.get("/users")
    def users_list():
        return jsonify([{"id": u.id, "email": u.email} for u in User.query.all()])

    @app.get("/users/favorites")
    def user_favorites():
        favs = Favorite.query.filter_by(user_id=CURRENT_USER_ID).all()
        return jsonify([
            {"id": f.id,
             "people_id": f.people_id,
             "planet_id": f.planet_id}
            for f in favs
        ])

    @app.post("/favorite/planet/<int:planet_id>")
    def add_fav_planet(planet_id):
        db.session.add(Favorite(user_id=CURRENT_USER_ID, planet_id=planet_id))
        db.session.commit()
        return jsonify({"msg": "planet added"}), 201

    @app.post("/favorite/people/<int:people_id>")
    def add_fav_people(people_id):
        db.session.add(Favorite(user_id=CURRENT_USER_ID, people_id=people_id))
        db.session.commit()
        return jsonify({"msg": "people added"}), 201

    @app.delete("/favorite/planet/<int:planet_id>")
    def del_fav_planet(planet_id):
        f = Favorite.query.filter_by(user_id=CURRENT_USER_ID, planet_id=planet_id).first_or_404()
        db.session.delete(f); db.session.commit()
        return jsonify({"msg": "planet removed"})

    @app.delete("/favorite/people/<int:people_id>")
    def del_fav_people(people_id):
        f = Favorite.query.filter_by(user_id=CURRENT_USER_ID, people_id=people_id).first_or_404()
        db.session.delete(f); db.session.commit()
        return jsonify({"msg": "people removed"})

    return app

app = create_app()
