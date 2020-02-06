import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///data/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Flask Setup
app = Flask(__name__)
# Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"Search by (single start date) or (start and end date):<br/>"
        f"/api/v1.0/YYYY-MM-DD<br/>"
        f"/api/v1.0/YYYY-MM-DD/YYYY-MM-DD<br/>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a list of all measurements"""
    # Query all measurements
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    # Create a dictionary from the row data
    data_list = []
    for date, prcp in results:
        my_dict = {}
        my_dict[date] = prcp
        data_list.append(my_dict)
    return jsonify(data_list)
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a list of all measurements"""
    # Query all measurements
    results = session.query(Station.station).all()
    session.close()
    return jsonify(list(np.ravel(results)))

@app.route("/api/v1.0/tobs")
def tobservation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a list of all measurements"""
    # Design a query to retrieve the last 12 months of precipitation data and plot the results
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    # Calculate the date 1 year ago from the last data point in the database
    first_date = (pd.to_datetime(last_date) + pd.DateOffset(months=-12)).strftime('%Y-%m-%d')
    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= first_date).all()
    session.close()
    # Create a dictionary from the row data
    data_list = []
    for date, prcp in results:
        my_dict = {}
        my_dict[date] = prcp
        data_list.append(my_dict)
    return jsonify(data_list)
@app.route("/api/v1.0/<start_date>")
def date_start_only(start_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    session.close()
    return jsonify(list(np.ravel(results)))
@app.route("/api/v1.0/<start_date>/<end_date>")
def date_start_end(start_date, end_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    session.close()
    return jsonify(list(np.ravel(results)))

if __name__ == '__main__':
    app.run(debug=True)
