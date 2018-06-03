import os

from werkzeug import security
from flask import json


class Config:
    SECRET_KEY = security.gen_salt(32)
    DEBUG = False
    TESTING = False
    APP_DIRECTORY = os.path.abspath(os.path.dirname(__file__))

    @staticmethod
    def load_local_config():
        """
        Load Environment Variables needed for Python Predix SDK from config.json
        :return: None
        """
        config_filename = os.path.join(Config.APP_DIRECTORY, 'config.json')
        if os.path.exists(config_filename):
            with open(os.path.join(Config.APP_DIRECTORY, 'config.json')) as config_json:
                config = json.loads(config_json.read())

            for env_variable, value in config.items():
                if env_variable == 'PREDIX_DATA_TIMESERIES_ZONE_ID':
                    os.environ['PREDIX_DATA_TIMESERIES_INGEST_ZONE_ID'] = value
                    os.environ['PREDIX_DATA_TIMESERIES_QUERY_ZONE_ID'] = value
                else:
                    os.environ[env_variable] = value


class Development(Config):
    DEBUG = True

    Config.load_local_config()


class Testing(Config):
    TESTING = True

    Config.load_local_config()


class Predix(Config):
    # Set Predix Service Labels
    uaa_label = 'predix-uaa'
    ts_label = 'predix-timeseries'

    # Must check even if not running in this environment
    if 'VCAP_SERVICES' in os.environ:
        vcap_services = json.loads(os.environ['VCAP_SERVICES'])

        uaa_credentials = vcap_services[uaa_label][0]['credentials']
        ts_credentials = vcap_services[ts_label][0]['credentials']

        # Set Environment Variables needed for Python Predix SDK
        os.environ['PREDIX_SECURITY_UAA_URI'] = uaa_credentials['uri']
        os.environ['PREDIX_DATA_TIMESERIES_INGEST_ZONE_ID'] = ts_credentials['ingest']['zone-http-header-value']
        os.environ['PREDIX_DATA_TIMESERIES_INGEST_URI'] = ts_credentials['ingest']['uri']
        os.environ['PREDIX_DATA_TIMESERIES_QUERY_ZONE_ID'] = ts_credentials['query']['zone-http-header-value']
        os.environ['PREDIX_DATA_TIMESERIES_QUERY_URI'] = ts_credentials['query']['uri']
