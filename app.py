import os

from flask import Flask, render_template, request, jsonify
from sqlalchemy import or_, func, tuple_, select,text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
#from sqlalchemy_sample import session



  # Import table definitions.
from models import *

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://xvxsqqqppyqakc:2fe7f4f454a35890a46444ef5cbe43679e7183bb8b484d3177db22a13d47cf5b@ec2-52-87-58-157.compute-1.amazonaws.com:5432/d4ch6pfhdqcgg5"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False




engine = create_engine(os.getenv("DATABASE_URL"))

some_engine = create_engine('postgresql://scott:tiger@localhost/')

# create a configured "Session" class
Session = sessionmaker(bind=engine)

# create a Session
session = Session()

connection = engine.connect()

  # Link the Flask app with the database (no Flask app is actually being run yet).
db.init_app(app)

def main():
    # Create tables based on each table definition in `models`
    db.create_all()

    
def main_2():
   a=Aggregate.query.all()
   b=text("SELECT * FROM aggregatedb")
   c=("SELECT SUM(indicator_value) AS indicator_value,year, indicator_id FROM indicatordb WHERE country_id IN (SELECT country_id FROM aggregatedb WHERE aggregate_isoid = '")
   g=str(23)
   e=("') GROUP BY year,indicator_id ORDER BY indicator_id, year")
   f=c+g+e
   d=text(f)
   result=connection.execute(d)
   rslt=result.fetchall()
   print(rslt)
   return jsonify({
              "origin": flight.origin,
              "destination": flight.destination,
              "duration": flight.duration,
              "passengers": names
          })
   for i in rslt:
       print(i.year)
       print(i.indicator_value)
       print(i.indicator_id)

def main_3():
    region_id=23
    region_id=str(region_id)
    check_aggregate=Aggregate.query.filter(Aggregate.aggregate_isoid==region_id).all()
    lst=[]
    for i in check_aggregate:
        lst.append(i.country_id)

    qry=Indicator.query.with_entities(func.sum(Indicator.indicator_value)).filter(Indicator.country_id.in_(lst)).all()
    #for i in qry:
        #print(i)
 
    #qry=qry.order_by(Indicator.indicator_id, Indicator.year)
    #check_indi = Indicator.query.filter(Indicator.country_id.in_(lst)).order_by(Indicator.year, Indicator.indicator_id).all()
    #print(check_indi)

        
    #lst=tuple(lst)
    #qry = Indicator.query(Indicator.indicator_id).filter(Indicator.country_id.in_(lst))
    #result=qry.all()
    #.order_by(Indicator.year, Indicator.indicator_id).all()
    #print(result)
    #final=Indicator.query.filter(Indicator.country_id.in_(lst)).all()
##    slc = select([func.sum(Indicator.indicator_value), Indicator.year, Indicator.indicator_id].where(Indicator.country_id).\
##                 in_(lst).group_by(Indicator.year, Indicator.indicator_id).order_by(Indicator.indicator_id, Indicator.year))
##    b=db.query(slc).all()
##    print(b)
##    for i in check_aggregate:
##        print(i.country_id)
    



    
@app.route("/")
def hello():
    return "Hello, World!"

if __name__ == "__main__":
    # Allows for command line interaction with Flask application
    with app.app_context():
        main_2()
        print("hello")
