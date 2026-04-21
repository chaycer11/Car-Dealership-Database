from flask import Flask, render_template
import mysql.connector
import os
from dotenv import load_dotenv

app = Flask(__name__)

def get_db_connection():
    connection = mysql.connector.connect(
        host=os.environ.get('DB_HOST'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASS'),
        database=os.environ.get('DB_NAME'),
        port=os.environ.get('DB_PORT')
    )
    return connection




@app.route('/')
def database():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM Vehicle')
        Vehicle = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('index.html', cars=Vehicle)
    except Exception as e:
        return f"<h1> System online but failed to connect to database </h1> <p> Error: {e} </p>"

if __name__ == '__main__':
    app.run(debug=True)