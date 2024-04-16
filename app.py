from collections import UserDict
from flask import Flask, render_template, request,redirect,session,url_for,flash
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from flask_migrate import Migrate
from datetime import datetime
from sqlalchemy.orm import relationship
import os
from flask import request
import uuid
import random


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = 'secret_key'
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), unique=True)
    name = db.Column(db.String(40), nullable=False)
    adharno = db.Column(db.String(12), nullable=False)
    mobileno = db.Column(db.String(10), nullable=False)  
    password = db.Column(db.String(40), nullable=False)
    accountbalance =db.Column(db.Integer ,nullable=False)

    def __init__(self, email, name, adharno, mobileno, password , accountbalance):
        self.email = email
        self.name = name
        self.adharno = adharno
        self.mobileno = mobileno
        self.accountbalance =accountbalance
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    
    def addmoney(email, amount):
        user = User.query.filter_by(email=email).first()
        if user:
            if amount>0:
                user.accountbalance += amount 
                return True
            else:
                return False
        return False
    
    def withdraw(email , amount):
        user = User.query.filter_by(email=session['email']).first()
        if amount < 0 :
            amount=(-1)*amount
            
        if user.accountbalance >= amount:
            user.accountbalance = user.accountbalance - amount 
            return 1
        else:
            return 0
    
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        name=request.form['name']
        adharno = request.form['adharno']
        mobileno = request.form['mobileno']
        password = request.form['password']
        accountbalance = 0
        new_user = User(email=email, name=name, adharno=adharno, mobileno=mobileno, password=password , accountbalance= accountbalance)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
    
    return render_template('register.html')  

@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None  
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['email'] = user.email
            return redirect('/choose')
        else:
            error_message = "Invalid email or password." 
    return render_template('login.html', error=error_message)


@app.route('/choose', methods=['GET', 'POST'])
def choose():
    if 'email' in session:
        return render_template('choose.html')
    else:
        return redirect('/login')

class Station(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stationname = db.Column(db.String(80), unique =True ,nullable=False)
    bikes = db.relationship('Bikes', backref='station', lazy=True)

    def __init__(self, stationname):
        self.stationname = stationname

    def __repr__(self):
        return f'<Station {self.stationname}>'

with app.app_context():
    db.create_all()

class Bikes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    numberofbikes = db.Column(db.Integer, nullable=False)
    station_id = db.Column(db.Integer, db.ForeignKey('station.id'), nullable=False)


    def __init__(self, name, price, numberofbikes,station_id):
        self.name = name
        self.price = price
        self.numberofbikes = numberofbikes
        self.station_id = station_id

    def __repr__(self):
        return f'<Bikes {self.name}>'

with app.app_context():
    db.create_all()


def get_station_by_id(station_id):
    station = Station.query.filter_by(id=station_id).first()
    return station


def initialize_bikes():
    stations_data = [
        {'name': 'Swargate', 'bikes': [
            {'name': 'Ather 450X', 'price': 50, 'numberofbikes': 5, 'image': 'photo'},
            {'name': 'Ola S1 Pro', 'price': 60, 'numberofbikes': 8, 'image': 'photo'},
            {'name': 'TVS X Electric', 'price': 70, 'numberofbikes': 10, 'image': 'photo'},
            {'name': 'ONE Electric Kridn', 'price': 80, 'numberofbikes': 3, 'image': 'photo'},
            {'name': 'ABZO VS1', 'price': 90, 'numberofbikes': 6, 'image': 'photo'},
        ]},
        {'name': 'HADAPSAR', 'bikes': [
            {'name': 'Ather 450X', 'price': 50, 'numberofbikes': 5, 'image': 'photo'},
            {'name': 'Ola S1 Pro', 'price': 60, 'numberofbikes': 8, 'image': 'photo'},
            {'name': 'TVS X Electric', 'price': 70, 'numberofbikes': 10, 'image': 'photo'},
            {'name': 'ONE Electric Kridn', 'price': 80, 'numberofbikes': 3, 'image': 'photo'},
            {'name': 'ABZO VS1', 'price': 90, 'numberofbikes': 6, 'image': 'photo'},
        ]},
        {'name': 'COEP HOSTEL', 'bikes': [
            {'name': 'Ather 450X', 'price': 50, 'numberofbikes': 5, 'image': 'photo'},
            {'name': 'Ola S1 Pro', 'price': 60, 'numberofbikes': 8, 'image': 'photo'},
            {'name': 'TVS X Electric', 'price': 70, 'numberofbikes': 10, 'image': 'photo'},
            {'name': 'ONE Electric Kridn', 'price': 80, 'numberofbikes': 3, 'image': 'photo'},
            {'name': 'ABZO VS1', 'price': 90, 'numberofbikes': 6, 'image': 'photo'},
        ]},
        {'name': 'KHARADI', 'bikes': [
            {'name': 'Ather 450X', 'price': 50, 'numberofbikes': 5, 'image': 'photo'},
            {'name': 'Ola S1 Pro', 'price': 60, 'numberofbikes': 8, 'image': 'photo'},
            {'name': 'TVS X Electric', 'price': 70, 'numberofbikes': 10, 'image': 'photo'},
            {'name': 'ONE Electric Kridn', 'price': 80, 'numberofbikes': 3, 'image': 'photo'},
            {'name': 'ABZO VS1', 'price': 90, 'numberofbikes': 6, 'image': 'photo'},
        ]},
        {'name': 'KHADKI', 'bikes': [
            {'name': 'Ather 450X', 'price': 50, 'numberofbikes': 5, 'image': 'photo'},
            {'name': 'Ola S1 Pro', 'price': 60, 'numberofbikes': 8, 'image': 'photo'},
            {'name': 'TVS X Electric', 'price': 70, 'numberofbikes': 10, 'image': 'photo'},
            {'name': 'ONE Electric Kridn', 'price': 80, 'numberofbikes': 3, 'image': 'photo'},
            {'name': 'ABZO VS1', 'price': 90, 'numberofbikes': 6, 'image': 'photo'},
        ]},
        {'name': 'AUNDH', 'bikes': [
            {'name': 'Ather 450X', 'price': 50, 'numberofbikes': 5, 'image': 'photo'},
            {'name': 'Ola S1 Pro', 'price': 60, 'numberofbikes': 8, 'image': 'photo'},
            {'name': 'TVS X Electric', 'price': 70, 'numberofbikes': 10, 'image': 'photo'},
            {'name': 'ONE Electric Kridn', 'price': 80, 'numberofbikes': 3, 'image': 'photo'},
            {'name': 'ABZO VS1', 'price': 90, 'numberofbikes': 6, 'image': 'photo'},
        ]},
        {'name': 'PASHAN', 'bikes': [
            {'name': 'Ather 450X', 'price': 50, 'numberofbikes': 5, 'image': 'photo'},
            {'name': 'Ola S1 Pro', 'price': 60, 'numberofbikes': 8, 'image': 'photo'},
            {'name': 'TVS X Electric', 'price': 70, 'numberofbikes': 10, 'image': 'photo'},
            {'name': 'ONE Electric Kridn', 'price': 80, 'numberofbikes': 3, 'image': 'photo'},
            {'name': 'ABZO VS1', 'price': 90, 'numberofbikes': 6, 'image': 'photo'},
        ]},
        {'name': 'AUNDH', 'bikes': [
            {'name': 'Ather 450X', 'price': 50, 'numberofbikes': 5, 'image': 'photo'},
            {'name': 'Ola S1 Pro', 'price': 60, 'numberofbikes': 8, 'image': 'photo'},
            {'name': 'TVS X Electric', 'price': 70, 'numberofbikes': 10, 'image': 'photo'},
            {'name': 'ONE Electric Kridn', 'price': 80, 'numberofbikes': 3, 'image': 'photo'},
            {'name': 'ABZO VS1', 'price': 90, 'numberofbikes': 6, 'image': 'photo'},
        ]},
        {'name': 'KATRAJ', 'bikes': [
            {'name': 'Ather 450X', 'price': 50, 'numberofbikes': 5, 'image': 'photo'},
            {'name': 'Ola S1 Pro', 'price': 60, 'numberofbikes': 8, 'image': 'photo'},
            {'name': 'TVS X Electric', 'price': 70, 'numberofbikes': 10, 'image': 'photo'},
            {'name': 'ONE Electric Kridn', 'price': 80, 'numberofbikes': 3, 'image': 'photo'},
            {'name': 'ABZO VS1', 'price': 90, 'numberofbikes': 6, 'image': 'photo'},
        ]},
        {'name': 'WARJE', 'bikes': [
            {'name': 'Ather 450X', 'price': 50, 'numberofbikes': 5, 'image': 'photo'},
            {'name': 'Ola S1 Pro', 'price': 60, 'numberofbikes': 8, 'image': 'photo'},
            {'name': 'TVS X Electric', 'price': 70, 'numberofbikes': 10, 'image': 'photo'},
            {'name': 'ONE Electric Kridn', 'price': 80, 'numberofbikes': 3, 'image': 'photo'},
            {'name': 'ABZO VS1', 'price': 90, 'numberofbikes': 6, 'image': 'photo'},
        ]},
    ]
    
    for station_data in stations_data:
        existing_station = Station.query.filter_by(stationname=station_data['name']).first()

        if not existing_station:
            station = Station(stationname=station_data['name'])
            db.session.add(station)
            db.session.commit()

            for bike_data in station_data['bikes']:
                bike = Bikes(name=bike_data['name'], price=bike_data['price'], numberofbikes=bike_data['numberofbikes'], station_id=station.id)
                db.session.add(bike)
                db.session.commit()

with app.app_context():
    db.create_all()
    initialize_bikes()


@app.route('/bikes')
def display_bikes():
    bikes = Bikes.query.all()
    return render_template('bikes.html', bikes=bikes)
      

@app.route('/dashboard')
def dashboard():
    if 'email' in session:
        user = User.query.filter_by(email=session['email']).first()
        statio = Station.query.all()
        stations = [
    {"id" : 3 ,"name": "COEP HOSTEL", "lat": 18.5286, "lon": 73.8519, "details": "16"},
    {"id" : 2 ,"name": "HADAPSAR", "lat": 18.500793, "lon": 73.937902, "details": "15"},
    {"id" : 1 ,"name": "SWARGATE", "lat": 18.499925, "lon": 73.858591, "details": "13"},
    {"id" : 4 ,"name": "KHARADI", "lat": 18.552356, "lon": 73.936539, "details": "14"},
    {"id" : 5 ,"name": "KHADKI", "lat": 18.563510, "lon": 73.851512, "details": "18"},
    {"id" : 6 ,"name": "AUNDH", "lat": 18.560218, "lon": 73.809171, "details": "15"},
    {"id" : 7 ,"name": "PASHAN", "lat": 18.538216, "lon": 73.794843, "details": "16"},
    {"id" : 9 ,"name": "WARJE", "lat": 18.480878, "lon": 73.802130, "details": "17"},
    {"id" : 8 ,"name": "KATRAJ", "lat": 18.452709, "lon": 73.858644, "details": "12"}
]
        return render_template('dashboard.html', user=user, stations=stations)
    return redirect('/login')


@app.route('/rentoutdashboard')
def rentoutdashboard():
    if 'email' in session:
        user = User.query.filter_by(email=session['email']).first()
        statio = Station.query.all()
        stations = [
    {"id" : 3 ,"name": "COEP HOSTEL", "lat": 18.5286, "lon": 73.8519, "details": "7"},
    {"id" : 2 ,"name": "HADAPSAR", "lat": 18.500793, "lon": 73.937902, "details": "5"},
    {"id" : 1 ,"name": "SWARGATE", "lat": 18.499925, "lon": 73.858591, "details": "7"},
    {"id" : 4 ,"name": "KHARADI", "lat": 18.552356, "lon": 73.936539, "details": "7"},
    {"id" : 5 ,"name": "KHADKI", "lat": 18.563510, "lon": 73.851512, "details": "7"},
    {"id" : 6 ,"name": "AUNDH", "lat": 18.560218, "lon": 73.809171, "details": "7"},
    {"id" : 7 ,"name": "PASHAN", "lat": 18.538216, "lon": 73.794843, "details": "7"},
    {"id" : 9 ,"name": "WARJE", "lat": 18.480878, "lon": 73.802130, "details": "7"},
    {"id" : 8 ,"name": "KATRAJ", "lat": 18.452709, "lon": 73.858644, "details": "7"}

]
        return render_template('rentoutdashboard.html', user=user, stations=stations)
    return redirect('/login') 


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))


@app.route('/add_funds', methods=['POST'])
def add_funds():
    if 'email' in session:
        amount = int(request.form['amount']) 
        User.addmoney(session['email'], amount)
        db.session.commit()
        return redirect('/userwallet')
    else:
        return redirect('/dashboard')
    
@app.route('/withdraw_funds', methods=['POST'])
def withdraw_funds():
    if 'email' in session:
        amount = int(request.form['amount'])
        result = User.withdraw(session['email'], amount)
        if result == 1:
            db.session.commit()
            return redirect('/userwallet')
        else:
            return render_template('userwallet.html', error='Insufficient Balance')
    else:
        return redirect('login.html')
@app.route('/bikes', methods=['GET', 'POST'])
def manage_bikes():
    if request.method == 'POST':
        if 'email' in session:
            user = User.query.filter_by(email=session['email']).first()
            station_id = int(request.form['stationid'])
            rent_amount = int(request.form['amountofrent'])
            bike_id = int(request.form['bikeid'])  
            duration = int(request.form['duration'])
            bike = Bikes.query.get(bike_id)

            # Calculate the rent amount based on duration
            rent_amount = duration*rent_amount

            if user.accountbalance >= rent_amount and bike.numberofbikes > 0:
                user.accountbalance -= rent_amount
                bike.numberofbikes -= 1
                otp = str(random.randint(100000, 999999))
                session['otp'] = otp  
                db.session.commit()
                
                if bike.numberofbikes == 0:
                    db.session.delete(bike)
                    db.session.commit()
            
                    station = Station.query.get(bike.station_id)
                    bikes_photos_dir = os.path.join(app.static_folder, 'bike_photos', station.stationname)
                    if os.path.exists(bikes_photos_dir):
                        for filename in os.listdir(bikes_photos_dir):
                            if filename.startswith(f"bike_{bike_id}.jpg"):
                                os.remove(os.path.join(bikes_photos_dir, filename))
                
                print("Funds withdrawn successfully. Bike rented.")
                return render_template('successfullrented.html',  otp=session['otp'])
            else:
                station = Station.query.get(station_id)
                bikes_in_station = Bikes.query.filter_by(station_id=station_id).all()

                
                bikes_photos_dir = os.path.join(app.static_folder, 'bike_photos', station.stationname)

                if not os.path.exists(bikes_photos_dir):
                    os.makedirs(bikes_photos_dir)

                total_num_images = len([name for name in os.listdir(bikes_photos_dir) if os.path.isfile(os.path.join(bikes_photos_dir, name))])
              
                return render_template('bikes.html', station=station, bikes=bikes_in_station, total_num_images=total_num_images, bikes_photos_dir=bikes_photos_dir)
        else:
            return redirect('login.html')
    else:
        station_id = request.args.get('stationid')
        station = Station.query.get(station_id)
        bikes_in_station = Bikes.query.filter_by(station_id=station_id).all()

        
        bikes_photos_dir = os.path.join(app.static_folder, 'bike_photos', station.stationname)

        
        if not os.path.exists(bikes_photos_dir):
            os.makedirs(bikes_photos_dir)

        total_num_images = len([name for name in os.listdir(bikes_photos_dir) if os.path.isfile(os.path.join(bikes_photos_dir, name))])

        
        return render_template('bikes.html', station=station, bikes=bikes_in_station, total_num_images=total_num_images, bikes_photos_dir=bikes_photos_dir)



@app.route('/dashboard/station/<int:station_id>', methods=['GET'])
def station_details(station_id):
   
    station = Station.query.get(station_id)
    bikes_in_station = Bikes.query.filter_by(station_id=station_id).all()

   
    bikes_photos_dir = os.path.join(app.static_folder, 'bike_photos', station.stationname)

   
    if not os.path.exists(bikes_photos_dir):
        os.makedirs(bikes_photos_dir)

    total_num_images = len([name for name in os.listdir(bikes_photos_dir) if os.path.isfile(os.path.join(bikes_photos_dir, name))])

    
    return render_template('bikes.html', station=station, bikes=bikes_in_station, total_num_images=total_num_images, bikes_photos_dir=bikes_photos_dir)

@app.route('/userdetail', methods=['GET', 'POST'])
def userdetail():
    user = User.query.filter_by(email=session['email']).first()
    return render_template('userdetail.html', user=user)

@app.route('/userwallet', methods=['GET', 'POST'])
def userwallet():
    user = User.query.filter_by(email=session['email']).first()
    return render_template('userwallet.html', user=user)

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')




class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), unique=True) 
    password = db.Column(db.String(40), nullable=False)
    accountbalance =db.Column(db.Integer ,nullable=False)

    def __init__(self, email,password , accountbalance):
        self.email = email
        self.accountbalance =accountbalance
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    
with app.app_context():
    db.create_all()    


@app.route('/adminregister', methods=['GET', 'POST'])
def adminregister():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        accountbalance = 0
        new_user = Admin(email=email, password=password , accountbalance= accountbalance)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/adminlogin')
    return render_template('adminregister.html')  

@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = Admin.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['email']=user.email
            return redirect('/admindashboard') 
        else:
            return render_template('adminlogin.html',error='Invalid User')
        
    return render_template('adminlogin.html')  

@app.route('/admindashboard')
def admindashboard():
    if 'email' in session:
        admin = Admin.query.filter_by(email=session['email']).first()
        if admin:
            users = User.query.all()
            stations = Station.query.all()
            rental_reqs = Rentalrequest.query.all()
            return render_template('admindashboard.html', rental_reqs=rental_reqs, admin=admin, stations=stations, users=users)
        else:
            return redirect(url_for('adminlogin', message="Admin not found. Please log in."))
    else:
        return render_template('adminlogin.html')
    


class Rentalrequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    vehicle_name = db.Column(db.String(100), nullable=False)
    vehicle_number = db.Column(db.String(20), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='Pending')
    timestamp = db.Column(db.DateTime, default=datetime.now)
    station_id = db.Column(db.Integer, db.ForeignKey('station.id'))
    station = relationship('Station', backref='rental_requests')
    bike_photo_path = db.Column(db.String(255))  



    def __init__(self, user_id, vehicle_name, vehicle_number, duration, status, station_id, bike_photo_path):
        self.user_id = user_id
        self.vehicle_name = vehicle_name
        self.vehicle_number = vehicle_number
        self.duration = duration
        self.status = status
        self.station_id = station_id
        self.bike_photo_path = bike_photo_path

with app.app_context():
    db.create_all()

def save_bike_photo(photo , station_id):

    station = Station.query.filter_by(id=station_id).first()
    station_name = station.stationname
    photo_dir = os.path.join('static', 'bike_photos', station_name)

    if not os.path.exists(photo_dir):
        os.makedirs(photo_dir)

    filename = f"bike_{uuid.uuid4().hex}.jpg"  

    
    photo_path = os.path.join(photo_dir, filename)
    photo.save(photo_path)


    return f"/{photo_path}"




@app.route('/approve_rental', methods=['POST'])
def approve_rental():
    request_id = request.form['request_id']
    rental_request = Rentalrequest.query.get(request_id)
    rating = request.form.get('rating')

    if rental_request:
        station = Station.query.get(rental_request.station_id)
        station_name = station.stationname
        bike_count = Bikes.query.filter_by(station_id=rental_request.station_id).count()
        new_filename = f"bike_{bike_count + 1}.jpg"   
        old_path = os.path.join(app.root_path, 'static', 'bike_photos', station_name , os.path.basename(rental_request.bike_photo_path)) 
        new_path = os.path.join(app.root_path, 'static', 'bike_photos', station_name, new_filename)  
        if os.path.exists(old_path):
    
            os.rename(old_path, new_path)

   
            rental_request.bike_photo_path = f"/static/bike_photos/{station_name}/{new_filename}"
        else:
   
            print("Error: The file to be renamed does not exist.")
        
        price = int(rating) * 60
        
        user = User.query.get(rental_request.user_id)
        user.accountbalance += price 

        price = int(rating) * 20



        new_bike = Bikes(name=rental_request.vehicle_name, price=price, numberofbikes=1, station_id=rental_request.station_id)
        db.session.add(new_bike)
        
        rental_request.status = 'Approved'
        db.session.commit()
        db.session.delete(rental_request)
        db.session.commit()

        return redirect(url_for('admindashboard')) 
    else:
        return "Rental request not found", 404


@app.route('/decline_rental', methods=['POST'])
def decline_rental():
    request_id = request.form['request_id']
    rental_request = Rentalrequest.query.get(request_id)

    if rental_request:
       
        if rental_request.bike_photo_path:
            photo_path = os.path.join(app.root_path, rental_request.bike_photo_path)
            if os.path.exists(photo_path):
                os.remove(photo_path)


        db.session.delete(rental_request)
        db.session.commit()

        return redirect(url_for('admindashboard'))  
    else:
        return "Rental request not found", 404



@app.route('/rentout_bike', methods=['POST'])
def rentout_bike():
    if 'email' in session:
        user = User.query.filter_by(email=session['email']).first()
        vehicle_name = request.form['vehicle_name']
        vehicle_number = request.form['vehicle_number']
        station_id = request.form['station_id']
        duration = request.form['duration']
        bike_photo = request.files['bike_photo']

        rating = request.form.get('rating')

        bike_photo_path = save_bike_photo(bike_photo , station_id)

        new_rental_request = Rentalrequest(
            user_id=user.id,
            vehicle_name=vehicle_name,
            vehicle_number=vehicle_number,
            duration=duration,
            status='Pending',
            station_id=station_id,               
            bike_photo_path=bike_photo_path
            )

        db.session.add(new_rental_request)
        db.session.commit()

        return render_template('rentrequest.html')
    else:
        return redirect('login.html')

@app.route('/adminlogout', methods=['GET', 'POST'])
def adminlogout():
    session.pop('email', None)
    return redirect(url_for('index'))    

if __name__ == '__main__':
    app.run(debug=True)


