from flask import Flask
from flask_cors import CORS #For connection between flask and Vue
import mysql.connector #For connecting database
from dotenv import load_dotenv #For env vars when run locally in development
load_dotenv() #Search .env file for env vars. In deployment, .env ignored -> searches host instead
import os

application = Flask(__name__) #Define app within init -> used throughout program

CORS(application)
#Connect to MySQL and create cursor to make queries.
db = mysql.connector.connect(
    user = os.environ["MODEL_VISUALISER_RDB_USER"], #env vars from .env in development, and host in deployment
    database = os.environ["MODEL_VISUALISER_RDB_NAME"],
    host = os.environ["MODEL_VISUALISER_RDB_HOST"],
    port = os.environ["MODEL_VISUALISER_RDB_PORT"],
    password = os.environ["MODEL_VISUALISER_RDB_PASSWORD"])

#Import Blueprints here to avoid circular imports
from biological_models_app.user.routes import user
from biological_models_app.pred_prey.routes import pred_prey
from biological_models_app.competing_species.routes import competing_species
from biological_models_app.sir.routes import SIR
from biological_models_app.seidr.routes import SEIDR

application.register_blueprint(user)
application.register_blueprint(pred_prey)
application.register_blueprint(competing_species)
application.register_blueprint(SIR)
application.register_blueprint(SEIDR)
    