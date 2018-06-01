import os
import logging

from flask import Flask

logger = logging.getLogger('root')

def create_app():
    config = os.getenv('FLASK_CONFIG') or 'Development'

    app = Flask(__name__)
    app.config.from_object('config.{}'.format(config))
    logger.info('********************* Environment: {} *********************'.format(config))

    from tsclient.api import api
    app.register_blueprint(api, url_prefix='/api/v1')

    return app
