from flask import Flask, render_template, send_file, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    """Serve the client-side application."""
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

# @socketio.on('connect')
# def on_connect():
#     pass

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@socketio.on('my event')
def test_message(message):
    emit('my response', {'data': 'got it!'})

if __name__ == '__main__':
    socketio.run(app)
