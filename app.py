import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_

from flask import Flask, jsonify


engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precip():
    session = Session(engine)
    
    s = session.query(Measurement.date,func.avg(Measurement.prcp)).\
        order_by(Measurement.date.desc()).group_by(Measurement.date).limit(365).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(s))

    return jsonify(all_names)

@app.route("/api/v1.0/stations")
def stat():
    session = Session(engine)
    
    st = session.query(Measurement.station).group_by(Measurement.station).\
    order_by(func.count(Measurement.station).desc()).all()
    
    session.close()
    
    return jsonify(list(np.ravel(st)))

@app.route("/api/v1.0/tobs")
def tob():
    session = Session(engine)
    
    high_station = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).limit(1).all()

    high_station
    
    t = session.query(Measurement.tobs).filter(Measurement.station == high_station[0][0]).\
        order_by(Measurement.date.desc()).limit(365).all()
    
    session.close()
    
    return jsonify(list(np.ravel(t)))

@app.route("/api/v1.0/<start>")
def begin(start):
    session = Session(engine)
    
    avg = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    maxi = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    mini = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start).all()
    
    x = jsonify(average=avg[0][0], maximum=maxi[0][0], minimum=mini[0][0])
    
    session.close()
    
    #I could only return the json, not all of the values indicdually
#    return(f"The average is: {avg[0][0]}</br>The maximum is: {maxi[0][0]}<br/>The minimum is: {mini[0][0]}")
    return(x)

@app.route("/api/v1.0/<start>/<end>")
def end(start, end):
    session = Session(engine)

    avg = session.query(func.avg(Measurement.tobs)).filter(and_(start<= Measurement.date, Measurement.date <=end)).all()
    maxi = session.query(func.max(Measurement.tobs)).filter(and_(start<= Measurement.date, Measurement.date <=end)).all()
    mini = session.query(func.min(Measurement.tobs)).filter(and_(start<= Measurement.date, Measurement.date <=end)).all()
    
    alls = session.query(func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).\
    filter(and_(start<= Measurement.date, Measurement.date <=end)).all()
    
    x = jsonify(average=avg[0][0], maximum=maxi[0][0], minimum=mini[0][0])
    
    session.close()
#    return jsonify(average=avg[0][0], maximum=maxi[0][0], minimum=mini[0][0])
#    return(f"{x}, The average is: {avg[0][0]} </br>The maximum is: {maxi[0][0]}<br/>The minimum is: {mini[0][0]}<br/>")
    return(x)
    






if __name__ == '__main__':
    app.run(debug=True)