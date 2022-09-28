from app.api import bp
from flask import request, jsonify
from app.models import Bike_Availability,Booking,Bike,Bike_Location,Bike_Status
from sqlalchemy import func

@bp.route('/bike/markerlist', methods=['GET'])
def get_bike_markerlist():
    bikes = Bike_Location.query.all()
    bikeList={}
    for count,bike in  enumerate(bikes,1):
        booked = Booking.query.filter_by(bike_id="BIKE-"+bike.bike_Serial_no,booking_status="BOOKED").count() == 0
        markedForRepair = Bike_Status.query.filter(Bike_Status.bike_Serial_no == bike.bike_Serial_no,Bike_Status.defective_status == False).count() > 0
        if booked and markedForRepair:
            if bike.current_location in bikeList.keys():
                bikeList[bike.current_location]['count'] += 1
            else:
                bikeList[bike.current_location]={}
                bikeList[bike.current_location]['count'] = 1
                bikeList[bike.current_location]['current_location_latlong'] = bike.current_location_latlong
                bikeList[bike.current_location]['previous_location_latlong'] = bike.previous_location_latlong
    
    print(bikeList)
    print(jsonify(bikeList))
    return jsonify(bikeList)


@bp.route('/bike/manager/charts/data', methods=['GET'])
def fetch_bike_chart_data():
    customer_booking_info = Booking.query.with_entities(Booking.customer_id,func.count(Booking.customer_id)).group_by(Booking.customer_id).all()
    chart1 = {
        'name' : 'Customer Based Trip Count',
        'data' : [{
            'x':[booking[0] for booking in customer_booking_info],
            'y':[booking[1] for booking in customer_booking_info],
            'type':'bar'
        }]
    }
    types_of_bike = Bike.query.with_entities(Bike.bike_brand,func.count(Bike.bike_brand)).group_by(Bike.bike_brand).all()
    chart2 = {
        'name' : 'Company Based Bike Count',
        'data' : [{
            'labels':[bike[0] for bike in types_of_bike],
            'values':[bike[1] for bike in types_of_bike],
            'textposition': 'inside',
            'hoverinfo': 'x+y',
            'hole': .4,
            'type':'pie'
        }],
        "layout": {
            'height': 400,
            'width': 500
        }
    }
    bike_count = Bike_Availability.query.all()
    chart3 = {
        'name' : 'Location Based Bike Count',
        'data' : [{
            'labels':[bike.location for bike in bike_count],
            'values':[bike.count for bike in bike_count],
            'type':'pie'
        }],
        "layout": {
            'height': 400,
            'width': 500
        }
    }
    location_booking_info = Booking.query.with_entities(Booking.start_location,func.count(Booking.start_location)).group_by(Booking.start_location).all()
    chart4 = {
        'name' : 'Location Based Trip Count',
        'data' : [{
            'x':[booking[0] for booking in location_booking_info],
            'y':[booking[1] for booking in location_booking_info],
            'type':'bar'
        }]
    }

    datetimechart = Booking.query.with_entities(Booking.start_date,func.count(Booking.start_date)).group_by(Booking.start_date).all()

    chart5 = {
        'name' : 'Count of booking done in a month',
        'data' : [{
            'x':[rec[0] for rec in datetimechart],
            'y':[rec[1] for rec in datetimechart],
            'type':'bar'
        }]
    }

    charts={
        '1':chart1,
        '2':chart2,
        '3':chart3,
        '4':chart4,
        '5':chart5
    }

    print(jsonify(charts))
    return jsonify(charts)
