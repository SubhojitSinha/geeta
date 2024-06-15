from flask import Blueprint
from controllers.test_controller import *
from helper import getFreshTimeStamp

test_routes = Blueprint('test_routes', __name__, url_prefix='/test')
test_routes.route('/implementation', methods=['POST'])(test_implementation)