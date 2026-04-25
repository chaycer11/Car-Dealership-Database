from flask import Flask, render_template, url_for, redirect, flash, request
import db
from dotenv import load_dotenv
from auth import auth_bp
from forms import VehicleForm, CustomerForm, ServiceForm, BillingForm, SaleForm
from flask_login import LoginManager, login_required, current_user

app = Flask(__name__)

app.config['SECRET_KEY'] = 'd757a259ea5d51bd40f2eaff47aad6ae'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login' # Redirects here if @login_required fails

@login_manager.user_loader
def load_user(user_id):
    return db.get_user_by_id(user_id)

app.register_blueprint(auth_bp)

@app.route('/')
def index():
    return redirect(url_for('auth.register'))

@app.route('/home')
def home():
    return render_template('base.html')


@app.route('/vehicles')
def database():
    make = request.args.get('make')
    model = request.args.get('model')
    year = request.args.get('year')
    max_price = request.args.get('max_price')

    if current_user.is_authenticated and current_user.user_type == 'employee':
        
        if current_user.role == 'mechanic':
            # Mechanics only see the Service Queue
            vehicles = db.get_service_queue()
            return render_template('index.html', cars=vehicles)
            
        elif current_user.role == 'salesperson':
            # Salespeople see EVERYTHING and can still use filters
            vehicles = db.get_all_inventory(make, model, year, max_price)
            return render_template('index.html', cars=vehicles)

    # 2. Pass them to our new secure function
    vehicles = db.get_showroom_vehicles(make, model, year, max_price)
    
    try:
        return render_template('index.html', cars=vehicles)
    except Exception as e:
        return f"<h1> System online but failed to connect to database </h1> <p> Error: {e} </p>"
    

@app.route('/add_vehicle', methods=['GET', 'POST'])
@login_required
def add_vehicle():
    # Only employees should be able to add vehicles, so we check their user_type before showing the form
    if current_user.role != 'salesperson':
        flash("Unauthorized access.", "danger")
        return redirect(url_for('home'))
    form = VehicleForm()
    if form.validate_on_submit():
        success = db.insert_vehicle(
            vin=form.vin.data,
            make=form.make.data,
            model=form.model.data,
            year=form.year.data,
            price=form.price.data,
            location=form.location.data
        )
        if success:
            # Flash a green success message and send them to the inventory page
            flash(f'Successfully added {form.year.data} {form.make.data} {form.model.data} to inventory!', 'success')
            return redirect(url_for('database'))
        else:
            flash('Error adding vehicle to database. Check the VIN.', 'danger')
            
    return render_template('add_vehicle.html', form=form)

@app.route('/add_customer', methods=['GET', 'POST'])
@login_required
def add_customer():
    # Only employees should be able to add customers, so we check their user_type before showing the form
    if current_user.role != 'salesperson':
        flash("Unauthorized: Staff access only.", "danger")
        return redirect(url_for('home'))
    form = CustomerForm()
    if form.validate_on_submit():
        success = db.insert_customer(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            address=form.address.data,
            customer_type=form.customer_type.data
        )
        if success:
            flash(f'Successfully added customer {form.name.data}!', 'success')
            return redirect(url_for('home')) # Redirects back to the main dashboard
        else:
            flash('Error adding customer to database.', 'danger')
            
    return render_template('add_customer.html', form=form)



@app.route('/sell_vehicle', methods=['GET', 'POST'])
@login_required
def sell_vehicle():
    # Only employees should be able to process sales, so we check their user_type before showing the form
    if current_user.role != 'salesperson':
        flash("Unauthorized: Staff access only.", "danger")
        return redirect(url_for('home'))
    form = SaleForm()
    if form.validate_on_submit():
        success = db.process_sale(
            vehicle_id=form.vehicle_id.data,
            customer_id=form.customer_id.data,
            temp_tag_num=form.temp_tag_num.data,
            customization_work=form.customization.data,
            salesperson_id=1  # Hardcoding Sarah Jenkins until login is finished!
        )
        if success:
            flash('Sale processed successfully! The vehicle has been removed from available inventory.', 'success')
            return redirect(url_for('database'))
        else:
            flash('Transaction failed. Make sure the Vehicle ID and Customer ID actually exist!', 'danger')
            
    return render_template('sell_vehicle.html', form=form)


@app.route('/service_vehicle', methods=['GET', 'POST'])
@login_required
def service_vehicle():
    if current_user.role != 'mechanic':
        flash("Unauthorized: Staff access only.", "danger")
        return redirect(url_for('home'))
    form = ServiceForm()
    mechanics = db.get_mechanics()
    form.mechanic_id.choices = [(m['employee_id'], m['name']) for m in mechanics]

    if form.validate_on_submit():
        success = db.process_service(
            vehicle_id=form.vehicle_id.data,
            customer_id=form.customer_id.data,
            mechanic_id=form.mechanic_id.data,
            mileage_in=form.mileage_in.data,
            mileage_out=form.mileage_out.data,
            estimate=form.preliminary_estimate.data,
            work_done=form.work_done.data
        )
        if success:
            flash('Service ticket successfully logged and mechanic assigned!', 'success')
            return redirect(url_for('database'))
        else:
            flash('Transaction failed. Check that the Vehicle and Customer IDs exist.', 'danger')
            
    return render_template('service_vehicle.html', form=form)


@app.route('/billing', methods=['GET', 'POST'])
@login_required
def billing():
    # Only employees should be able to process billing, so we check their user_type before showing the form
    if current_user.role != 'billing':
        flash("Unauthorized: Staff access only.", "danger")
        return redirect(url_for('home'))
    form = BillingForm()
    if form.validate_on_submit():
        success = db.process_payment(
            ticket_type=form.ticket_type.data,
            ticket_id=form.ticket_id.data,
            amount=form.amount.data,
            payment_method=form.payment_method.data
        )
        if success:
            flash(f'Payment of ${form.amount.data} processed successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Transaction failed. Check that the Ticket ID exists!', 'danger')
            
    return render_template('billing.html', form=form)


@app.route('/customer_lookup')
@login_required
def customer_lookup():
    # 1. Security Check: Only Employees allowed
    if current_user.user_type != 'employee':
        flash("Unauthorized: Customer Database is restricted to staff.", "danger")
        return redirect(url_for('home'))

    # 2. Grab the search query if they typed one
    search_query = request.args.get('search_query', '')
    customers = []

    # 3. If they searched for something, query the database
    if search_query:
        customers = db.search_customers(search_query)

    return render_template('customer_lookup.html', customers=customers, search_query=search_query)

@app.route('/reports')
@login_required
def reports():
    # Security: Only Employees can view financial/operational reports
    if current_user.user_type != 'employee':
        flash("Unauthorized: Managerial Reports are restricted to staff.", "danger")
        return redirect(url_for('home'))

    # Fetch the math from the database
    stats = db.get_operational_report()
    
    return render_template('reports.html', stats=stats)










if __name__ == '__main__':
    app.run(debug=True)