from flask import Flask, jsonify, request
from flask_cors import CORS #For connection between flask and Vue
import mysql.connector #For connecting database

app = Flask(__name__)

CORS(app, resources={r'/*':{'origins':"*"}})
#Connect to MySQL and create cursor to make queries
db = mysql.connector.connect(host="localhost", user="root", database="biologicalmodelswebapp", password="030103")
cursor = db.cursor()

@app.route("/Account", methods=["GET", "POST"])
def Account():
    response_object = {"status":"success"} #Track server response
    if request.method == "POST":
        post_data = request.get_json() #Retrieve payload from client
        #Insert user details into database
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s,%s,%s)", \
            (post_data.get("username"), post_data.get("email"), post_data.get("password")))
        db.commit()
        response_object["message"] = "User added"
    else:
        response_object["user"] = "User data fetched"

    return jsonify(response_object)

if __name__ == "__main__":
    app.run(debug = True)