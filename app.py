from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os
from flask_heroku import Heroku
# import psycopg2

my_app = Flask(__name__)
heroku = Heroku(my_app)
# base_file = os.path.abspath(os.path.dirname(__file__))
# my_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(base_file, "app.sqlite")

base_file = os.path.abspath(os.path.dirname(__file__))
my_app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://qvimxnvgmxqrwd:9717a39d81934c9b0cc5e037d0ed19520e0d0a78cb5d8893b234ebe2c0a2ac43@ec2-44-195-191-252.compute-1.amazonaws.com:5432/d31kda6bjh23gl"

CORS(my_app)

db = SQLAlchemy(my_app)
marsh = Marshmallow(my_app)

class Stamps(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100))
    time = db.Column(db.String(20))

    def  __init__(self, date, time):
        self.date = date
        self.time = time

class StampSchema(marsh.Schema):
    class Meta:
        fields = ("date", "time")

stamp_schema = StampSchema()
stamps_schema = StampSchema(many=True)

# This will create a single time stamp
@my_app.route("/stamp", methods =["POST"])
def add_project():
    date = request.json["date"]
    time = request.json["time"]

    new_stamp = Stamps(date, time)

    db.session.add(new_stamp)
    db.session.commit()

    stamp = Stamps.query.get(new_stamp.id)
    return(stamp_schema.jsonify(stamp))


# This will query all the stamps!
@my_app.route("/stamps", methods=["GET"])
def get_stamps():
    all_stamps = Stamps.query.all()
    result = stamps_schema.dump(all_stamps)
    return(jsonify(result))


# This will query a SINGLE stamp!
@my_app.route("/stamp/<id>", methods=["GET"])
def get_stamp(id):
    stamp = Stamps.query.get(id)
    return(stamp_schema.jsonify(stamp))


# This will update a single stamp
@my_app.route("/stamp/<id>", methods=["PUT"])
def stamp_update(id):
    stamp = Stamps.query.get(id)
    date = request.json["date"]
    time = request.json["time"]

    stamp.date = date
    stamp.time = time
    db.session.commit()

    return stamp_schema.jsonify(stamp)


# This will delete a single stamp
@my_app.route("/stamp/<id>", methods=["DELETE"])
def stamp_delete(id):
    stamp = Stamps.query.get(id)
    date = request.json["date"]
    time = request.json["time"]

    db.session.delete(stamp)
    db.session.commit()

    return(f"Date:{date}\nTime: {time} was successfully deleted")


if __name__ == "__main__":
    my_app.run(debug=True)

# to install postgress:
# heroku addons:create heroku-postgresql:hobby-dev
# pip install psycopg2-binary then import psycopg2 at the top
# pip install flask-cors
# from flask_cors import CORS
# Then: CORS(my_app) AFTER app.config line
# pipenv install flask gunicorn
# pip install flask_heroku
# from flask_heroku import Heroku
# after my_app = Flask(__name__) say: heroku = Heroku(app)
# IMPORTANT!
# After adding the new postgres uri, make sure to delete the app.sqlite file, then get
# into the python repl, from nameOfFile import db, then db.create_all() to create the new
# database for postgress
# IMPORTANT!
# change the URI from postgres:// to postgresql://

# IF there's a h10 error in the heroku logs --tail, make sure you update the requirements.txt file by doing:
# pip freeze > requirements.txt