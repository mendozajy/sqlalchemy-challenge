# sqlalchemy-challenge 
#Uploaded juypityer notebook, supporting files and app.py file.  The last two questions are partially answered as I couldnt figure out or truly understand the commands/syntax needed.

#Although I have the code written out for the last two question I dont' get what I am doing or referencing.  They remain in draft/# format and the qestions in visual studio code remain partially answered.



@app.route("/api/v1.0/start/<startdate>")
def start(startdate):
    #parsestartdate
    split=startdate.split("-")
    sqlstart=dt.datetime(int(split[2]),int(split[0]),int(split[1]))
    sqlend=dt.datetime(int(split[2]),int(split[0]),(int(split[1])+1))
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """Return the minimum temperature, the average temperature, and the max temperature for a given date"""

# Perform a query to retrieve tempature information
    results=session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
    filter(measurement.date >= sqlstart,measurement.date < sqlend).all()
    session.close()

    # Create a dictionary from the row data and append to a list of all_startdateweather
    all_startdateweather = []
    for LowTempature, HighTempature, AvgTempature in results:
        start_dict = {}
        start_dict["LowTempature"] = LowTempature
        start_dict["HighTempature"] = HighTempature
        start_dict["AVGTempature"] = AvgTempature
        all_startdateweather.append(start_dict)

    return jsonify(all_startdateweather)

@app.route("/api/v1.0/start/<startdate>/end/<enddate>")
def startend(startdate,enddate):
    #parsestartdate
    splitstart=startdate.split("-")
    splitend=enddate.split("-")
    sqlstart=dt.datetime(int(splitstart[2]),int(splitstart[0]),int(splitstart[1]))
    sqlend=dt.datetime(int(splitend[2]),int(splitend[0]),int(splitend[1]))
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return the minimum temperature, the average temperature, and the max temperature for a given date"""
# Perform a query to retrieve tempature information
    results=session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
    filter(measurement.date >= sqlstart, measurement.date <= sqlend)

    session.close()

    # Create a dictionary from the row data and append to a list of all_startdateweather
    all_startenddateweather = []
    for LowTempature, HighTempature, AvgTempature in results:
        startend_dict = {}
        startend_dict["LowTempature"] = LowTempature
        startend_dict["HighTempature"] = HighTempature
        startend_dict["AVGTempature"] = AvgTempature
        all_startenddateweather.append(startend_dict)

    return jsonify(all_startenddateweather)

if __name__ == "__main__":
    app.run(debug=True) 
