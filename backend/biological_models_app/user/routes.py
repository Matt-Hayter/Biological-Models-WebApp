from biological_models_app import db
from flask import jsonify, request, Blueprint
import argon2 #For salted hashing
from datetime import datetime

user = Blueprint("user", __name__)

salted_hasher = argon2.PasswordHasher(
                time_cost=3, # number of iterations
                memory_cost=64 * 1024, # Units of KB -> 64MB
                parallelism=1, # how many parallel threads to use
                hash_len=32, # the size of the derived key
                salt_len=16 # the size of the random generated salt in bytes
            )

@user.route("/SignUp", methods=["POST"])
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

@user.route("/SignIn", methods=["POST"])
def SignIn():
    print("here")
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
