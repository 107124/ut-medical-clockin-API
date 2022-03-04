from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

my_app = Flask(__name__)

base_file = os.path.abspath(os.path.dirname(__file__))
my_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(base_file, "app.sqlite")

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

    return(f"Date: {date}\nTime: {time} was successfully deleted")


if __name__ == "__main__":
    my_app.run(debug=True)

