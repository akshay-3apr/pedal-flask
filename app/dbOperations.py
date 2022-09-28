from logging import raiseExceptions
from app import bikerental, db
from app.models import Users
import json
import os
import traceback
from sqlalchemy import exc


class DBOperations:
    def add(self, object):
        try:
            db.session.add(object)
            db.session.commit()
            return True
        except exc.SQLAlchemyError:
            bikerental.logger.error("An error occurred while adding data to table: {}".format(traceback.format_exc()))
            raise exc.SQLAlchemyError

    def delete(self, object):
        try:
            db.session.delete(object)
            db.session.commit()
            return True
        except exc.SQLAlchemyError:
            return "An error occurred while deleting data from table: {}".format(traceback.format_exc())

    def merge(self, object):
        try:
            db.session.merge(object)
            db.session.commit()
            return True
        except exc.SQLAlchemyError:
            return "An error occurred while merging data to table: {}".format(traceback.format_exc())

    def fetch(self,object,size):
        try:
            return object.query.limit(size).fetchall()
        except exc.SQLAlchemyError:
            return "An error occurred while fetching data from table: {}".format(traceback.format_exc())

    def fetchAll(self, object):
        try:
            records = object.query.all()
            return records
        except exc.SQLAlchemyError:
            return "An error occurred while fetching all the data from table: {}".format(traceback.format_exc())
    
    def count(self,objectCol):
        try:
            return db.session.query(objectCol).count()
        except exc.SQLAlchemyError:
            return "An error occurred while getting row count of the data from table: {}".format(traceback.format_exc())
    
    def db_cusQuery(self,object):
        return db.session.query(object)

    def db_Commit(self):
        db.session.commit()

    # don't run this
    def clean_slate(self):
        meta = db.metadata
        for table in reversed(meta.sorted_tables):
            print('Clear table:',table)
            db.session.execute(table.delete())
        self.db_Commit()
