from flask_table import Table, Col,ButtonCol
from app.models import Bike_Location,Booking,Bike_repair,Bike,Bike_Status
from datetime import datetime

# Declare table
class BikeTable(Table):
    classes = ['table', 'table-bordered','table-hover']
    number = Col("No.",th_html_attrs={'space': 'col',"class":"table-primary"},column_html_attrs={'class':'mb-3'})
    bike_id = Col('Bike Serial Number',th_html_attrs={'space': 'col',"class":"table-primary"},column_html_attrs={'class':'mb-3'})
    book = ButtonCol('Book',endpoint="booking",url_kwargs=dict(bike_id='bike_id',startlocation='location'),button_attrs={'class':'btn btn-primary btn-lg ms-2'},th_html_attrs={'space': 'col',"class":"table-primary"})

class AvailableBike(object):
    def __init__(self, count,bike_Serial_no,location):
        self.number = count
        self.bike_id = bike_Serial_no
        self.location = location

def fetchBikeTable(location):
        # Populate the table
        # Print the html
        # get bike based on location
        bikes = Bike_Location.query.filter(Bike_Location.current_location==location).all()
        print(bikes)
        bikeList=[]
        for count,bike in  enumerate(bikes,1):
            booked = Booking.query.filter_by(bike_id="BIKE-"+bike.bike_Serial_no,booking_status="BOOKED").count() == 0
            markedForRepair = Bike_Status.query.filter(Bike_Status.bike_Serial_no == bike.bike_Serial_no,Bike_Status.defective_status == False).count() > 0
            if booked and markedForRepair:
                bikeList.append(AvailableBike(count,"BIKE-"+bike.bike_Serial_no,location))

        print(bikeList)
        table = BikeTable(bikeList)
        print(table.__html__())
        # or just {{ table }} from within a Jinja template
        return table