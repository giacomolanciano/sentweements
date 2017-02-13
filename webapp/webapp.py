import eventlet
eventlet.monkey_patch()
from flask import Flask, render_template, send_file, request
from flask_socketio import SocketIO, emit
from tweets_rest import ImageRetriever

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
sio = SocketIO(app, async_mode='eventlet')

pool = eventlet.GreenPool(1000)
subprocesses = dict()


def background_job(sid):
    image_stream = ImageRetriever(sio, sid, 'ciao')
    image_stream.search_api_request()
    # while True:
    #     update = [1,2,3] #{'hi': 'hello', 'ciao': 'salve'}  # update object, TODO: insert call to blocking function here
    #     sio.emit('update', update, room=sid)
    #     sio.sleep(10)


@app.route('/')
def index():
    return send_file('stub.html')


@sio.on('connect')
def on_connect():
    sid = request.sid
    print('Client connected:', sid)
    pool.spawn_n(background_job, sid)
    # t = threading.Thread(name=sid, target=background_job, args=(sid,))
    # subprocesses[sid] = t
    # t.start()


@sio.on('disconnect')
def on_disconnect():
    sid = request.sid
    print('Client disconnected:', sid)
    # on disconnect we destroy the corresponding thread
    # t = subprocesses.pop(sid)
    # #t.terminate()


if __name__ == '__main__':
    sio.run(app, debug=True, port=5000)
