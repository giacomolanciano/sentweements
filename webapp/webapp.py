import __init__  # update Python PATH
from datetime import datetime, timedelta

import json
from flask import Flask, send_file, request

import persistence
from tweets_streaming import SQLITE_DATETIME_FORMAT

DEFAULT_SINCE = 7
CLIENT_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

app = Flask(__name__)


@app.route('/')
def index():
    return send_file('leaflet_italy_choropleth.html')


@app.route('/italy_regions.js')
def italy_regions():
    return send_file('italy_regions.js')


@app.route('/italy_regions/')
def italy_regions_get_data():
    since_str = request.args.get('since')
    until_str = request.args.get('until')

    if since_str:
        since = datetime.strptime(since_str, CLIENT_DATETIME_FORMAT)
    else:
        since = datetime.today() - timedelta(days=DEFAULT_SINCE)

    if until_str:
        until = datetime.strptime(until_str, CLIENT_DATETIME_FORMAT).strftime(SQLITE_DATETIME_FORMAT)
    else:
        until = datetime.now().strftime(SQLITE_DATETIME_FORMAT)

    # Query the db to obtain the data
    db_response = persistence.get_regions_stats(since.strftime(SQLITE_DATETIME_FORMAT), until)

    # Dump to JSON string and send it
    json_data = json.dumps(db_response)
    return json_data


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')  # set debug to True to allow auto-reloading during development
