import time

from flask import Flask, send_file, request

from tweets_rest import ImageRetriever

app = Flask(__name__)


@app.route('/')
def root():
    query = request.args.get('query')
    since_date = request.args.get('since_date')
    until_date = request.args.get('until_date')
    language = request.args.get('language')
    location = request.args.get('location')
    if query:
        start_time = time.time()

        ir = ImageRetriever(query, since_date, until_date, language, location)
        # TODO start request

        elapsed = time.time() - start_time
        # return render_template('query_results.html', query=query, time=elapsed, results=results)
    else:
        return send_file('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')  # set debug to True to allow auto-reloading during development
