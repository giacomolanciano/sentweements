import __init__  # update Python PATH
from flask import Flask, render_template, send_file, request
import sys
import os.path
import time

app = Flask(__name__)


@app.route('/')
def root():
    query = request.args.get('query')
    if query:
        start_time = time.time()
        results = None
        elapsed = time.time() - start_time
        return render_template('query_results.html', query=query, time=elapsed, results=results)
    else:
        return send_file('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')  # set debug to True to allow auto-reloading during development
