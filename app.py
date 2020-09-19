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
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)
# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station
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
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/<startdate>/end/<enddate>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return Percipitation from 8/23/16 to 8/23/17"""
    # Filter Data in the measurement table  going back one year from the newest date
    date = dt.datetime(2016, 8, 23)

# Perform a query to retrieve the data and precipitation scores
    lastyear=session.query(measurement.date, measurement.prcp).\
    filter(measurement.date > date).\
    order_by(measurement.date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_precipitation
    #flask returns data in a list format
    all_precipitation = []
    for date, prcp in lastyear:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    stations = session.query(measurement.station).distinct().all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    #flask returns data in a list format
    all_stations = []
    for name in stations:
        stations_dict = {}
        stations_dict["station ID"] = name

        all_stations.append(stations_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    date = dt.datetime(2016, 8, 23)
    session = Session(engine)
    station = Base.classes.station
    last12 = session.query(station.name, func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
    filter(measurement.station==station.station, measurement.station=="USC00519281", measurement.date >=date)

    session.close()

    all_tobs = []
    for station, lowtemp, hightemp, avgtemp in last12:
        tobs_dict = {}
        tobs_dict["station"] = station
        tobs_dict["lowtemp"] = lowtemp
        tobs_dict["hightemp"] = hightemp
        tobs_dict["avgtemp"] = avgtemp
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

    #@app.route("/api/v1.0/start/<startdate>")
    #def start(startdate):
    #Create our session (link) from Python to the DB
    #session = Session(engine)

    # Perform a query to retrieve tempature information
    #results=session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
    #filter()
    #session.close()
    # Create a dictionary from the row data and append to a list of all_startdateweather
    #all_startdateweather = []
    #for LowTempature, HighTempature, AvgTempature in results:
        #start_dict = {}
    #return jsonify(all_startdateweather)

    #@app.route("/api/v1.0/start/<startdate>/end/<enddate>")
    #def startend(startdate,enddate):
    # Create our session (link) from Python to the DB
    #session = Session(engine)
    #"""Return the minimum temperature, the average temperature, and the max temperature for a given date"""
    # Perform a query to retrieve tempature information
    #results=session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
    #filter()
    # session.close()

    # Create a dictionary from the row data and append to a list of all_startdateweather
    #all_startenddateweather = []
    #for LowTempature, HighTempature, AvgTempature in results:
        #startend_dict = {}
   #return jsonify(all_startenddateweather)

if __name__ == '__main__':
    app.run(debug=True)