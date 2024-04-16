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
    bike_photo_path = db.Column(db.String(255))  # Add this column
    # Define your relationships here


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
# Adjusting save_bike_photo method to save photos within the static folder
def save_bike_photo(photo):
    """
    Save the bike photo to a location within the static folder and return the path to the photo.
    """
    # Define the directory where photos will be stored within the static folder
    photo_dir = os.path.join('static', 'bike_photos')
    if not os.path.exists(photo_dir):
        os.makedirs(photo_dir)

    # Generate a unique filename for the photo
    filename = f"bike_{uuid.uuid4().hex}.jpg"  # Assuming the photo is in JPEG format

    # Save the photo to the directory
    photo_path = os.path.join(photo_dir, filename)
    photo.save(photo_path)

    # Return the path to the photo
    return photo_path


# Adjusting approve_rental function to handle approval of rental requests
@app.route('/approve_rental', methods=['POST'])
def approve_rental():
    request_id = request.form['request_id']
    rental_request = Rentalrequest.query.get(request_id)

    if rental_request:
        # Add bike data to the bikes database
        new_bike = Bikes(name=rental_request.vehicle_name, price=0, numberofbikes=1, station_id=rental_request.station_id)
        db.session.add(new_bike)
        
        rental_request.status = 'Approved'
        db.session.commit()

        return redirect(url_for('admindashboard'))  # Redirect back to admin dashboard  
    else:
        return "Rental request not found", 404

# Adjusting decline_rental function to handle declining of rental requests
@app.route('/decline_rental', methods=['POST'])
def decline_rental():
    request_id = request.form['request_id']
    rental_request = Rentalrequest.query.get(request_id)

    if rental_request:
        # Remove the bike photo if it exists
        if rental_request.bike_photo_path:
            photo_path = os.path.join(app.root_path, rental_request.bike_photo_path)
            if os.path.exists(photo_path):
                os.remove(photo_path)

        # Delete the rental request from the database
        db.session.delete(rental_request)
        db.session.commit()

        return redirect(url_for('admindashboard'))  # Redirect back to admin dashboard
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

            # Save the bike photo and obtain the path
        bike_photo_path = save_bike_photo(bike_photo)

            # Create a new Rentalrequest instance
        new_rental_request = Rentalrequest(
            user_id=user.id,
            vehicle_name=vehicle_name,
            vehicle_number=vehicle_number,
            duration=duration,
            status='Pending',
            station_id=station_id,               
            bike_photo_path=bike_photo_path
            )

            # Add the new rental request to the database
        db.session.add(new_rental_request)
        db.session.commit()

            # Redirect or render a response
            # You can redirect to a success page or render a template
        return render_template('rentrequest.html')
    else:
        return redirect('login.html')