from flask import Flask
from flask_cors import CORS
#from flask_socketio import SocketIO, emit

app = Flask(__name__)
CORS(app)
cors = CORS(app, resource={r"/*": {"origins": "*"}})

UPLOAD_FOLDER = 'uploads'

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER