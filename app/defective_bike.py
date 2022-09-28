from flask_table import Table, Col,ButtonCol
from app.models import Bike, Bike_Location, Bike_Status,Bike_Availability,Booking

# Declare table
class DefectiveBikeTable(Table):
    classes = ['table', 'table-bordered','table-hover']
    number = Col("No.",th_html_attrs={'space': 'col',"class":"table-primary"},column_html_attrs={'class':'mb-3'})
    bike_id = Col('Bike Serial Number',th_html_attrs={'space': 'col',"class":"table-primary"},column_html_attrs={'class':'mb-3'})
    location = Col('Location',th_html_attrs={'space': 'col',"class":"table-primary"},column_html_attrs={'class':'mb-3'})
    book = ButtonCol('Mark Defective',endpoint="reportdefectiveBikes",url_kwargs=dict(bike_id='bike_id'),button_attrs={'class':'btn btn-primary btn-lg ms-2'},th_html_attrs={'space': 'col',"class":"table-primary"})

class DefectiveBike(object):
    def __init__(self, count,bike_Serial_no,location):
        self.number = count
        self.bike_id = bike_Serial_no
        self.location = location
    def __repr__(self) -> str:
        return f"<number: {self.number} bike_id: {self.bike_id} location:{self.location}>"

def fetchDefectiveBiketable():
    # Populate the table
    # Print the html
    bikes = Bike.query.all()
    print(bikes)
    bikeList=[]
    for count,bike in  enumerate(bikes,1):
        booked = Booking.query.filter_by(bike_id="BIKE-"+str(bike.bike_id),booking_status="BOOKED").count() == 0
        markedForRepair = Bike_Status.query.filter(Bike_Status.bike_Serial_no == bike.bike_id,Bike_Status.defective_status == False).count() > 0
        print(Booking.query.filter_by(bike_id="BIKE-"+str(bike.bike_id),booking_status=None).count())
        if booked and markedForRepair:
            bike_loc = Bike_Location.query.filter(Bike_Location.bike_Serial_no==bike.bike_id).first()
            bikeList.append(DefectiveBike(count,"BIKE-"+str(bike.bike_id),bike_loc.current_location))
    table = DefectiveBikeTable(bikeList)
    return table