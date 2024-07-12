from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource, fields
from datetime import datetime, timedelta
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

app = Flask(__name__)
app.config['SECRET_KEY']= '11f280828a3c4cb689bf7011c8b44feb'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_database.db'
db = SQLAlchemy()
db.init_app(app)

api = Api(app, version='1.0', title='MHI API', description='MHI API documentation')
ns = api.namespace('api/v1', description="Version 1.0 API's of MHI")
api.authorizations = {
    'api_key': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

from Login import route
from Signup import route
from Dashboard import route