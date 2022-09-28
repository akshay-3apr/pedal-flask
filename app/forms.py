from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,HiddenField
from wtforms.fields.core import IntegerField, SelectField
from wtforms.validators import DataRequired, ValidationError
from wtforms.widgets.core import Select

from app.models import Users

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

    def validate_username(self, username):
        if username.data != self.username:
            user = Users.query.filter_by(username=self.username.data).first()
            if user is None:
                raise ValidationError('User not registered')

    def validate_password(self,password):
        if password.data != self.password:
            user = Users.query.filter_by(username=self.username.data).first()
            if user != None and (not user.check_password(password.data)):
                    raise ValidationError('Incorrect password')

class LoadOperatorForm(FlaskForm):
    firstname = StringField('Firstname', validators=[DataRequired()])
    lastname = StringField('Lastname', validators=[DataRequired()])
    email = StringField('Email Id', validators=[DataRequired()])
    phonenumber = StringField('Phone Number', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_username(self, username):
        if username.data != self.username:
            customer = Users.query.filter_by(
                username=self.username.data).first()
            if customer is not None:
                raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        if email.data != self.email:
            customer = Users.query.filter_by(email=self.email.data).first()
            if customer is not None:
                raise ValidationError('This email is already registered.')

    def validate_phonenumber(self, phonenumber):
        if phonenumber.data != self.phonenumber:
            customer = Users.query.filter_by(
                phonenumber=self.phonenumber.data).first()
            if customer is not None:
                raise ValidationError(
                    'This phone number is already registered.')


class RegistrationForm(FlaskForm):
    firstname = StringField('Firstname', validators=[DataRequired()])
    lastname = StringField('Lastname', validators=[DataRequired()])
    email = StringField('Email Id', validators=[DataRequired()])
    phonenumber = StringField('Phone Number', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        if username.data != self.username:
            customer = Users.query.filter_by(
                username=self.username.data).first()
            if customer is not None:
                raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        if email.data != self.email:
            customer = Users.query.filter_by(email=self.email.data).first()
            if customer is not None:
                raise ValidationError('This email is already registerd.')

    def validate_phonenumber(self, phonenumber):
        if phonenumber.data != self.phonenumber:
            customer = Users.query.filter_by(
                phonenumber=self.phonenumber.data).first()
            if customer is not None:
                raise ValidationError(
                    'This phone number is already registerd.')

class ManageCycleForm(FlaskForm):
    startlocation = StringField('From Location', validators=[DataRequired()])
    endlocation = StringField('To Location')
    startlatitude = StringField('Latitude', validators=[DataRequired()])
    startlongitude = StringField('Longitude', validators=[DataRequired()])
    endlatitude = StringField('Latitude')
    endlongitude = StringField('Longitude')
    count = IntegerField('Cycle Count', validators=[DataRequired()])
    bikebrand = StringField('Bike Brand', validators=[DataRequired()])
    bikeprice = IntegerField('Price', validators=[DataRequired()])
    submit = SubmitField('Submit')

class SearchRideForm(FlaskForm):
    pickupLocation = StringField('Pick-Up Location', validators=[DataRequired()])
    pickupLocationHidden = HiddenField('storedValue')
    submit = SubmitField('Submit')

class EndTripForm(FlaskForm):
    pickupLocation = SelectField('End Trip Location',coerce=int, validators=[DataRequired()])
    submit = SubmitField('End Trip')