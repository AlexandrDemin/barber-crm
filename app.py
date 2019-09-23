#! python3
# -*- coding: utf-8 -*-

from flask import Flask, abort, url_for, render_template, request, Response, current_app, send_from_directory
import json
from flask_cors import CORS
from backend_logic import *
import os
from functools import wraps
import time
from werkzeug.utils import secure_filename
import pandas as pd

app = Flask(__name__, static_folder='./front/dist/static/', template_folder="./front/dist/")
CORS(app)

def check_auth(username, password):
    if username == 'demo.user' and password == 'demo':
        return True
    return False

def authenticate():
    return Response(
    'Некорректный логин и пароль. Пожалуйста, перезапустите браузер, и попробуйте ещё раз.', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

def writeLog(logEntry):
    with codecs.open("log.txt", "a", "utf-8") as logFile:
        json.dump(logEntry, logFile, ensure_ascii=False)
        logFile.write('\n')
        
def connect(host,database,user,password,query):
        conn = psycopg2.connect(host="localhost",database="barbers", user="read_only", password="User_ro")
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute(query)
            result = cur.fetchall()
            cur.close()
            conn.close()
            
            if len(result_data) == 0:
                return {'error':'Нет таких данных'}
            else:
                result = result_data[0]
                return result

        except Exception as e:
            return [{'Error':e}]

@app.route("/api/Test/", methods=['POST', 'GET'])
@requires_auth
def get_projects():
    if request.method == "GET":
        return 'Please, use HTTP POST for this API'
    if request.method == "POST":
        startTime = datetime.now()
        data = json.loads(request.data)
        res = getData()
        endTime = datetime.now()
        writeLog({
            "timestamp": startTime.strftime('%d.%m.%Y %H:%M:%S'),
            'ip': request.remote_addr,
            "requestSeconds": (endTime-startTime).total_seconds(),
            'method': 'GetProjects'
        })
        return json.dumps(res, ensure_ascii=False), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/static/<path:path>')
@requires_auth
def send_files(path):
    return send_from_directory(app.static_folder, path)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
@requires_auth
def front(path):
    return render_template('index.html')

@app.errorhandler(404)
@requires_auth
def page_not_found(e):
    return "Page not found", 404

@app.route('/download/<path:filename>')
@requires_auth
def download(filename):
    directory = os.path.join(current_app.root_path, './downloadable_files/')
    return send_from_directory(directory=directory, filename=filename, as_attachment=True)

@app.route('/api/GetUserData/', methods=['POST'])
def GetUserData():
    if request.method == 'POST':
        data = request.get_json()
        login = data['login']
        query = f"""select name,"pictureUrl",roles from _user where login = '{login}'"""                
        result = connect("localhost","barbers","read_only","User_ro",query)
        return result

#добавить операции
@app.route('/api/GetCurrentSession/', methods=['POST'])
def GetCurrentSession():
    if request.method == 'POST':
        data = request.get_json()
        officeid = data['id']        
        query = f"""select * from session where state = 'open' and "officeId" = {officeid}"""               
        result_data = connect("localhost","barbers","read_only","User_ro",query)
        
        if len(result_data) == 0:
            return {'error':'Нет таких данных'}
        else:
            return result_data[0]
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
