from flask import Flask, jsonify
from routes.routes import bp_routes
from routes.test_routes import test_routes
from helper import getFreshTimeStamp

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    return app

app = create_app()  # Creating the app

# Registering the blueprint
app.register_blueprint(bp_routes)
app.register_blueprint(test_routes)

# reloading with timestamp time
print(f"\n================  Reloaded at: {getFreshTimeStamp(timezone='Asia/Kolkata') }  ===================\n")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("5000"), debug=True)