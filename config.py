import os

from werkzeug import security
from flask import json

APP_DIRECTORY = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = security.gen_salt(32)
    DEBUG = False
    TESTING = False
    APP_DIRECTORY = APP_DIRECTORY
    PROTOCOL = 'http'


class Development(Config):
    DEBUG = True

    with open(os.path.join(APP_DIRECTORY, 'config.json')) as config_json:
        config = json.loads(config_json.read())

    for env_variable, value in config.items():
        if env_variable == 'PREDIX_DATA_TIMESERIES_ZONE_ID':
            os.environ['PREDIX_DATA_TIMESERIES_INGEST_ZONE_ID'] = value
            os.environ['PREDIX_DATA_TIMESERIES_QUERY_ZONE_ID'] = value
        else:
            os.environ[env_variable] = value

class Testing(Config):
    TESTING = True


class Predix(Config):
    PROTOCOL = 'https'
