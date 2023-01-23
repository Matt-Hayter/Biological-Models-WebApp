from flask import Flask, jsonify, request
from flask_cors import CORS #For connection between flask and Vue
import mysql.connector #For connecting database

app = Flask(__name__)

CORS(app, resources={r'/*':{'origins':"*"}})
#Connect to MySQL and create cursor to make queries
db = mysql.connector.connect(host="localhost", user="root", database="biologicalmodelswebapp", password="030103")

@app.route("/SignUp", methods=["POST"])
def SignUp():
    #Track server response, initially set no error codes
    response_object = {"server status": "success", "username": None}
    cursor = db.cursor()
    post_data = request.get_json() #Retrieve payload from client
    if request.method == "POST": #Adding user
        #Check username and email are individually unique
        multi_query = \
            "SELECT EXISTS(SELECT * FROM users WHERE username = %s); \
            SELECT EXISTS(SELECT * FROM users WHERE email = %s);"
        results = cursor.execute(multi_query, (post_data.get("username") , post_data.get("email")), multi = True)
        query_results = [] #Store results of two query statements (bools)
        for result in results:
            query_results.append(result.fetchone()[0])
        if query_results[0] == False and query_results[1] == False: #If username/email don't already exist
            #Insert user details into database
            username = post_data.get("username").lower() #Used twice so assign temp variable
            query = "INSERT INTO users (username, email, priv_info) VALUES (%s,%s,%s)"
            cursor.execute(query, (username, post_data.get("email").lower(), post_data.get("password")))
            db.commit()
            cursor.close()
            response_object["message"] = "User added"
            #Return username once added to log in
            response_object["username"] = username
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
        query = "SELECT * FROM users WHERE email = %s AND priv_info= %s"
        cursor = db.cursor()
        cursor.execute(query, (SignIn_data.get("email").lower() , SignIn_data.get("password")))
        if cursor.fetchone() != None: #If email, password combination exists
            query = "SELECT username FROM users WHERE email = %s AND priv_info = %s"
            cursor.execute(query, (SignIn_data.get("email") , SignIn_data.get("password")))
            response_object["username"] = cursor.fetchone()[0]
            cursor.close()
            response_object["message"] = "User account found"
        else: #If email password combination not found, username key remains as None  
            cursor.close()  
            response_object["message"] = "User account not found"
    return jsonify(response_object)

if __name__ == "__main__":
    app.run(debug = True)