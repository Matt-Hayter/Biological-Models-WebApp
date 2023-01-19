from flask import Flask, jsonify
from flask_cors import CORS #For connection between flask and Vue
import mysql.connector

app = Flask(__name__)

CORS(app, resources={r'/*':{'origins':"*"}})
#Connect to MySQL and create cursor to make queries
db = mysql.connector.connect(host="localhost", user="root", database="biologicalmodelswebapp")
cursor = db.cursor()

#Base route
"""
@app.route("/")
def undefined():
    return ("Not yet defined!")

@app.route("/PredatorPrey", methods=["POST"])
def pred_prey():
"""


if __name__ == "__main__":
    app.run(debug = True)