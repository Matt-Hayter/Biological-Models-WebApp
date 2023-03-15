from flask import Flask
from flask_cors import CORS #For connection between flask and Vue
import mysql.connector #For connecting database
import os

application = Flask(__name__) #Define app within init -> used throughout program

CORS(application)

#Connect to MySQL and create cursor to make queries. os env variables to disguise db information
db = mysql.connector.connect(
    user = os.environ["MODEL_VISUALISER_RDB_USER"],
    database = os.environ["MODEL_VISUALISER_RDB_NAME"],
    host = os.environ["MODEL_VISUALISER_RDB_HOST"],
    port = os.environ["MODEL_VISUALISER_RDB_PORT"],
    password = os.environ["MODEL_VISUALISER_RDB_PASSWORD"])

#Import Blueprints here to avoid circular imports
from biological_models_app.user.routes import user
from biological_models_app.pred_prey.routes import pred_prey
from biological_models_app.competing_species.routes import competing_species
from biological_models_app.SIR.routes import SIR
from biological_models_app.SEIDR.routes import SEIDR

application.register_blueprint(user)
application.register_blueprint(pred_prey)
application.register_blueprint(competing_species)
application.register_blueprint(SIR)
application.register_blueprint(SEIDR)
    