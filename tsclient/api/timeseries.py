import logging

from flask import jsonify, request, json
from predix.data import timeseries

from tsclient.api import api, tag_validation, datapoints_validation

logger = logging.getLogger(__name__)

ts = timeseries.TimeSeries()


@api.route('/tags/', methods=['GET'])
def get_tags():
    return jsonify(ts.get_tags())


@api.route('/lastest/', methods=['POST'])
@tag_validation
def get_latest():
    tags = request.get_json(force=True, silent=True)
    return jsonify(ts.get_latest(tags=tags['tags']))


@api.route('/datapoints/', methods=['POST'])
@tag_validation
def get_datapoints():
    tags = request.get_json(force=True, silent=True)
    return jsonify(ts.get_datapoints(tags=tags['tags'], start='5y-ago', limit=10000))


@api.route('/ingest/', methods=['POST'])
@datapoints_validation
def send_datapoints():
    datapoints = request.get_json(force=True, silent=True)['datapoints']
    for datapoint in datapoints:
        ts.queue(**datapoint)
    return jsonify(json.loads(ts.send()))
