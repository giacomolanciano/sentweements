import eventlet
eventlet.monkey_patch()
from flask import Flask, render_template, send_file, request
from flask_socketio import SocketIO
from tweets_rest import ImageRetriever
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
sio = SocketIO(app, async_mode='eventlet')

threads = dict()


def background_job(sid, query_params):
    image_stream = ImageRetriever(sio, sid, query_params)
    image_stream.search_api_request()


@app.route('/')
def index():
    """Serve the client-side application."""
    if len(request.args):  # we have at least a search argument
        init_params = {
            'query': request.args.get('query'),
            'since_date': request.args.get('since_date'),
            'until_date': request.args.get('until_date'),
            'language': request.args.get('language'),
            'location': request.args.get('location')
        }
        print(json.dumps(init_params))
        # return the basic result page skeleton
        return render_template('query_results.html', init_params=json.dumps(init_params))
    else:
        # return send_file('index.html')  # return the homepage
        return send_file('query_results_skeleton.html')  # return the homepage


@sio.on('connect')
def on_connect():
    sid = request.sid
    print('Client connected:', sid)


@sio.on('init')
def on_init(msg):
    sid = request.sid
    obj = json.loads(msg)
    print('Client:', sid)
    print('Params:', msg)
    print('Object:', obj)
    gt = eventlet.greenthread.spawn(background_job, sid, obj)
    threads[sid] = gt


@sio.on('disconnect')
def on_disconnect():
    sid = request.sid
    print('Client disconnected:', sid)

    # on disconnect we destroy the corresponding thread
    gt = threads.pop(sid)
    gt.kill()


if __name__ == '__main__':
    sio.run(app, debug=True, port=5000)
