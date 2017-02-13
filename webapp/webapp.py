import multiprocessing

from flask import Flask, render_template, send_file, request
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
subprocesses = {}


def background_job():
    # ir = ImageRetriever()
    # ir.search_api_request()
    pass


@app.route('/')
def index():
    """Serve the client-side application."""
    query = request.args.get('query')
    since_date = request.args.get('since_date')
    until_date = request.args.get('until_date')
    language = request.args.get('language')
    location = request.args.get('location')

    if len(request.args):  # we have at least a search argument
        t = multiprocessing.Process(name=request.sid, target=background_job)
        subprocesses[request.sid] = t
        t.start()

        # return the basic result page skeleton
        return render_template('query_results.html', query=query, time=elapsed, results=results)
    else:
        return send_file('index.html')  # return the homepage


# @socketio.on('connect')
# def on_connect():
#     pass


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')
    # on disconnect we destroy the corresponding thread
    t = subprocesses.pop(request.sid)
    t.terminate()


# @socketio.on('my event')
# def test_message(message):
#     emit('my response', {'data': 'got it!'})


if __name__ == '__main__':
    socketio.run(app)
