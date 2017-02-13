import eventlet
eventlet.monkey_patch()
from flask import Flask, send_file, request
from flask_socketio import SocketIO
from tweets_rest import ImageRetriever

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
sio = SocketIO(app, async_mode='eventlet')

threads = dict()


def background_job(sid):
    image_stream = ImageRetriever(sio, sid, 'ciao')
    image_stream.search_api_request()
    # while True:
    #     update = [1,2,3] #{'hi': 'hello', 'ciao': 'salve'}  # update object, TODO: insert call to blocking function here
    #     sio.emit('update', update, room=sid)
    #     sio.sleep(10)


@app.route('/')
def index():
    # return send_file('index.html')
    return send_file('stub.html')


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
