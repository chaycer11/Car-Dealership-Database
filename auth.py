from flask import Blueprint, render_template, redirect, url_for, flash
from forms import RegistrationForm, LoginForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Later, we will add the Flask-WTF form logic here!
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # Later, we will add the database insertion logic here!
    form = RegistrationForm()

    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success') 
        return redirect(url_for('database'))
  
    return render_template('register.html', form=form)

@auth_bp.route('/logout')
def logout():
    # Logic to clear the user's session
    form = LoginForm()

    if form.validate_on_submit():
        flash(f'Logged in as {form.username.data}!', 'success')
        return redirect(url_for('database'))

    return render_template('login.html', form=form)