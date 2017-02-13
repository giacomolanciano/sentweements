import eventlet
eventlet.monkey_patch()
from flask import Flask, render_template, send_file, request
from flask_socketio import SocketIO, emit
from tweets_rest import ImageRetriever

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
sio = SocketIO(app, async_mode='eventlet')

threads = dict()


def background_job(sid):
    image_stream = ImageRetriever(sio, sid, query)
    image_stream.search_api_request()
    # while True:
    #     update = [1,2,3] #{'hi': 'hello', 'ciao': 'salve'}  # update object, TODO: insert call to blocking function here
    #     sio.emit('update', update, room=sid)
    #     sio.sleep(10)


@app.route('/')
def index():
    """Serve the client-side application."""
    query = request.args.get('query')
    # since_date = request.args.get('since_date')
    # until_date = request.args.get('until_date')
    # language = request.args.get('language')
    # location = request.args.get('location')

    if len(request.args):  # we have at least a search argument
        # return the basic result page skeleton
        # return render_template('query_results.html', query=query, time=elapsed, results=results)
        return send_file('stub.html')  # return a stub client page
    else:
        return send_file('index.html')  # return the homepage


@sio.on('connect')
def on_connect():
    sid = request.sid
    print('Client connected:', sid)
    gt = eventlet.greenthread.spawn(background_job, sid)
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
