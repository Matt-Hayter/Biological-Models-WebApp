from flask import Flask, jsonify
from flask_cors import CORS #For connection between flask and Vue

app = Flask(__name__)

CORS(app, resources={r'/*':{'origins':"*"}})

#Base route, with default GET method
@app.route('/')
def base():
    return ("Hello world")

if __name__ == "__main__":
    app.run(debug = True)