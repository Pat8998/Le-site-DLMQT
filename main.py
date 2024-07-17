from flask import url_for, Flask, request, json, jsonify, render_template, send_from_directory, redirect, make_response
import os
from flask_sock import Sock
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from static.alias import *
import hashlib
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
    if request.cookies.get('pwd') == '43568a72689a2759140dfb25d2301912913e5c2d54d450fc55389acacb8ab1dc':
        return render_template('main.html')
    else:
        return redirect(url_for('login_page'))

@app.route('/login')
def login_page():
	return render_template('Connection.html')


@app.route('/loginscript', methods=['GET'])
def Login():
    login = request.args.get('login')
    hash_obj = hashlib.sha256()
    hash_obj.update(login.encode('utf-8'))
    hash_obj.update(hash_obj.hexdigest().encode('utf-8'))
    print(hash_obj.hexdigest())
    if hash_obj.hexdigest() == '43568a72689a2759140dfb25d2301912913e5c2d54d450fc55389acacb8ab1dc' :
        response = make_response("Login OK")
        response.set_cookie('pwd', hash_obj.hexdigest())
        return response
    else:
        return "Login not OK :"+login

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
    

@app.route('/change_priority')
def change_priority():
    device = request.args.get('device')
    priority = request.args.get('priority')
    pvalue = request.args.get('previousvalue')
    print(pvalue)
    server_change_priority(device, priority, pvalue)
    try:
        return 'Success'
    except:
        return 'Fail'





if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6969)
