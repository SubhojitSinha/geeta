from flask import Flask
from flask_pymongo import PyMongo
from os import environ

# Create a Flask application
app = Flask(__name__)

# Check if the environment is development or production
# and load environment variables from a config file
env_verb   = "LOCAL" if environ['FLASK_ENV'] == 'development' else "PROD"
app.config.from_object('config.BaseConfig')

# Get the database name, host, port, username, and
# password from environment variables
database   = app.config['DATABASE'][env_verb]
mongo_db   = database["NAME"]
mongo_host = database["HOST"]
mongo_port = database["PORT"]
mongo_user = database["USER"]
mongo_pass = database["PASS"]
mongo_sfx  = database["SUFFIX"]

# Construct the MongoDB connection string
mongo_url = f"mongodb://{mongo_user}:{mongo_pass}@{mongo_host}:{mongo_port}/{mongo_db}?{mongo_sfx}"
print('MONGO_URL: ', mongo_url)

app.config["MONGO_URI"] = mongo_url

mongo = PyMongo(app)
db    = mongo.db

def DB():
    return mongo.db

def check_mongo_connection():
    """
    Function to check the MongoDB connection.
    """
    try:
        # Attempt to list all the collections in the database
        collections = mongo.db.list_collection_names()

        return {
            'status'     : True,
            'collections': collections,
            'message'    : 'MongoDB connection successful'
        }
    except Exception as e:
        return {
            'status': False,
            'message': str(e)
        }