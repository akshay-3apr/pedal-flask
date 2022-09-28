# login imports
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash,check_password_hash
from hashlib import md5
from app import login,bikerental
import logging,os

# database imports
from app import db

# miscellaneous
from datetime import datetime
from sqlalchemy import exc

@login.user_loader
def load_user(id):
    return Users.query.get(int(id))

class Users(UserMixin,db.Model):
    id = db.Column(db.Integer,index=True,primary_key=True,autoincrement="auto")
    username = db.Column(db.String(64), index=True, unique=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(120), index=True, unique=True)
    phonenumber  =  db.Column(db.String(120), index=True, unique=True)
    address = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(120))

    def __repr__(self):
        return '<Customer id:{0} username:{1} email:{2} phonenumber:{3} password:{4} role:{5}>'.format(self.id,self.username,self.email,self.phonenumber,self.password_hash,self.role)

    def set_password(self,password):
        self.password_hash=generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def get_id(self):
        return (self.id)

    def getUser(self,form):
        user = Users.query.filter_by(username=form.username.data).first()
        if user.check_password(form.password.data):
            return user
        else:
            bikerental.logger.error(f"User not found: {form.username.data}")
            return None

class Bike(db.Model):
    bike_id = db.Column(db.Integer,index=True,primary_key=True)
    bike_brand = db.Column(db.String(64))
    price = db.Column(db.String(100))
    status = db.Column(db.String(120))
    created_at  =  db.Column(db.DateTime,default=datetime.utcnow)
    def __repr__(self):
        return '<bike_id:{0} bike_brand:{1} price:{2} status:{3}>'.format(self.bike_id,self.bike_brand,self.price,self.status)

class Bike_Parking(db.Model):
    id = db.Column(db.Integer,index=True,primary_key=True,autoincrement="auto")
    bike_Serial_no = db.Column(db.Integer) #change
    location = db.Column(db.String(100))
    Parking_Status = db.Column(db.Boolean)
    time_start = db.Column(db.DateTime)
    time_end  =  db.Column(db.DateTime)
    def __repr__(self):
        return '<id:{0} bike_Serial_no:{1} location:{2} Parking_Status:{3} time_start:{4} time_end:{5}>'.format(self.id,self.bike_Serial_no,self.location,self.Parking_Status,self.time_start,self.time_end)

class Bike_Status(db.Model):
    id = db.Column(db.Integer,index=True,primary_key=True,autoincrement="auto")
    bike_Serial_no = db.Column(db.Integer) #change
    rent_status = db.Column(db.Boolean)
    defective_status = db.Column(db.Boolean)
    lock_status = db.Column(db.Boolean)
    parked_status  =  db.Column(db.Boolean)
    modified_on = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return '<id:{0} bike_Serial_no:{1} rent_status:{2} defective_status:{3} lock_status:{4} parked_status:{5} modified_on:{6}>'.format(self.id,self.bike_Serial_no,self.rent_status,self.defective_status,self.lock_status,self.parked_status,self.modified_on)

class Bike_Location(db.Model):
    id = db.Column(db.Integer, primary_key = True,autoincrement="auto")
    bike_Serial_no = db.Column(db.String(64), index = True, unique = True)
    current_location = db.Column(db.String(128), index = True)
    previous_location = db.Column(db.String(128), index = True)
    current_location_latlong = db.Column(db.String(128), index = True)
    previous_location_latlong = db.Column(db.String(128), index = True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<id:{0} bike_Serial_no:{1} current_location:{2} previous_location:{3} current_location_latlong:{4} previous_location_latlong:{5}>'.format(self.id,self.bike_Serial_no,self.current_location,self.previous_location,self.current_location_latlong,self.previous_location_latlong)

class Bike_Availability(db.Model):
    id = db.Column(db.Integer, primary_key = True,autoincrement="auto")
    location = db.Column(db.String(128), index = True)
    current_location_latlong = db.Column(db.String(128), index = True)
    count = db.Column(db.Integer)
    def __repr__(self):
        return '<id:{0} location:{1} count:{2} latlong: {3}>'.format(self.id,self.location,self.count,self.current_location_latlong)

class Bike_repair(db.Model):
    id =  db.Column(db.Integer,index=True,primary_key=True,autoincrement="auto")
    bike_id =  db.Column(db.Integer,index=True,primary_key=True)
    reported_date = db.Column(db.DateTime)
    fixed_date  =  db.Column(db.DateTime)
    def __repr__(self):
        return '<id:{0} bike_id:{1} reported_date:{2} fixed_date: {3}>'.format(self.id,self.bike_id,self.reported_date,self.fixed_date)

class Booking(db.Model):
    id = db.Column(db.Integer,index=True,primary_key=True,autoincrement="auto")
    booking_id = db.Column(db.Integer,index=True,autoincrement="auto") #change
    customer_id = db.Column(db.Integer) #change
    bike_id = db.Column(db.Integer) #change
    status = db.Column(db.String(100))
    start_location = db.Column(db.String(100))
    end_location = db.Column(db.String(100))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    total_amount = db.Column(db.Float)
    payment_status  =  db.Column(db.String(100)) #change
    booking_status = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow) #change
    def __repr__(self):
        return '<id:{0} booking_id:{1} customer_id:{2} bike_id: {3} status:{4} start_location:{5} end_location:{6} start_date:{7} end_date:{8} total_amount:{9} payment_status:{10} booking_status:{11}> '.format(self.id,self.booking_id,self.customer_id,self.bike_id,self.status,self.start_location,self.end_location,self.start_date,self.end_date,self.total_amount,self.payment_status,self.booking_status)

class Payment(db.Model):
    id = db.Column(db.Integer,index=True,primary_key=True)
    booking_id = db.Column(db.Integer,index=True,unique=True)
    payment_type = db.Column(db.String)
    payment_by = db.Column(db.String)
    payment_date = db.Column(db.DateTime,default=datetime.utcnow)
    payment_status = db.Column(db.String)
    remarks  =  db.Column(db.String)

class Feedback(db.Model):
    id = db.Column(db.Integer,index=True,primary_key=True)
    booking_id = db.Column(db.Integer,index=True,unique=True)
    customer_id = db.Column(db.Integer,index=True,unique=True)
    feedback = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
