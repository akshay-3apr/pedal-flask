from flask_table import Table, Col
from app.models import Bike_Availability

# Declare table
class LocationBikeCountTable(Table):
    classes = ['table', 'table-bordered','table-hover']
    id = Col("Id.",th_html_attrs={'space': 'col',"class":"table-primary"},column_html_attrs={'class':'mb-3'})
    location = Col("Location",th_html_attrs={'space': 'col',"class":"table-primary"},column_html_attrs={'class':'mb-3'})
    current_location_latlong = Col('LatLong',th_html_attrs={'space': 'col',"class":"table-primary"},column_html_attrs={'class':'mb-3'})
    count = Col('Bike Count',th_html_attrs={'space': 'col',"class":"table-primary"},column_html_attrs={'class':'mb-3'})

class Locations(object):
    def __init__(self,id,location,current_location_latlong,count):
        self.id = id
        self.location = location
        self.current_location_latlong = current_location_latlong
        self.count = count
    def __repr__(self) -> str:
        return f"<location: {self.location} current_location_latlong: {self.current_location_latlong} count: {self.count}>"

def fetchLocationBikeCount():
        # Populate the table
        # Print the html
        locations = Bike_Availability.query.all()
        print(locations)
        locationList=[]
        for loc in  locations:
            locationList.append(Locations(loc.id,loc.location,loc.current_location_latlong,loc.count))

        table = LocationBikeCountTable(locationList)
        return table