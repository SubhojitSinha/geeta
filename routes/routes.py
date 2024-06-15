from flask import Blueprint
from controllers.test import *
bp_routes = Blueprint('blueprint', __name__)

bp_routes.route('/', methods=['GET'])(hello_world)