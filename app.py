from flask import Flask, render_template, url_for, redirect
import db
from dotenv import load_dotenv
from auth import auth_bp

app = Flask(__name__)

app.config['SECRET_KEY'] = 'd757a259ea5d51bd40f2eaff47aad6ae'

app.register_blueprint(auth_bp)

@app.route('/')
def index():
    return redirect(url_for('auth.register'))

@app.route('/home')
def home():
    return render_template('base.html')


@app.route('/vehicles')
def database():
    vehicles = db.get_all_vehicles()
    try:
        return render_template('index.html', cars=vehicles)
    except Exception as e:
        return f"<h1> System online but failed to connect to database </h1> <p> Error: {e} </p>"

if __name__ == '__main__':
    app.run(debug=True)