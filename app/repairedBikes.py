from flask_table import Table, Col,ButtonCol
from app.models import Bike,Booking,Bike_repair,Bike_Location
from datetime import datetime
from sqlalchemy import or_

# Declare table
class RepairedBikeTable(Table):
    classes = ['table', 'table-bordered','table-hover']
    number = Col("No.",th_html_attrs={'space': 'col',"class":"table-primary"},column_html_attrs={'class':'mb-3'})
    bike_id = Col('Bike Serial Number',th_html_attrs={'space': 'col',"class":"table-primary"},column_html_attrs={'class':'mb-3'})
    location = Col('Location',th_html_attrs={'space': 'col',"class":"table-primary"},column_html_attrs={'class':'mb-3'})
    book = ButtonCol('Repaired',endpoint="repairDefectiveBikes",url_kwargs=dict(bike_id='bike_id'),button_attrs={'class':'btn btn-primary btn-lg ms-2'},th_html_attrs={'space': 'col',"class":"table-primary"})

class RepairedBike(object):
    def __init__(self, count,bike_Serial_no,location):
        self.number = count
        self.bike_id = bike_Serial_no
        self.location = location
    def __repr__(self) -> str:
        return f"<number: {self.number} bike_id: {self.bike_id}>"

def fetchBikeRepaireTable():
        # Populate the table
        # Print the html
        bikes = Bike_repair.query.filter(Bike_repair.fixed_date==None).all()
        print(bikes)
        bikeList=[]
        for count,bike in  enumerate(bikes,1):
            id = bike.bike_id.split("-")[1]
            bike_loc = Bike_Location.query.filter(Bike_Location.bike_Serial_no==id).first()
            bikeList.append(RepairedBike(count,bike.bike_id,bike_loc.current_location))

        table = RepairedBikeTable(bikeList)
        return table