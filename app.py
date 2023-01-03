from flask import Flask, request, jsonify, render_template
import requests
from database import find_places_in_specific_distance
import maxminddb
from flask_restful import Resource, Api, reqparse
import google.cloud.logging
import logging
from subprocess import run
import os
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
api = Api(app)


client = google.cloud.logging.Client()
client.setup_logging()


class HomePage(Resource):
    def get(self):
        return render_template("home.html"), 200


class DataBase(Resource):
    def get(self, distance: int, user_latitude, user_longitude):
        try:
            logging.info(f"Running on {user_latitude} {user_longitude} coordinates, distance: {distance*1000}")
            result = find_places_in_specific_distance(user_latitude, user_longitude, distance*1000)
        except Exception as e:
            logging.info("Database - FAIL")
            logging.error(e)
            result = str(e)
        logging.info("Database - SUCCEED")
        return {"db_response": result}, 200


class UserIP(Resource):
    def get_location(self, ip_addr):
        coordinates = ""
        try:
            logging.info("User IP: trying to get coordinates")
            with maxminddb.open_database('city_local_database.mmdb') as reader:
                coordinates = reader.get(ip_addr)
        except Exception as e:
            logging.info("User IP: trying to get coordinates - FAIL")
            logging.error(e)
            coordinates = str(e)
        try:
            response = coordinates["location"]
        except Exception as e:
            logging.info("User IP: trying to get coordinates - FAIL")
            logging.error(e)
            response = str(e)
        logging.info("User IP: trying to get coordinates - SUCCEED")
        return response


    def get(self):
        response =  requests.get("https://checkip.amazonaws.com")
        user_ip = response.text.strip("\n")
        logging.info("User IP: {}".format(user_ip))
        return {"user_ip": user_ip,
        "localisation": self.get_location(user_ip)}, 200

api.add_resource(UserIP, '/user_ip')
api.add_resource(DataBase, '/get_places/<int:distance>/<string:user_latitude>/<string:user_longitude>')

@app.route('/', methods=['GET', 'POST'])
def home():
   return render_template('home.html')

port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)