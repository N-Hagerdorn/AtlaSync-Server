from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/room')
def room():
    # Get room
    # Get floor from room.floor_id
    # Get floor map
    # Get building
    # Get organization
    return None


@app.route('/floor')
def floor():
    return None


app.run(host='192.168.0.5', port=5001, debug=True, threaded=False)