from flask import Flask, send_file, request
import json

import __init__  # update Python PATH

app = Flask(__name__)

@app.route('/')
def index():
    return send_file('leaflet_italy_choropleth.html')


@app.route('/italy_regions.js')
def italy_regions():
    return send_file('italy_regions.js')


@app.route('/italy_regions/')
def italy_regions_get_data():
    since = request.args.get('since')
    if not since:
        since = ''  # insert default date value here (e.g. 7 days ago)

    # Query the db to obtain the data
    db_response = ''

    # Parse the data into a dictionary
    data = {}

    # Dump to JSON string and send it
    json_data = json.dumps(data)
    return json_data


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')  # set debug to True to allow auto-reloading during development