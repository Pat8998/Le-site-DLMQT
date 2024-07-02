from flask import url_for, Flask, request, json, jsonify, render_template, send_from_directory
import os
from flask_sock import Sock
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import json
import time

app = Flask(__name__)
sockets = Sock(app)
send_message = False
# Path to your JSON file
json_file_path = os.path.join(os.path.dirname(__file__), 'database')
class JSONFileEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        else:
            print('json_updated')
            global WebSock
            WebSock.send('json_updated')
            time.sleep(0.5)


@sockets.route('/ws')
def echo_socket(ws):
    while True:
        global WebSock
        WebSock =ws
        message = ws.receive()
        if message:
            print('Client said:', message)
        


# Start observing the JSON file for changes
event_handler = JSONFileEventHandler()
observer = Observer()
observer.schedule(event_handler, path=json_file_path, recursive=False)
observer.start()

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/database/database.json')
def get_json():
    return send_from_directory('database', "database.json")



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='20079')
