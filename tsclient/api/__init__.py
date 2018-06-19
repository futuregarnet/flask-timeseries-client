from os import path
from functools import wraps

from flask import Blueprint, jsonify, json, request
from flask import current_app as app

from jsonschema import Draft4Validator, FormatChecker

api = Blueprint('api', __name__)


def tag_validation(route):
    @wraps(route)
    def validate_tags(*args, **kwargs):
        with open(path.join(app.config['APP_DIRECTORY'], 'resources/schemas/tags.json'), 'r') as schema_json:
            tags_schema = json.loads(schema_json.read())

        tags = request.get_json(force=True, silent=True)
        if tags is not None:
            tags_validator = Draft4Validator(tags_schema)
            errors = sorted(tags_validator.iter_errors(tags), key=lambda e: e.path)
            if len(errors) > 0:
                return jsonify(errors=[error.message for error in errors]), 400
        else:
            return jsonify(errors='Missing tags JSON.'), 400
        return route(*args, **kwargs)
    return validate_tags

def datapoints_validation(route):
    @wraps(route)
    def validate_datapoints(*args, **kwargs):
        with open(path.join(app.config['APP_DIRECTORY'], 'resources/schemas/datapoints.json'), 'r') as schema_json:
            tags_schema = json.loads(schema_json.read())

        tags = request.get_json(force=True, silent=True)
        if tags is not None:
            tags_validator = Draft4Validator(tags_schema, format_checker=FormatChecker())
            errors = sorted(tags_validator.iter_errors(tags), key=lambda e: e.path)
            if len(errors) > 0:
                return jsonify(errors=[error.message for error in errors]), 400
        else:
            return jsonify(errors='Missing datapoints JSON.'), 400
        return route(*args, **kwargs)
    return validate_datapoints


from tsclient.api import timeseries
