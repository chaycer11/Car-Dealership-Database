from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    address = StringField('Home Address', validators=[DataRequired()])
    
    password = PasswordField('Password', validators=[DataRequired()])
    # This ensures they didn't typo their new password
    confirm_password = PasswordField('Confirm Password', 
                         validators=[DataRequired(), EqualTo('password')])
    
    submit = SubmitField('Create Account')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

    user_type = SelectField('Login as:', choices=[
        ('employee', 'Employee'),
        ('customer', 'Customer')
    ], validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class VehicleForm(FlaskForm):
    vin = StringField('VIN', validators=[DataRequired(), Length(max=50)])
    make = StringField('Make', validators=[DataRequired(), Length(max=50)])
    model = StringField('Model', validators=[DataRequired(), Length(max=50)])
    year = StringField('Year', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])

    location = SelectField('Location', choices=[
        ('main_lot', 'Main Lot'),
        ('remote_lot', 'Remote Lot'),
        ('other_dealership', 'Other Dealership'),
        ('in_transit', 'In Transit')
    ], validators=[DataRequired()])
    # We default the new car to 'inventory' and main lot
    submit = SubmitField('Add Vehicle to Inventory')

class CustomerForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email Address', validators=[DataRequired(), Email(), Length(max=100)])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(max=20)])
    address = StringField('Home Address', validators=[DataRequired(), Length(max=255)])

    
    # The rubric requires "purchase, service, or visit"
    customer_type = SelectField('Customer Type', choices=[
        ('visit', 'Just Visiting / Browsing'),
        ('purchase', 'Looking to Purchase'),
        ('service', 'Here for Service')
    ], validators=[DataRequired()])
    
    submit = SubmitField('Add Customer')

class SaleForm(FlaskForm):
    vehicle_id = StringField('Vehicle ID', validators=[DataRequired()])
    customer_id = StringField('Customer ID', validators=[DataRequired()])
    temp_tag_num = StringField('Temporary Tag Number', validators=[DataRequired(), Length(max=50)])
    customization = StringField('Customization Work (Optional)', validators=[Length(max=255)])
    submit = SubmitField('Process Sale')

class ServiceForm(FlaskForm):
    vehicle_id = StringField('Vehicle ID', validators=[DataRequired()])
    customer_id = StringField('Customer ID', validators=[DataRequired()])
    
    # --- CHANGED THIS LINE ---
    mechanic_id = SelectField('Assigned Mechanic', coerce=int, validators=[DataRequired()])
    
    mileage_in = StringField('Mileage In', validators=[DataRequired()])
    mileage_out = StringField('Mileage Out', validators=[DataRequired()])
    preliminary_estimate = StringField('Preliminary Estimate ($)', validators=[DataRequired()])
    work_done = StringField('Work Performed', validators=[DataRequired(), Length(max=255)])
    submit = SubmitField('Log Service Ticket')

class BillingForm(FlaskForm):
    ticket_type = SelectField('Payment For', choices=[
        ('sale', 'Vehicle Purchase'),
        ('service', 'Service Repair')
    ], validators=[DataRequired()])
    
    ticket_id = StringField('Ticket ID (Sale ID or Service ID)', validators=[DataRequired()])
    
    amount = StringField('Total Amount ($)', validators=[DataRequired()])
    
    payment_method = SelectField('Payment Method', choices=[
        ('Cash', 'Cash'),
        ('Credit', 'Credit Card'),
        ('Financing', 'Bank Financing')
    ], validators=[DataRequired()])
    
    submit = SubmitField('Process Payment')