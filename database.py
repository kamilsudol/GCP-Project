import psycopg2
import sqlalchemy
from subprocess import run
import random
import logging


def connection():
    logging.info("Connecting to database")
    from google.cloud.sql.connector import Connector
    connector = Connector()

    INSTANCE_CONNECTION_NAME = f"sabre-gcp-projekt:us-central1:geo-places-sql"
    print(f"Your instance connection name is: {INSTANCE_CONNECTION_NAME}")
    DB_USER = "client"
    DB_PASS = "client"
    DB_NAME = "places"

    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pg8000",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    logging.info("Connecting to database - DONE")
    return conn

def find(db_conn, latitude, longitude, distance):
    logging.info(f"Looking for results using latitude: {latitude}, longitude: {longitude}, distance: {distance}.")
    results = db_conn.execute(f"SELECT * FROM places_table pt WHERE (6371000 * 2 * atan2(sqrt(sin(({latitude}-pt.latitude)*pi()/360) * sin(({latitude}-pt.latitude)*pi()/360) + cos({latitude}*pi()/180) * cos(pt.latitude*pi()/180) * sin(({longitude}-pt.longitude)*pi()/360) * sin(({longitude}-pt.longitude)*pi()/360)), sqrt(1-(sin(({latitude}-pt.latitude)*pi()/360) * sin(({latitude}-pt.latitude)*pi()/360) + cos({latitude}*pi()/180) * cos(pt.latitude*pi()/180) * sin(({longitude}-pt.longitude)*pi()/360) * sin(({longitude}-pt.longitude)*pi()/360))))) < {distance}").fetchall()
    res = []
    for row in results:
        res.append(dict(row))
    logging.info(f"Looking for results using latitude: {latitude}, longitude: {longitude}, distance: {distance} - found {len(res)} result(s).")
    return res

def insert_rows(db_conn):
    types = ["Hotel", "Library", "School", "University", "Restaurant", "Pub", "Shop"]
    names = ["Thomson", "Becky", "Wood", "Brickleberry", "Rick", "Sanchez", "Biden", "Trump", "Donald", "Mickey"]
    # latitude = .0 # -90 to 90
    # longitude = .0 # -180 to 180
    ROWS_TO_BE_GENERATED = 100

    for _ in range(ROWS_TO_BE_GENERATED):

        insert_stmt = sqlalchemy.text(
                "INSERT INTO places_table (place_name, type, latitude, longitude) VALUES (:place_name, :type, :latitude, :longitude)",
            )
        chosen_name = random.choice(names)
        chosen_type = random.choice(types)
        chosen_latitude = random.uniform(-90.0, 90.0)
        chosen_longitude = random.uniform(-180.0, 180.0)
        db_conn.execute(insert_stmt, place_name=chosen_name, type=chosen_type, latitude=chosen_latitude, longitude=chosen_longitude)


def find_places_in_specific_distance(latitude, longitude, distance):
    database_instance = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=connection,
    )
    with database_instance.connect() as db_conn:
        db_conn.execute(
            "CREATE TABLE IF NOT EXISTS places_table "
            "( id SERIAL NOT NULL, place_name VARCHAR(255) NOT NULL, "
            "type VARCHAR(255) NOT NULL, latitude FLOAT NOT NULL, longitude FLOAT NOT NULL, "
            "PRIMARY KEY (id));"
        )
        # insert_rows(db_conn)

        return find(db_conn, latitude, longitude, distance)