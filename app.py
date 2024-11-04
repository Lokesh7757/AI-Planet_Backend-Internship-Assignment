from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
socketio = SocketIO(app)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET'])
def home():
    return "Welcome to the PDF Upload Service", 200

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({"message": "File uploaded successfully", "filename": filename}), 201
    else:
        return jsonify({"error": "Only PDF files are allowed"}), 400

# WebSocket endpoint
@socketio.on('connect')
def handle_connect():
    print("Client connected")
    emit('message', {"message": "Connected to WebSocket"})

@socketio.on('message')
def handle_message(data):
    # Assume data contains JSON with filename and question
    print(f"Received message: {data}")
    # Process the data here and emit a response
    emit('response', {"answer": "Here is a response to your question"})

if __name__ == '__main__':
    app.run(debug=True)