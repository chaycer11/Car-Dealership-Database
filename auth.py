from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from forms import LoginForm, RegistrationForm # Use your existing forms
import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.authenticate_user(form.email.data, form.password.data, form.user_type.data)
        if user:
            login_user(user)
            flash(f'Welcome back, {user.name}!', 'success')
            return redirect(url_for('home'))
        flash('Invalid Name or Password.', 'danger')
    return render_template('login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        success = db.create_customer(
            name=form.name.data,
            phone=form.phone.data,
            email=form.email.data,
            address=form.address.data,
            password=form.password.data 
        )
        
        if success:
            flash('Your account has been created! You can now log in.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Something went wrong. Email might already be in use.', 'danger')
            
    return render_template('register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))