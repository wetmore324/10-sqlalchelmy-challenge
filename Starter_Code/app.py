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
engine =  create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

################################################
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
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
        f"Note: to access values between a start and end date enter both dates using format: YYYY-mm-dd/YYYY-mm-dd"
    )

#Create a route that queries precipitation levels and dates and returns a dictionary using date as key and precipitation as value
@app.route("/api/v1.0/precipitation")
def precipitation():

    #Calculate the date one year from the last date in data set.
    start_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    session = Session(engine)

    #Create a new variable to store results from query
    precipitation_results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= start_date).all()
    session.close()
    precipitation_values={date: prcp for date,prcp in precipitation_results}
    return jsonify(precipitation_values)

#Create a route that returns jsonified data of all of the stations in the database
@app.route("/api/v1.0/station")
def station():

    session = Session(engine)

    station_results = session.query(Station.station,Station.name).all()
    session.close()
    station_values={station: name for station,name in station_results}
    return jsonify (station_values)

#Create a route that queries the dates and temp observed for the most active station for the last year of data
@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)
    start_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    active_station= session.query(Measurement.station, func.count(Measurement.station)).\
        order_by(func.count(Measurement.station).desc()).\
        group_by(Measurement.station).first()
    most_active_station = active_station[0]

    # Create query to find list of Temperature Observations (tobs) for the previous year
    tobs_results = session.query(Measurement.date, Measurement.station, Measurement.tobs).filter(Measurement.date >= start_date).filter(Measurement.station == most_active_station).all()
    session.close()

    tobs_last_year_values = []
    for date, tobs, station in tobs_results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_dict["station"] = station
        tobs_last_year_values.append(tobs_dict)   
    return jsonify(tobs_last_year_values)

@app.route("/api/v1.0/<start>")
def start_date(start):

    session = Session(engine)

    # Create query for minimum, average, and max tobs where query date is greater than or equal to the date the user submits in URL
    day_temp_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    session.close()
    daily_temp_values =[]
    for min, avg, max in day_temp_results:
        start_date_dict = {}
        start_date_dict["min"] = min
        start_date_dict["average"] = avg
        start_date_dict["max"] = max
        daily_temp_values.append(start_date_dict)
    
    return jsonify(daily_temp_values)
    
# Create a route that when given the start date only, returns the minimum, average, and maximum temperature observed for all dates greater than or equal to the start date entered by a user
@app.route("/api/v1.0/<start>/<end>")
def Start_end_date(start, end):

    session = Session(engine)

    # Create query for minimum, average, and max tobs where query date is greater than or equal to the start date and less than or equal to end date user submits in URL
    start_end_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()

    # Create a list of min,max,and average temps that will be appended with dictionary values for min, max, and avg tobs queried above
    start_end_values = []
    for min, avg, max in start_end_results:
        start_end_dict = {}
        start_end_dict["min_temp"] = min
        start_end_dict["avg_temp"] = avg
        start_end_dict["max_temp"] = max
        start_end_values.append(start_end_dict) 
    return jsonify(start_end_values)

if __name__ == '__main__':
    app.run(debug=True)