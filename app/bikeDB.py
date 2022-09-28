from app import bikerental,db
from app .dbOperations import DBOperations
import json,os,traceback
from sqlalchemy import exc
from app.models import Users
from app import dbOperations
from app.models import Bike_Availability,Booking
from datetime import date, timedelta,datetime

class BikeDB:

    dbOperations = DBOperations()

    def add(self,bike):
        try:
            self.dbOperations.add(bike)
            return True
        except exc.SQLAlchemyError:
            return None
    
    def merge(self,bike):
        try:
            self.dbOperations.add(bike)
            return True
        except exc.SQLAlchemyError:
            return None

    def rowCount(self,objectCol):
        try:
            return self.dbOperations.count(objectCol)
        except exc.SQLAlchemyError:
            return None
    
    def getCount(self,object,field,value):
        return self.dbOperations.db_cusQuery(object).filter(field==value).count()

    def checkbikelocation(self,location):
        try:
            count = Bike_Availability.query.filter(Bike_Availability.location == location).count()
            print(count)
            if count>0:
                return True
            else:
                return False
        except exc.SQLAlchemyError:
            return None

    def addBikeAvailability(self,location,count):
        try:
            bikelocation = self.dbOperations.db_cusQuery(Bike_Availability).filter(Bike_Availability.location == location).first()
            bikelocation.count += count
            self.dbOperations.db_Commit()
            return bikelocation.count
        except exc.SQLAlchemyError:
            return None
    
    def removeBikeAvailability(self,location,count):
        try:
            bikelocation = self.dbOperations.db_cusQuery(Bike_Availability).filter(Bike_Availability.location == location).first()
            bikelocation.count -= count
            self.dbOperations.db_Commit()
            return bikelocation.count
        except exc.SQLAlchemyError:
            return None
    
    def updateBooking(self,username,price):
        try:
            booking = Booking.query.filter_by(customer_id=username,booking_status="BOOKED").first()
            booking.status="FINISHED"
            booking.end_date = datetime.now()
            booking.payment_status = "SUCCESSFUL"
            booking.booking_status = None
            self.dbOperations.db_Commit()
            return True
        except exc.SQLAlchemyError:
            return None

    def fetch(self,object):
        try:
            obj = self.dbOperations.fetch(object)
            return obj
        except exc.SQLAlchemyError:
            return f"An error occurred while fetching data from table: {traceback.format_exc()}"
    
    def fetchWithCondition(self,object,field,value):
        try:
            obj = self.dbOperations.db_cusQuery(object).filter(field==value).all()
            return obj
        except exc.SQLAlchemyError:
            return f"An error occurred while fetching data from table: {traceback.format_exc()}"
    
    def fetchAll(self,object):
        try:
            obj = self.dbOperations.fetchAll(object)
            return obj
        except exc.SQLAlchemyError:
            return f"An error occurred while fetching data from table: {traceback.format_exc()}"
    
    def commit(self):
        self.dbOperations.db_Commit()