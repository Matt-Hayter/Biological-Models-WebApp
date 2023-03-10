from biological_models_app import db
from flask import jsonify, request, Blueprint
import argon2 #For salted hashing
from datetime import datetime

user = Blueprint("user", __name__, url_prefix="/Account")

salted_hasher = argon2.PasswordHasher(
                time_cost=3, # number of iterations
                memory_cost=64 * 1024, # Units of KB -> 64MB
                parallelism=1, # how many parallel threads to use
                hash_len=32, # the size of the derived key
                salt_len=16 # the size of the random generated salt in bytes
            )

@user.route("/SignUp", methods=["POST"])
def sign_up():
    #Track server response, initially set no error codes
    response = {"server status": "success", "username": None}
    cursor = db.cursor()
    SignUp_data = request.get_json() #Retrieve payload from client
    #Check username and email are individually unique
    multi_query = \
        "SELECT EXISTS(SELECT * FROM users WHERE username = %s); \
        SELECT EXISTS(SELECT * FROM users WHERE email = %s);"
    results = cursor.execute(multi_query, (SignUp_data.get("username").lower(),
        SignUp_data.get("email").lower()), multi = True)
    query_results = [] #Store results of two query statements (bools)
    for result in results:
        query_results.append(result.fetchone()[0])
    if query_results[0] == False and query_results[1] == False: #If username/email don't already exist
        #Insert user details into database
        username = SignUp_data.get("username").lower()
        email = SignUp_data.get("email").lower()
        query = "INSERT INTO users (username, email, priv_info) VALUES (%s,%s,%s)"
        #Salted hashing of password (one-way) for database storage, using the argon2i algorithm
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
def sign_in():
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
        response["message"] = "User account not found"
    return jsonify(response)

@user.route("/ChangeUsername", methods=["PUT"])
def change_username():
    #Track server response, initially set no error codes
    response = {"server status": "success"}
    cursor = db.cursor()
    username_change_data = request.get_json() #Retrieve payload from client
    new_username = username_change_data.get("newUsername").lower()
    #Check username is unique
    query = "SELECT EXISTS(SELECT * FROM users WHERE username = %s);"
    cursor.execute(query, (new_username,))
    if cursor.fetchone()[0] == False: #If username doesn't already exist
        #Change username in database
        query = "UPDATE users SET username = %s WHERE email = %s"
        cursor.execute(query, (new_username, username_change_data.get("email").lower()))
        db.commit()
        cursor.close()
        response["message"] = "Username updated"
        #Return new username
        response["username"] = new_username
    else: #Username or email already exist
        cursor.close()
        response["message"] = "Username not updated, not unique"
        response["username_error"] = True
    return jsonify(response)

@user.route("/DeleteAccount", methods=["PUT"])
def delete_account():
    response = {"server status": "success"}
    cursor = db.cursor()
    request_data = request.get_json() #Retrieve payload from client
    #Get user's id (primary key)
    query = "SELECT id FROM users WHERE email = %s;"
    cursor.execute(query, (request_data.get("email").lower(),))
    user_id = cursor.fetchone()[0]
    if not user_id: #If email isn't found in database
        raise ValueError
    #Delete account and presets from tables
    query = "DELETE FROM pred_prey_presets WHERE owner_id = %s; \
        DELETE FROM competing_species_presets WHERE owner_id = %s; \
        DELETE FROM sir_presets WHERE owner_id = %s; \
        DELETE FROM seidr_presets WHERE owner_id = %s; \
        DELETE FROM users WHERE id = %s;"
    query_results = cursor.execute(query, (user_id, user_id, user_id, user_id, user_id), multi=True)
    for result in query_results: #Clear cursor results
        result.fetchall()
    db.commit()
    cursor.close()
    response["message"] = "Account and presets deleted!"
    return jsonify(response)
