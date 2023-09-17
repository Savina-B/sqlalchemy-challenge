# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# Create an engine and connect to the SQLite database
engine = create_engine("sqlite:///resources/hawaii.sqlite")
connection = engine.connect()

# Reflect the tables
Base = automap_base()
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
def home():
    """List all available routes."""
    return (
        "Available Routes:<br/>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
        "/api/v1.0/start_date<br/>"
        "/api/v1.0/start_date/end_date"
    )

@app.route("/api/v1.0/start_date/<start>")
def get_temperatures_start(start):
    """Return the min, max, and average temperatures from the given start date to the end of the dataset."""

    try:
        # Perform the calculation using the start date
        min_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start).scalar()
        max_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start).scalar()
        avg_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start).scalar()

        # Create a dictionary to hold the results
        result = {
            "start_date": start,
            "end_date": "end of dataset",
            "min_temp": min_temp,
            "max_temp": max_temp,
            "avg_temp": avg_temp
        }

        # Return the result as JSON
        return jsonify(result)
    except Exception as e:
        # Handle exceptions gracefully and return an error response
        return jsonify({"error": str(e)}), 500
    finally:
        # Close the session
        session.close()

@app.route("/api/v1.0/start_date/<start>/end_date/<end>")
def get_temperatures_range(start, end):
    """Return the min, max, and average temperatures from the given start date to the given end date."""

    try:
        # Perform the calculation using the start and end dates
        min_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start, Measurement.date <= end).scalar()
        max_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start, Measurement.date <= end).scalar()
        avg_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start, Measurement.date <= end).scalar()

        # Create a dictionary to hold the results
        result = {
            "start_date": start,
            "end_date": end,
            "min_temp": min_temp,
            "max_temp": max_temp,
            "avg_temp": avg_temp
        }

        # Return the result as JSON
        return jsonify(result)
    except Exception as e:
        # Handle exceptions gracefully and return an error response
        return jsonify({"error": str(e)}), 500
    finally:
        # Close the session
        session.close()

# Run the application
if __name__ == "__main__":
    app.run(debug=True)
