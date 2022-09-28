from app import bikerental,db
from app .dbOperations import DBOperations
import json,os,traceback
from sqlalchemy import exc
from app.models import Users

class UserDB:

    dbOperations = DBOperations()

    def add_User(self,user):
        try:
            self.dbOperations.add(user)
            return True
        except exc.SQLAlchemyError:
            return None
    
    def fetchAll(self):
        try:
            users = self.dbOperations.fetchAll(Users)
            print(users)
            return users
        except exc.SQLAlchemyError:
            return f"An error occurred while fetching all users from the User table: {traceback.format_exc()}"