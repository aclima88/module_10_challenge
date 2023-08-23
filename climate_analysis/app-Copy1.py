# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import func
import datetime as dt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

# reflect the tables
measurement = Base.classes.measurement
station = Base.classes.station

# Save references to each table
# Create our session (link) from Python to the DB
Session = sessionmaker(bind=engine)
session = Session()

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
# Define the homepage route
@app.route("/")
def homepage():
    return (
        "Welcome to my Climate Analysis API!<br/>"
        "Available Routes:<br/>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
        "/api/v1.0/<start>"
        "/api/v1.0/<start>/<end>"
    )

    # Define the /api/v1.0/precipitation route
    @app.route("/api/v1.0/precipitation")
    def precipitation():
        # Returns json with the date as the key and the value as the precipitation
        # Only returns the jsonified precipitation data for the last year in the database
        year_ago = dt.date.today() - dt.timedelta(days=365)
        temps = session.query(measurement.date, measurement.prcp).filter(measurement.date >= year_ago).all()
        temps_dict = dict(temps)
        return jsonify(temps_dict)

    # Define the /api/v1.0/stations route
    @app.route("/api/v1.0/stations")
    def stations():
        # Returns jsonified data of all of the stations in the database
        stations = session.query(station).all()
        stations_list = list(stations)
        stations_json = jsonify(stations_list)
        return stations_json

    # Define the /api/v1.0/tobs route
    @app.route("/api/v1.0/tobs")
    def tobs():
        # Returns jsonified data for the most active station (USC00519281)
        # Only returns the jsonified data for the last year of data
        year_ago = dt.date.today() - dt.timedelta(days=365)
        most_active_station = session.query(station.name).filter(station.station == "USC00519281").first()
        temps = session.query(measurement.date, measurement.tobs).filter(measurement.station == most_active_station.station).filter(
            measurement.date >= year_ago
        ).all()
        temps_dict = dict(temps)
        return jsonify(temps_dict)

    # Define the /api/v1.0/<start> and /api/v1.0/<start>/<end> routes
    @app.route("/api/v1.0/<start>")
    def temp_range(start):
        # temperature range route code
        start_date = dt.datetime.strptime(start, "%Y-%m-%d")
        temps = session.query(measurement.tobs).filter(measurement.date >= start_date).all()
        temps_list = list(temps)
        temps_json = jsonify(temps_list)
        return temps_json

if __name__ == '__main__':
    app.run(debug=True)
