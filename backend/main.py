from flask import Flask, jsonify, request
from flask_cors import CORS #For connection between flask and Vue
import mysql.connector #For connecting database

app = Flask(__name__)

CORS(app, resources={r'/*':{'origins':"*"}})
#Connect to MySQL and create cursor to make queries
db = mysql.connector.connect(host="localhost", user="root", database="biologicalmodelswebapp", password="030103")

@app.route("/Account", methods=["GET", "POST"])
def Account():
    #Track server response, initially set no error codes
    response_object = {"server status":"success", "username_error": False, "email_error": False}
    cursor = db.cursor()
    if request.method == "POST": #Adding user
        post_data = request.get_json() #Retrieve payload from client
        #Check username and email are unique
        multi_query = \
            "SELECT EXISTS(SELECT * FROM users WHERE username = %s); \
            SELECT EXISTS(SELECT * FROM users WHERE email = %s);"
        results = cursor.execute(multi_query, (post_data.get("username") , post_data.get("email")), multi = True)
        query_results = [] #Store results of two query statements (bools)
        for result in results:
            query_results.append(result.fetchone()[0])
        if query_results[0] == False and query_results[1] == False: #If username/email don't already exist
            #Insert user details into database
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s,%s,%s)", \
            (post_data.get("username").lower(), post_data.get("email").lower(), post_data.get("password")))
            db.commit()
            cursor.close()
            response_object["message"] = "User added"
        else: #Username or email already exist
            cursor.close()
            response_object["message"] = "User not added, not unique"
            if query_results[0] == True: #username already in use
                response_object["username_error"] = True
            if query_results[1] == True: #email already in use
                response_object["email_error"] = True
    else: #Get method: retrieving user details
        response_object["user"] = "User data fetched"

    return jsonify(response_object)

if __name__ == "__main__":
    app.run(debug = True)