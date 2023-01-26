from flask import Flask, jsonify, request
from flask_cors import CORS #For connection between flask and Vue
import mysql.connector #For connecting database
import argon2 #For salted hashing
from datetime import datetime

app = Flask(__name__)

CORS(app, resources={r'/*':{'origins':"*"}})
#Connect to MySQL and create cursor to make queries
db = mysql.connector.connect(host="localhost", user="root", database="biologicalmodelswebapp", password="030103")
salted_hasher = argon2.PasswordHasher(
                time_cost=3, # number of iterations
                memory_cost=64 * 1024, # Units of KB -> 64MB
                parallelism=1, # how many parallel threads to use
                hash_len=32, # the size of the derived key
                salt_len=16 # the size of the random generated salt in bytes
            )

@app.route("/SignUp", methods=["POST"])
def SignUp():
    #Track server response, initially set no error codes
    response = {"server status": "success", "username": None}
    cursor = db.cursor()
    SignUp_data = request.get_json() #Retrieve payload from client
    if request.method == "POST": #Adding user
        #Check username and email are individually unique
        multi_query = \
            "SELECT EXISTS(SELECT * FROM users WHERE username = %s); \
            SELECT EXISTS(SELECT * FROM users WHERE email = %s);"
        results = cursor.execute(multi_query, (SignUp_data.get("username") , SignUp_data.get("email")), multi = True)
        query_results = [] #Store results of two query statements (bools)
        for result in results:
            query_results.append(result.fetchone()[0])
        if query_results[0] == False and query_results[1] == False: #If username/email don't already exist
            #Insert user details into database
            username = SignUp_data.get("username").lower()
            email = SignUp_data.get("email").lower()
            query = "INSERT INTO users (username, email, priv_info) VALUES (%s,%s,%s)"
            #Salted hashing of password (one-way) for database storage, using the argonid algorithm
            hash = salted_hasher.hash(SignUp_data.get("password")) #Apply salted hashing
            cursor.execute(query, (username, SignUp_data.get("email").lower(), hash))
            db.commit()
            cursor.close()
            response["message"] = "User added"
            #Return username once added to log in
            response["username"] = username
            response["email"] = email
        else: #Username or email already exist
            cursor.close()
            response["message"] = "User not added, not unique"
            if query_results[0] == True: #username already in use
                response["username_error"] = True
            if query_results[1] == True: #email already in use
                response["email_error"] = True
    return jsonify(response)

@app.route("/SignIn", methods=["POST"])
def SignIn():
    if request.method == "POST":
        response = {"server status": "success", "username": None}
        SignIn_data = request.get_json() #Retrieve payload from client
        #Check email is present in db. If so, extract hashed password
        query = "SELECT username, email, priv_info FROM users WHERE email = %s" #Emails are unique
        cursor = db.cursor()
        cursor.execute(query, (SignIn_data.get("email").lower(),))
        query_result = cursor.fetchone()
        cursor.close()
        try: 
            if query_result == None: #If inputted email doesn't exist
                raise ValueError
            db_username = query_result[0]
            db_email = query_result[1]
            db_hashed_passwd = query_result[2]
            #One-way hash inputted password to see if it matches db records. If no match, raises exception
            verify_result = salted_hasher.verify(db_hashed_passwd, SignIn_data.get("password"))
            #If passed without exceptions:
            response["username"] = db_username
            response["email"] = db_email
            response["message"] = "User account found and logged in"
        except:
            cursor.close()  
            response["message"] = "User account not found"
    return jsonify(response)

@app.route("/PredPrey/AddPresets", methods=["POST"])
def add_PredPrey_preset():
    response = {"server status": "success"}
    preset = request.get_json() #Retrieve payload from client
    if request.method == "POST": #Adding a preset
        #First get id of user with active email
        query = "SELECT id FROM users WHERE email = %s"
        cursor = db.cursor()
        cursor.execute(query, (preset.get("userEmail"),))
        activeid = cursor.fetchone()[0]
        presetData = preset.get("presetData")
        #Now insert preset into presets table, with the correct Foreign key
        query = "INSERT INTO pred_prey_presets (owner_id, preset_name, N0, a, b, P0, c, d, date) \
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,NOW())"
        cursor.execute(query, (activeid, preset.get("presetName"), presetData[0], presetData[1],
            presetData[2], presetData[3], presetData[4], presetData[5]))
        cursor.close()
        db.commit()
        response["message"] = "Added PredPrey preset"
    return jsonify(response)

@app.route("/PredPrey/AllPresets", methods=["POST"])
def all_PredPrey_presets():
    response = {"server status": "success"}
    post_data = request.get_json()
    if request.method == "POST": #Grab user's presets
        #First get user id, given email
        query = "SELECT id FROM users WHERE email = %s"
        cursor = db.cursor()
        cursor.execute(query, (post_data.get("userEmail"),))
        activeid = cursor.fetchone()[0]
        #Now grab all pred prey presets for that user
        query = "SELECT preset_name, date FROM pred_prey_presets WHERE owner_id = %s"
        cursor.execute(query, (activeid,))
        response["presets"] = cursor.fetchall()
        cursor.close()
        response["message"] = "Grabbed all of user's pred-prey presets"
    return jsonify(response)

@app.route("/PredPrey/PresetParams", methods=["POST"])
def get_PredPrey_preset():
    response = {"server status": "success"}
    post_data = request.get_json()
    if request.method == "POST":
        #First get user id, given email
        query = "SELECT id FROM users WHERE email = %s"
        cursor = db.cursor()
        cursor.execute(query, (post_data.get("userEmail"),))
        activeid = cursor.fetchone()[0]
        #Now grab data for requested preset
        query = "SELECT N0, a, b, P0, c, d FROM pred_prey_presets WHERE owner_id = %s AND preset_name = %s"
        cursor.execute(query, (activeid, post_data.get("presetName")))
        response["preset_params"] = cursor.fetchone()
        print(response["preset_params"])
        cursor.close()
        response["message"] = "Grabbed data for selected pred prey preset"
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug = True)
    