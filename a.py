from flask import Flask, request,  jsonify, render_template, redirect, session
from flask_sqlalchemy import SQLAlchemy
import pytz
from datetime import time, datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aa.db'
db = SQLAlchemy(app)
app.secret_key = 'your_secret_key'

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_name = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)

class Location(db.Model):
      create_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))
      t = db.Column(db.Float, nullable=False, default=0.0)
      impression = db.Column(db.Integer)
      impression_counts = db.Column(db.PickleType, default =  {i: 0 for i in range(1, 11)})
      id = db.Column(db.Integer, primary_key=True)
      lat = db.Column(db.Float)
      lon = db.Column(db.Float)

@app.route('/register/save_location/aa', methods=['GET', 'POST'])
def aa():
        l = Location.query.order_by(Location.id.desc()).first() 
        ll = Location.query.all()
        if l is not None:
         return render_template('aa.html', lat=l.lat, lon=l.lon, Locations=ll)
        else: 
         return ('ee')
        

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        password = request.form.get('password')
        return redirect('/register/save_location')
    else:
       return render_template('register.html')

@app.route('/register/save_location', methods= ['GET', 'POST'])
def save_location():
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    

    
    if request.method == 'POST':
        impression_value = request.form.get('impression')
        if impression_value is None:
           l = Location(lat=latitude, lon=longitude)  
           db.session.add(l)
           db.session.commit()
           return render_template('location.html'.)
        else:
            latest_post = Location.query.order_by(Location.id.desc()).first()
            if latest_post. impression_counts is None:
             latest_post.impression_counts = {i: 0 for i in range(1, 11)}
             impression_counts[int(impression_value)] += 1
             post = Location(impression=int(impression_value), impression_counts=impression_counts, create_at=now, lat=latitude, lon=longitude)     
       
            latest_post.impression_counts[int(impression_value)] += 1
            now = datetime.now(pytz.timezone('Asia/Tokyo'))
            post = Location(impression=int(impression_value), impression_counts=latest_post.impression_counts, create_at=now,lat=latitude, lon=longitude)
            db.session.add(post)
            db.session.commit()
            session['impression'] = int(impression_value)
            return render_template('location.html', lat=latitude, lon=longitude)
    else:
      return render_template('location.html', lat=0, lon=0)  

if __name__ == '__main__':
   app.run()