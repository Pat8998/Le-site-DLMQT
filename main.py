from flask import url_for, Flask, request, json, jsonify, render_template, send_from_directory, redirect
import os
from static.Check_MAC import *
from flask_sock import Sock
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from static.alias import *
import json
import time

app = Flask(__name__)
sockets = Sock(app)
websockets = []

# Path to your JSON file
json_file_path = os.path.join(os.path.dirname(__file__), 'database')

class JSONFileEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        else:
            print('json_updated')
            for ws in websockets:
                try:
                    ws.send('json_updated')
                except:
                    websockets.remove(ws)

@sockets.route('/ws')
def echo_socket(ws):
    websockets.append(ws)
    try:
        while True:
            message = ws.receive()
            if message:
                print('Client said:', message)
    finally:
        websockets.remove(ws)

# Start observing the JSON file for changes
event_handler = JSONFileEventHandler()
observer = Observer()
observer.schedule(event_handler, path=json_file_path, recursive=False)
observer.start()

@app.route('/')
def home():
    if Check_MAC(request.remote_addr):
        return render_template('main.html')
    else:
        return redirect("https://youtu.be/dQw4w9WgXcQ")
    
@app.route('/database/database.json')
def get_json():
    return send_from_directory('database', "database.json")

@app.route('/static/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')


@app.route('/ip')
def get_ip():
    return request.host.split(':')[0]

@app.route('/disconnect', methods=['GET'])
def disconnect():
    device = request.args.get('device')
    try:
        Disconnect(device)
        return 'Success'
    except:
        return 'Fail'

if __name__ == '__main__':
    # threading.Thread(target=start_sniffing, daemon=True).start()
    app.run(debug=True, host='0.0.0.0', port=6969)
