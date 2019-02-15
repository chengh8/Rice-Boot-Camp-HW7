# 1. import Flask and other dependencies
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite", echo=False)

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )

@app.route("/api/v1.0/precipitation")
def Precipitation():

    Prcp = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > Start).filter(Measurement.date < Finish).all()

    YearDate = [d[0] for d in Prcp]
    YearPrcp = [p[1] for p in Prcp]

    TripPrcp_df = pd.DataFrame({'date':YearDate,'precipitation':YearPrcp})
    TripPrcp_df.set_index('date',inplace=True)
    df_json = TripPrcp.to_dict(orient='split')
    
    return jsonify(df_json)

@app.route("/api/v1.0/stations")
def Stations():

    Stations = session.query(Station.station, Station.name, Station.latitude,Station.longitude,Station.elevation).statement
    Active_df = pd.read_sql_query(Stations, session.bind)
    Active_df.set_index('station',inplace=True)
    Station_json = Active_df.to_dict(orient='split')

    return jsonify(Station_json)

@app.route("/api/v1.0/tobs")
def Tobs():

    Measure = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > YearBeg).filter(Measurement.date < YearEnd).statement
    Temps = pd.read_sql_query(Measure, session.bind)
    Temps_json = Temps.to_dict(orient='split')

    return jsonify(Temps_json)

if __name__ == "__main__":
    app.run(debug=True)