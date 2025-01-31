from flask import Flask, request, jsonify, send_from_directory, abort
import os
import json
import webbrowser
import threading
import requests
import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)

JSON_FILE = 'data.json'

if not os.path.exists(JSON_FILE):
    with open(JSON_FILE, 'w') as file:
        json.dump({}, file) 

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/data', methods=['GET'])
def get_data():
    with open(JSON_FILE, 'r') as file:
        data = json.load(file)
    return jsonify(data), 200

@app.route('/submit', methods=['POST'])
def submit():
    new_data = request.json
    with open(JSON_FILE, 'r+') as file:
        file_data = json.load(file)
        file_data.update(new_data)
        file.seek(0)
        json.dump(file_data, file, indent=4)
        file.truncate() 
    return jsonify({"message": "Data saved successfully"}), 200

@app.route('/<path:filename>')
def serve_static_files(filename):
    if os.path.exists(os.path.join('static', filename)):
        return send_from_directory('static', filename)
    else:
        return abort(404)

if __name__ == '__main__':
    webbrowser.open("http:/127.0.0.1:5000")
    app.run(port=5000)

