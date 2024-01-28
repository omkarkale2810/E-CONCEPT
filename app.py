from flask import Flask, render_template, request ,redirect
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__)
app.config['SQLAlCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer , primary_key =True  )
    email = db.Column(db.String(40) , unique=True  )
    name = db.Column(db.String(40) , nullable =False  )
    adharno = db.Column(db.String(12) , nullable =False )
    password = db.Column(db.String(40) , nullable =False )

    def __init_(self,email,password):
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8') , bcrypt.gensalt()).decode('utf-8')


    def check_password(self , password):
        return bcrypt.checkpw(password.encode('utf-8') , self.password.encode('utf-8'))


with app.app_context():
    db.create_all()




@app.route('/')
def Dashboard():
    return 'This is dashboard aaditya making'







# new user detail store in data base

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        email = request.form['email']
        fullname=request.form['fullname']
        adharno = request.form['adharno']
        mobileno = request.form['mobileno']
        password = request.form['password']
        new_user = User(email=email,fullname=fullname,adharno=adharno,mobileno=mobileno,password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('login.html')
    
    return render_template('register.html')  







@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['email']




    return render_template('login.html')  # Corrected the template name

if __name__ == '__main__':
    app.run()
