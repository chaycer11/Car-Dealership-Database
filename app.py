from flask import Flask, render_template
import db
from dotenv import load_dotenv

app = Flask(__name__)


@app.route('/')
def database():
    vehicles = db.get_all_vehicles()
    try:
        return render_template('index.html', cars=vehicles)
    except Exception as e:
        return f"<h1> System online but failed to connect to database </h1> <p> Error: {e} </p>"

if __name__ == '__main__':
    app.run(debug=True)