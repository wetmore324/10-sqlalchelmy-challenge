# Import the dependencies.
import numpy as np

import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start"
        f"/api/v1.0/start/end<br/>"
        f"Note: to access values between a start and end date enter both dates using format: YYYY-mm-dd/YYYY-mm-dd"
    )

#Create a route that queries precipitation levels and dates and returns a dictionary using date as key and precipitation as value
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    """Return a list of precipitation (prcp) and date (date) data"""

    #Create a new variable to store results from query
    precipitation_results = session.query(Measurement.prcp, Measurement.date).all()
    session.close()

    #Create a dictionary

    precipitation_values = []
    for prcp, date in precipitation_results:
        precipitation_dict = []
        precipitation_dict["precipitation"] = prcp
        precipitation_dict["date"] = date
        precipitation_values.append(precipitation_dict)
    return jsonify(precipitation_values)

#Create a route that returns jsonified data of all of the stations in the database
@app.route("/api/v1.0/station")
def station():

    session = Session(engine)

    """Return a list of stations from the database"""

    station_results = session.query(Station.station,Station.id).all()

    session.close()

    station_values = []
    for station, id in station_results:
        station_values_dict = {}
        station_values_dict['station'] = station
        station_values_dict['id'] = id
        station_values.append(station_values_dict)
    return jsonify (station_values)

#Create a route that queries the dates and temp observed for the most active station for the last year of data and returns a JSON list of the temps observed for the last year
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    """Return a list of dates and temps ovserved for the most active station from the last year of data from the database"""
    #Create query to find the last date in the database

    last_year_results = session.query(Measurement.date).\
        order_by(Measurement.date.desc()).first()
    
     # Create query_start_date by finding the difference between date time object of "2017-08-23" - 365 days
    query_start_date = dt.date(2017, 8, 23)-dt.timedelta(days =365) 
    print(query_start_date) 
    # returns: 2016-08-23 

    # Create query to find most active station in the database 

    active_station= session.query(Measurement.station, func.count(Measurement.station)).\
        order_by(func.count(Measurement.station).desc()).\
        group_by(Measurement.station).first()
    most_active_station = active_station[0] 

    session.close()


