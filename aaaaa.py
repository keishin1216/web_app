
from flask import Flask
from flask import render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
from datetime import time, datetime
import pytz
import os
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tour.db'
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)
app.config['SESSION_TYPE'] = 'sqlalchemy' 
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_KEY_PREFIX'] = 'your_prefix'



login_manager = LoginManager()
login_manager.init_app(app)


class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  user = db.relationship('User', back_populates='posts')
  create_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))
  t = db.Column(db.Float, nullable=False, default=0.0)
  impression = db.Column(db.Integer)
  #impression_data = db.Column(db.List)
  impression_counts = db.Column(db.PickleType, default =  {i: 0 for i in range(1, 11)})
  lat = db.Column(db.Float)
  lon = db.Column(db.Float)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_name = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    posts = db.relationship('Post', back_populates='user', lazy='dynamic')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
      return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        password = request.form.get('password')
        user = User(user_name=user_name, password=generate_password_hash(password, method='sha256'))
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        return redirect('/register/login')
    else:
       return render_template('register.html')


@app.route('/register/login', methods=['GET', 'POST']) 
def login():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        password = request.form.get('password')
        user = User.query.filter_by(user_name=user_name).first()
        #past_time = time.time()
        if check_password_hash(user.password, password):
          login_user(user)
          user_id = user.id
          existing_post = Post.query.filter_by(user_id=user_id, t=0).first()
          if not existing_post:
           t = 0
           first = Post(user_id = user_id, t=t)
           first.create_at = datetime.now(pytz.timezone('Asia/Tokyo'))
           db.session.add(first)
           db.session.commit()
          
          session['user_id'] = user.id
          login_user(user)
          return redirect('/register/login/count')
    else:
       return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST']) 
@login_required
def logout():
    logout_user()
    return redirect('/register/login')

@app.route('/register/login/count', methods=['GET', 'POST']) 
@login_required
def count():
    if request.method == 'GET':
        user = User.query.order_by(User.id.desc()).first()
        user_name = user.user_name
        posts = user.posts.all()
        post = Post.query.order_by(Post.id.desc()).first()
        if post.impression is None:
           return render_template('count.html', user_name=user_name, t = post.t, create_at=post.create_at)
        else:
         return render_template('count.html', user_name=user_name, posts=posts)#, impression_data=post.impression_data)
    elif request.method == 'POST':
        impression_value = int(request.form.get('impression'))
        user_id = session.get('user_id')
        user = User.query.order_by(User.id.desc()).first()
        user_name = user.user_name
        login_post = Post.query.filter_by(t=0).first()
        latest_post = Post.query.order_by(Post.id.desc()).first()
        now = datetime.now(pytz.timezone('Asia/Tokyo'))
        current_time = (now- login_post.create_at.astimezone(pytz.timezone('Asia/Tokyo'))).seconds
        #latest_post.impression_data = impression_data.append(impression_value)
        if latest_post is None:
           impression_counts = {i: 0 for i in range(1, 11)}
           impression_counts[impression_value] += 1
           post = Post(impression=impression_value, impression_counts=impression_counts, create_at=now, t = current_time, user_id=user_id)#, impression_data=latest_post.impression_data)       
        else:
           latest_post.impression_counts[impression_value] += 1
           post = Post(impression=impression_value, impression_counts=latest_post.impression_counts, create_at=now, t = current_time, user_id=user_id)#, impression_data=latest_post.impression_data) 
        db.session.add(post)
        db.session.commit()
        return redirect('/register/login/count/check')

       
@app.route('/register/login/count/check', methods=['GET', 'POST'])
def check():
    post = Post.query.order_by(Post.id.desc()).first() 
    if request.method == 'GET':
        if post.impression is not None:
         return render_template('check.html', impression=post.impression, impression_counts=post.impression_counts, create_at=post.create_at, t=post.t, lat=0, lon=0)
        else: 
         return 'ee'
    else:
       if post.impression is not None:
         lat = request.form.get('latitude')
         lon = request.form.get('longitude')
         if lat and lon is not None: 
          post.lat = lat
          post.lon = lon
          db.session.add(post)
          db.session.commit()
          return render_template('check.html', impression=post.impression, impression_counts=post.impression_counts, create_at=post.create_at, t=post.t, lat=post.lat, lon=post.lon)
       else:
          return 'ee'
       

@app.route('/register/login/count/finish', methods=['GET', 'POST'])
@login_required
def finish():
     if request.method == 'GET':
      user = User.query.order_by(User.id.desc()).first()
      post = Post.query.order_by(Post.id.desc()).first()
      user_name = user.user_name
      impression_counts = post.impression_counts
      db.session.commit()
      return render_template('finish.html', user_name=user_name,impression_counts=impression_counts)


if __name__ == '__main__':
    app.run(#host='0.0.0.0', ssl=('server.crt','server.key'),port=80, debug=True)
    )