import os
from flask import Flask, jsonify, render_template, request, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

key = os.getenv("SECRET_KEY")


# CREATE DB
class Base(DeclarativeBase):
    pass


# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route('/random', methods=['GET'])
def random_cafe():
    cafes = db.session.execute(db.select(Cafe)).scalars()
    _random_cafe = random.choice(list(cafes))
    return create_json([_random_cafe])


@app.route('/all', methods=['GET'])
def all_cafes():
    cafes = list(db.session.execute(db.select(Cafe)).scalars())
    return create_json(cafes)


@app.route('/search', methods=['GET'])
def search_cafe():
    location = request.args.get('loc')
    name = request.args.get('name')

    query = db.select(Cafe)
    if location:
        query = query.where(Cafe.location == location)
    if name:
        query = query.where(Cafe.name == name)

    cafes = list(db.session.execute(query).scalars())
    return create_json(cafes)


# HTTP POST - Create Record

@app.route('/add', methods=['POST'])
def add_cafe():
    print("Sent");
    with app.app_context():
        try:
            cafe = Cafe(name=request.form.get('name'), map_url=request.form.get('map_url'),
                        img_url=request.form.get('img_url'), location=request.form.get('loc'),
                        seats=request.form.get('seats'), has_toilet=request.form.get('toilet'),
                        has_wifi=request.form.get('wifi'),
                        has_sockets=request.form.get('sockets'), can_take_calls=request.form.get('calls'),
                        coffee_price=request.form.get('price'), )
            db.session.add(cafe)
            db.session.commit()
        finally:
            return create_json([cafe])


# HTTP PUT/PATCH - Update Record
@app.route('/update-price/<cafe_id>', methods=['PATCH'])
def update_price(cafe_id):
    with app.app_context():
        cafe = Cafe.query.get_or_404(cafe_id)
        cafe.coffee_price = request.args.get('new_price')
        print(cafe.coffee_price)
        db.session.commit()
        return create_json([cafe])


# HTTP DELETE - Delete Record

@app.route('/report-closed/<cafe_id>', methods=['DELETE'])
def delete(cafe_id):
    with app.app_context():
        cafe = Cafe.query.get_or_404(cafe_id)
        db.session.delete(cafe)
        db.session.commit()
        return jsonify({"success": True})


# HELPER

@app.before_request
def check_api_key():
    api_key = request.headers.get('api-key')
    if api_key != key:
        abort(403)  # Forbidden

def create_json(cafes):
    data = {}
    if len(cafes) > 0:
        for cafe in cafes:
            data[cafe.id] = {
                'name': cafe.name,
                'map_url': cafe.map_url,
                'img_url': cafe.img_url,
                'location': cafe.location,
                'seats': cafe.seats,
                'has_toilet': cafe.has_toilet,
                'has_wifi': cafe.has_wifi,
                'has_sockets': cafe.has_sockets,
                'can_take_calls': cafe.can_take_calls,
                'coffee_price': cafe.coffee_price
            }

        return jsonify(data)
    else:
        return jsonify({'error': 'No cafe found or created'}), 404


if __name__ == '__main__':
    app.run(debug=True)
