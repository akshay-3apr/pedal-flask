from flask import render_template, flash, redirect, url_for
from flask_login.utils import logout_user
from app import bikerental
from app.userDB import UserDB
from flask_login import current_user, login_user, login_required
from app.models import Users, Bike, Bike_Location, Bike_Status, Bike_Availability, Booking, Bike_repair, load_user
from app.forms import LoginForm, RegistrationForm, LoadOperatorForm, ManageCycleForm, SearchRideForm, EndTripForm
from flask import request
from werkzeug.urls import url_parse
from app.utility import check_loggedInUser
from app.bikeDB import BikeDB
from app.config import Config
from app.bikeTable import fetchBikeTable
from app.defective_bike import fetchDefectiveBiketable
from app.repairedBikes import fetchBikeRepaireTable
from app.bikeCountTable import fetchLocationBikeCount
from datetime import date, timedelta, datetime
from sqlalchemy import desc


@bikerental.route("/index")
@login_required
def index():
    return render_template('index.html')


@bikerental.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@bikerental.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('load_dash'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users().getUser(form)
        if user is None:
            flash('Invalid username or password', "danger")
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('load_dash')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

#load dash after login - dashboard will load dynamically based on role
@bikerental.route("/")
@bikerental.route("/dash")
@login_required
def load_dash():
    sideBarItems, navBarItems = check_loggedInUser(current_user)
    if current_user.role.lower() == 'customer':
        return render_template('user/customer_dash.html', title='Customer', sideBarItems=sideBarItems, navBarItems=navBarItems, form=SearchRideForm())
    elif current_user.role.lower() == 'operator':
        return render_template('user/operator_dash.html', title='Operator', sideBarItems=sideBarItems, navBarItems=navBarItems, bikes_bookings=Booking.query.all())
    elif current_user.role.lower() == 'manager':
        return render_template('user/manager_charts.html', title='Manager', sideBarItems=sideBarItems, navBarItems=navBarItems)

##CUSTOMER
# All customer route mentioned below
@bikerental.route("/customer/registration", methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        fname = form.firstname.data
        lname = form.lastname.data
        email = form.email.data
        phoneno = form.phonenumber.data
        address = form.address.data
        pwd = form.password.data
        customer = Users(username=username, firstname=fname, lastname=lname,
                         email=email, phonenumber=phoneno, address=address, role="CUSTOMER")
        customer.set_password(pwd)
        status = UserDB().add_User(customer)
        if status is not None:
            return redirect(url_for('login'))
    return render_template('registration.html', title='Sign Up', form=form)

# Fetch Ride list for Customer
@bikerental.route("/customer/rides", methods=["GET", "POST"])
@login_required
def getRideList():
    print('inside getRideList')
    sideBarItems, navBarItems = check_loggedInUser(current_user)
    form = SearchRideForm()
    if form.validate_on_submit():
        location = form.pickupLocation.data
        locationStoredValue = form.pickupLocationHidden.data
        return render_template('user/customer_dash.html', title='Customer', sideBarItems=sideBarItems, navBarItems=navBarItems, form=SearchRideForm(), table=fetchBikeTable(location))
    return redirect(url_for('load_dash'))

## Customer Booking Ride
@bikerental.route("/customer/booking/<startlocation>/<bike_id>", methods=["GET", "POST"])
@login_required
def booking(startlocation, bike_id):
    print("inside making booking")
    sideBarItems, navBarItems = check_loggedInUser(current_user)
    bikeDB = BikeDB()
    customer_id = current_user.username
    status = "INTRANSIT"
    start_location = startlocation
    end_location = ""
    start_date = datetime.now()
    end_date = datetime.now() + timedelta(days=1)
    total_amount = 0.00
    payment_status = "NOT-INITIATED"
    booking_status = "BOOKED"
    if Booking.query.filter_by(customer_id=customer_id, booking_status="BOOKED").count() == 0:
        status = bikeDB.add(Booking(customer_id=customer_id, bike_id=bike_id, status=status, start_location=start_location, end_location=end_location,
                            start_date=start_date, end_date=end_date, total_amount=total_amount, payment_status=payment_status, booking_status=booking_status))
        if status:
            flash("Booking done succesfully", "success")
            return redirect(url_for("payment"))
    else:
        flash("There is an ongoing trip. Please end the current trip to make a new one !!", "danger")
        return redirect(url_for("payment"))

# customer  payment
@bikerental.route("/customer/payment")
@login_required
def payment():
    sideBarItems, navBarItems = check_loggedInUser(current_user)
    for item in navBarItems:
        if item['item'].lower() == 'payment':
            item['active'] = True
        else:
            item['active'] = False
    form = EndTripForm()
    currenttrip = Booking.query.filter_by(customer_id=current_user.username, booking_status="BOOKED").first()
    previousTrips = Booking.query.filter_by(customer_id=current_user.username, booking_status=None).all()
    for trip in previousTrips:
        trip.total_time = round(((trip.end_date - trip.start_date).total_seconds() / 60.0)/60.0,2)
        trip.total_cost = Config.PRICE*trip.total_time
    
    locationlist = []
    for location in Bike_Availability.query.all():
        locationlist.append((location.id,location.location))
    form.pickupLocation.choices = locationlist
    return render_template('user/trips.html', title="Payment", form=form, sideBarItems=sideBarItems, navBarItems=navBarItems, currenttrip=currenttrip, previousTrips=previousTrips, mDisabled=True)

# Payment confirmation
@bikerental.route("/customer/paymentconfirmation")
@login_required
def paymentconfirmation():
    sideBarItems, navBarItems = check_loggedInUser(current_user)
    for item in navBarItems:
        if item['item'].lower() == 'payment':
            item['active'] = True
        else:
            item['active'] = False
    bikeDB = BikeDB()
    bikeDB.updateBooking(current_user.username, Config.PRICE)
    flash("Payment Successful", "success")
    return redirect(url_for('payment'))

# Customer Defective Bikes
@bikerental.route("/customer/report/defective")
@login_required
def defectiveBikes():
    sideBarItems, navBarItems = check_loggedInUser(current_user)
    return render_template('user/report_defective.html', title="Bikes", sideBarItems=sideBarItems, navBarItems=navBarItems, table=fetchDefectiveBiketable())

# customer endtrip
@bikerental.route("/customer/endtrip", methods=["GET", "POST"])
@login_required
def endtrip():
    sideBarItems, navBarItems = check_loggedInUser(current_user)
    for item in navBarItems:
        if item['item'].lower() == 'payment':
            item['active'] = True
        else:
            item['active'] = False
    form = EndTripForm()
    
    bikeDB = BikeDB()
    previousTrips = Booking.query.filter_by(customer_id=current_user.username, booking_status=None).order_by(desc(Booking.end_date)).all()
    for previousTrip in previousTrips:
        previousTrip.total_time = round((((previousTrip.end_date - previousTrip.start_date).total_seconds() / 60.0)/60.0),2)
    
    ##update necessary field on trip end
    currentTrip = Booking.query.filter_by(customer_id=current_user.username, booking_status="BOOKED").first()
    ##Booking table
    currentTrip.end_location = Bike_Availability.query.filter_by(id=form.pickupLocation.data).first().location
    currentTrip.end_date = datetime.now()
    currentTrip.total_time = round((((currentTrip.end_date - currentTrip.start_date).total_seconds() / 60.0)/60.0),2)
    currentTrip.total_amount = Config.PRICE*currentTrip.total_time
    currentTrip.payment_status = "DONE"
    ##update bike location
    id=currentTrip.bike_id.split("-")[1]
    bike_location = Bike_Location.query.filter_by(bike_Serial_no=id).first()
    bike_location.current_location = currentTrip.end_location
    bike_location.previous_location = currentTrip.start_location
    current_latlong = Bike_Availability.query.filter_by(location=currentTrip.end_location).first().current_location_latlong
    previous_latlong = Bike_Availability.query.filter_by(location=currentTrip.start_location).first().current_location_latlong
    bike_location.current_location_latlong = current_latlong
    bike_location.previous_location_latlong = previous_latlong
    ##bike availability
    bikeDB.addBikeAvailability(currentTrip.end_location, 1)
    bikeDB.removeBikeAvailability(currentTrip.start_location,1)
    ##commit changes
    bikeDB.commit()

    flash("End Trip Successful. Continue with payment", "success")
    
    locationlist = []
    for location in Bike_Availability.query.all():
        locationlist.append((location.id,location.location))
    form.pickupLocation.choices = locationlist
    form.pickupLocation(disabled=True)

    return render_template('user/trips.html', title="Payment", form=form, sideBarItems=sideBarItems, navBarItems=navBarItems, currenttrip=currentTrip, previousTrips=previousTrips, eDisabled=True)

# Customer report Defective Bikes
@bikerental.route("/customer/report/defective/<bike_id>", methods=["GET", "POST"])
@login_required
def reportdefectiveBikes(bike_id):

    sideBarItems, navBarItems = check_loggedInUser(current_user)
    id = bike_id.split('-')[1]
    bikeDB = BikeDB()
    bike_repair_row_count = bikeDB.rowCount(Bike_repair.id)
    br = Bike_repair(id=bike_repair_row_count+1,bike_id=bike_id,reported_date=datetime.now(),fixed_date=None)
    bikeDB.add(br)
    # update new bike status in table
    bikeStatus = Bike_Status.query.filter(Bike_Status.bike_Serial_no==id).first()
    if bikeStatus == None:
        bikeStatus = Bike_Status(bike_Serial_no=id, rent_status=False,defective_status=True, lock_status=True, parked_status=True)
        bikeDB.add(bikeStatus)
    else:
        bikeStatus.defective_status=True
        bikeDB.commit()

    flash("Cycle reported defective", "warning")
    return redirect(url_for('defectiveBikes'))

#Customer forgot password page
@bikerental.route("/customer/forgot_password")
def forgot_password():
    return "forgot_password Page !!"


##OPERATOR
#Below function is written to handle manage cycle functionality for Operator
@bikerental.route('/operator/managecycles', methods=['GET', 'POST'])
@login_required
def manageCycles():
    form = ManageCycleForm()
    sideBarItems, navBarItems = check_loggedInUser(current_user)
    if form.validate_on_submit():
        print('Managing Cycles Form validated')
        startlocation = form.startlocation.data
        endlocation = form.endlocation.data
        current_location_latlong = f'({form.startlatitude.data},{form.startlongitude.data})'
        previous_location_latlong = f'({form.endlatitude.data},{form.endlongitude.data})'
        count = form.count.data
        bikebrand = form.bikebrand.data
        bikeprice = form.bikeprice.data
        bikeDB = BikeDB()
        currentCount = bikeDB.rowCount(Bike.bike_id)
        # adding new bike to bike table
        if endlocation == "" or endlocation is None:
            for idx in range(1, count+1):
                currentCount += 1
                # add new bikes
                bike = Bike(bike_id=currentCount,
                            bike_brand=bikebrand, price=bikeprice)
                bikeDB.add(bike)
                # update new bike status in table
                bikeStatus = Bike_Status(bike_Serial_no=currentCount, rent_status=False,
                                         defective_status=False, lock_status=True, parked_status=True)
                bikeDB.add(bikeStatus)
                # updating bike current location
                bikelocation = Bike_Location(   bike_Serial_no=currentCount,
                                                current_location=startlocation,
                                                previous_location=startlocation,
                                                current_location_latlong=current_location_latlong, previous_location_latlong=current_location_latlong)
                bikeDB.add(bikelocation)
        else:
            bikes = bikeDB.fetchWithCondition(Bike_Location,Bike_Location.current_location,endlocation)
            for idx,bike in enumerate(bikes,1):
                # as these bikes are getting moved from one location to another, they are already added to system.
                # updating bike current location
                if idx>count:
                    break
                bike.current_location = startlocation
                bike.previous_location = endlocation
                bike.current_location_latlong=current_location_latlong
                bike.previous_location_latlong=previous_location_latlong
                bikeDB.commit()

        # updating bike availability at location
        if endlocation == "" or endlocation is None:
            bikeAvailability = Bike_Availability(
                location=startlocation, count=count, current_location_latlong=current_location_latlong)
            bikeDB.add(bikeAvailability)
            message = {"status": True, "msg": f"Final count of cycles added to {startlocation}: {count}"}
        elif bikeDB.checkbikelocation(startlocation):
            bikecount = bikeDB.addBikeAvailability(startlocation, count)
            bikeDB.removeBikeAvailability(endlocation,count)
            message = {"status": True, "msg": f"Final count of cycles at {startlocation}: {bikecount}"}
        else:
            bikeAvailability = Bike_Availability(
                location=startlocation, count=count, current_location_latlong=current_location_latlong)
            bikeDB.add(bikeAvailability)
            bikeDB.removeBikeAvailability(endlocation,count)
            message = {"status": True, "msg": f"Final count of cycles moved to {startlocation}: {count}"}
        return render_template('user/movecycle.html', sideBarItems=sideBarItems, navBarItems=navBarItems, form=form, message=message,table=fetchLocationBikeCount())
    return render_template('user/movecycle.html', sideBarItems=sideBarItems, navBarItems=navBarItems, form=form,table=fetchLocationBikeCount())

#repair bikes
@bikerental.route("/operator/repair")
@login_required
def repairBikes():
    sideBarItems, navBarItems = check_loggedInUser(current_user)
    return render_template('user/report_defective.html', title="Bikes", sideBarItems=sideBarItems, navBarItems=navBarItems, table=fetchBikeRepaireTable())

#marked Bikes as repaired
@bikerental.route("/operator/repair/<bike_id>", methods=["GET", "POST"])
@login_required
def repairDefectiveBikes(bike_id):
    id = bike_id.split("-")[1]
    # update Bike-repair table
    bikeDB = BikeDB()
    bike = Bike_repair.query.filter(Bike_repair.bike_id==bike_id,Bike_repair.fixed_date==None).first()
    bike.fixed_date=datetime.now()
    # update new bike status in table
    bikeStatus = Bike_Status.query.filter(Bike_Status.bike_Serial_no==id).first()
    bikeStatus.defective_status=False
    bikeDB.commit()
    flash("Cycle repaired successfully", "success")
    return redirect(url_for('repairBikes'))

##MANAGER
# manager functionalities
@bikerental.route("/manager/loadoperator", methods=['GET', 'POST'])
@login_required
def loadOperator():
    '''
        this functions loads operator to the platform
        only manager can access this page
    '''
    print('inside loadOperator')
    sideBarItems, navBarItems = check_loggedInUser(current_user)
    for item in navBarItems:
        if item['item'].lower() == 'load operator':
            item['active'] = True
        else:
            item['active'] = False
    form = LoadOperatorForm()
    print(form)
    if form.validate_on_submit():
        print("Reading operator creation form")
        username = form.username.data
        fname = form.firstname.data
        lname = form.lastname.data
        email = form.email.data
        phoneno = form.phonenumber.data
        address = form.address.data
        pwd = form.password.data
        operator = Users(username=username, firstname=fname, lastname=lname,
                         email=email, phonenumber=phoneno, address=address, role="OPERATOR")
        operator.set_password(pwd)
        status = UserDB().add_User(operator)
        print("Operator creation status", status)
        if status is not None:
            messages = [
                {'status': True, 'msg': 'Operator created Successfully'}]
            form.username.data = ""
            form.firstname.data = ""
            form.lastname.data = ""
            form.email.data = ""
            form.phonenumber.data = ""
            form.address.data = ""
            form.password.data = ""
            return render_template('user/loadOperator.html', title="Load Operator", sideBarItems=sideBarItems, navBarItems=navBarItems, form=form, messages=messages)
        else:
            messages = [
                {'status': False, 'msg': 'There was issue in Operator creation'}]
            form.username.data = ""
            form.firstname.data = ""
            form.lastname.data = ""
            form.email.data = ""
            form.phonenumber.data = ""
            form.address.data = ""
            form.password.data = ""
            return render_template('user/loadOperator.html', title="Load Operator", sideBarItems=sideBarItems, navBarItems=navBarItems, form=form, messages=messages)
    return render_template('user/loadOperator.html', title="Load Operator", sideBarItems=sideBarItems, navBarItems=navBarItems, form=form)

#plot manager charts
@bikerental.route("/manager/charts")
@login_required
def load_manager_charts():
    sideBarItems, navBarItems = check_loggedInUser(current_user)
    return render_template("user/manager_charts.html", title="Charts", sideBarItems=sideBarItems, navBarItems=navBarItems)

##BACKDOOR TO LOAD DATA
@bikerental.route("/operator/add", methods=["GET", "POST"])
def add_operator():
    userDB = UserDB()
    operator = Users(username="Operator", firstname="Operator", lastname="User", email="operator@gmail1.com",
                     phonenumber="876545678", address="Firhill, Glasgow", role="OPERATOR")
    operator.set_password("operator")
    userDB.add_User(operator)
    users = userDB.fetchAll()
    return render_template('list.html', users=users)


@bikerental.route("/manager/add", methods=["GET", "POST"])
def add_manager():
    userDB = UserDB()
    manager = Users(username="Manager", firstname="Manager", lastname="User", email="manager@gmail1.com",
                    phonenumber="7654345678", address="Firhill, Glasgow", role="MANAGER")
    manager.set_password("manager")
    userDB.add_User(manager)
    users = userDB.fetchAll()
    return render_template('list.html', users=users)


@bikerental.route("/user/delete")
def delete_user():
    return "Deletion Page"
