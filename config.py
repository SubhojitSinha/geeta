import os

# Each Flask web application contains a secret key
# which used to sign session cookies for protection
# against cookie data tampering.
SECRET_KEY = os.urandom(32)

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    SECRET_KEY = SECRET_KEY
    BASEDIR    = basedir
    # REDIS      = {
    #     "LOCAL":{
    #         "HOST": "redis",
    #         "PORT": "6379",
    #         "SSL" : False
    #     },
    #     "PROD": {
    #         "HOST": "proxy-app-extension-cache-pbx6uq.serverless.use1.cache.amazonaws.com",
    #         "PORT": "6379",
    #         "SSL" : True
    #     }
    # }
    DATABASE   = {
        "LOCAL":{
            "HOST"  : "mongodb",
            "PORT"  : "27017",
            "NAME"  : "geeta-db",
            "USER"  : "root",
            "PASS"  : "pass",
            "SUFFIX": "authSource=admin"
        },
        # "PROD":{
        #     "HOST"  : "document-db-path.amazonaws.com",
        #     "PORT"  : "27017",
        #     "NAME"  : "geeta-db",
        #     "USER"  : "root",
        #     "PASS"  : "password",
        #     "SUFFIX": "ssl=true&tlsCAFile=global-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false"
        # }
    }
    