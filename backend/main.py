from flask import Flask, jsonify, request
from flask_cors import CORS #For connection between flask and Vue
import mysql.connector #For connecting database
import argon2 #For salted hashing

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
    response_object = {"server status": "success", "username": None}
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
            response_object["message"] = "User added"
            #Return username once added to log in
            response_object["username"] = username
            response_object["email"] = email
        else: #Username or email already exist
            cursor.close()
            response_object["message"] = "User not added, not unique"
            if query_results[0] == True: #username already in use
                response_object["username_error"] = True
            if query_results[1] == True: #email already in use
                response_object["email_error"] = True
    return jsonify(response_object)

@app.route("/SignIn", methods=["POST"])
def SignIn():
    if request.method == "POST":
        response_object = {"server status": "success", "username": None}
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
            response_object["username"] = db_username
            response_object["email"] = db_email
            response_object["message"] = "User account found and logged in"
        except:
            cursor.close()  
            response_object["message"] = "User account not found"
    return jsonify(response_object)

@app.route("/PredPrey/presets", methods=["GET", "POST"])
def add_PredPrey_preset():
    response_object = {"server status": "success"}
    preset_data = request.get_json() #Retrieve payload from client
    if request.method == "POST": #Adding a preset
        #First get id of user with active email
        query = "SELECT id from users WHERE email = %s"
        cursor = db.cursor()
        cursor.execute(query, (preset_data.get("userEmail"),))
        activeid = cursor.fetchone()[0]
        presetData = preset_data.get("presetData")
        #Now insert preset into presets table, with the correct Foreign key
        query = "INSERT INTO pred_prey_presets (owner_id, preset_name, N0, a, b, P0, c, d, date) \
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,now())"
        cursor.execute(query, (activeid, preset_data.get("presetName"), presetData["N0"], presetData["a"],
            presetData["b"], presetData["P0"], presetData["c"], presetData["d"]))
        cursor.close()
        db.commit()
        response_object["message"] = "Added PredPrey preset"
    return jsonify(response_object)

if __name__ == "__main__":
    app.run(debug = True)
    