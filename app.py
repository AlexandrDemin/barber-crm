#! /home/devel/anaconda2/envs/py35/bin/python3.6
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

@app.route("/api/GetProjects/", methods=['POST'])
@requires_auth
def get_projects():
    if request.method == "POST":
        startTime = datetime.now()
        projects = getProjects()
        endTime = datetime.now()
        writeLog({
            "timestamp": startTime.strftime('%d.%m.%Y %H:%M:%S'),
            'ip': request.remote_addr,
            "requestSeconds": (endTime-startTime).total_seconds(),
            'method': 'GetProjects'
        })
        return json.dumps(projects, ensure_ascii=False), 200, {'Content-Type': 'application/json; charset=utf-8'}
 
@app.route("/api/GetProject/", methods=['POST'])
@requires_auth
def get_project():
    if request.method == "POST":
        startTime = datetime.now()
        request_text = request.data
        data = json.loads(request_text)
        projectId = data['projectId']
        res = getProject(projectId)
        endTime = datetime.now()
        writeLog({
            "timestamp": startTime.strftime('%d.%m.%Y %H:%M:%S'),
            "requestSeconds": (endTime-startTime).total_seconds(),
            'method': 'GetProject',
            "projectId": projectId
        })
        return json.dumps(res, ensure_ascii=False), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route("/api/GetSemcore/", methods=['POST'])
@requires_auth
def get_semcore():
    if request.method == "POST":
        startTime = datetime.now()
        request_text = request.data
        data = json.loads(request_text)
        domain = data['domain']
        directions = data['priority'].split('\n')
        regions = data['regions']
        max_count = data['maxQueries']
        minus_words = data['minusWords'].split('\n')
        minus_phrases = data['minusPhrases'].split('\n')
        res = getSemCore(domain, directions, regions, max_count, minus_words, minus_phrases)
        endTime = datetime.now()
        writeLog({
            "timestamp": startTime.strftime('%d.%m.%Y %H:%M:%S'),
            "requestSeconds": (endTime-startTime).total_seconds(),
            'method': 'GetSemcore'
        })
        return json.dumps(res, ensure_ascii=False), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route("/api/DownloadSemcore/", methods=['POST'])
@requires_auth
def download_semcore():
    if request.method == "POST":
        startTime = datetime.now()
        request_text = request.data
        data = json.loads(request_text)
        sem_core = data['semCore']
        df = pd.DataFrame(sem_core)
        filename = 'semcore ' + str(random.random())[2:] + '.xlsx'
        df.to_excel('./downloadable_files/' + filename)
        endTime = datetime.now()
        writeLog({
            "timestamp": startTime.strftime('%d.%m.%Y %H:%M:%S'),
            "requestSeconds": (endTime-startTime).total_seconds(),
            'method': 'DownloadSemcore'
        })
        return json.dumps({'filename': filename}, ensure_ascii=False), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route("/api/GetTerec/", methods=['POST'])
@requires_auth
def get_terec():
    if request.method == "POST":
        startTime = datetime.now()
        request_text = request.data
        data = json.loads(request_text)
        urls = data['urls'].split('\n')
        queries = data['queries'].split('\n')
        res = {}
        for url in urls:
            url_res = getTerec(url, queries)
            res[url] = getTerec(url, queries)
        endTime = datetime.now()
        writeLog({
            "timestamp": startTime.strftime('%d.%m.%Y %H:%M:%S'),
            "requestSeconds": (endTime-startTime).total_seconds(),
            'method': 'GetTerec'
        })
        return json.dumps(res, ensure_ascii=False), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route("/api/DownloadTerec/", methods=['POST'])
@requires_auth
def download_terec():
    if request.method == "POST":
        startTime = datetime.now()
        request_text = request.data
        data = json.loads(request_text)
        terec = data['terec']
        terec_words = []
        for url in terec:
            for word in terec[url]:
                word['url'] = url
                terec_words.append(word)
        df = pd.DataFrame(terec_words)
        filename = 'terec' + str(random.random())[2:] + '.xlsx'
        df.to_excel('./downloadable_files/' + filename)
        endTime = datetime.now()
        writeLog({
            "timestamp": startTime.strftime('%d.%m.%Y %H:%M:%S'),
            "requestSeconds": (endTime-startTime).total_seconds(),
            'method': 'DownloadTerec'
        })
        return json.dumps({'filename': filename}, ensure_ascii=False), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route("/api/GetConversionForecast/", methods=['POST'])
@requires_auth
def get_conversion_forecast():
    if request.method == "POST":
        startTime = datetime.now()
        file = request.files['file']
        df = pd.read_excel(file)
        res = getConversionForecast(df['Запросы'].tolist())
        endTime = datetime.now()
        writeLog({
            "timestamp": startTime.strftime('%d.%m.%Y %H:%M:%S'),
            "requestSeconds": (endTime-startTime).total_seconds(),
            'method': 'GetConversionForecast'
        })
        return json.dumps(res, ensure_ascii=False), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route("/api/DownloadConversionForecast/", methods=['POST'])
@requires_auth
def download_conversion():
    if request.method == "POST":
        startTime = datetime.now()
        request_text = request.data
        data = json.loads(request_text)
        data = data['data']
        df = pd.DataFrame(data)
        filename = 'conversions ' + str(random.random())[2:] + '.xlsx'
        df.to_excel('./downloadable_files/' + filename)
        endTime = datetime.now()
        writeLog({
            "timestamp": startTime.strftime('%d.%m.%Y %H:%M:%S'),
            "requestSeconds": (endTime-startTime).total_seconds(),
            'method': 'DownloadConversionForecast'
        })
        return json.dumps({'filename': filename}, ensure_ascii=False), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route("/api/GetTopTimeForecast/", methods=['POST'])
@requires_auth
def get_time_to_top_forecast():
    if request.method == "POST":
        startTime = datetime.now()
        file = request.files['file']
        df = pd.read_excel(file)
        res = getTopTimeForecast(df['Запросы'].tolist())
        endTime = datetime.now()
        writeLog({
            "timestamp": startTime.strftime('%d.%m.%Y %H:%M:%S'),
            "requestSeconds": (endTime-startTime).total_seconds(),
            'method': 'GetTopTimeForecast'
        })
        return json.dumps(res, ensure_ascii=False), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route("/api/DownloadTimeToTopForecast/", methods=['POST'])
@requires_auth
def download_time_to_top():
    if request.method == "POST":
        startTime = datetime.now()
        request_text = request.data
        data = json.loads(request_text)
        data = data['data']
        df = pd.DataFrame(data)
        filename = 'time to top ' + str(random.random())[2:] + '.xlsx'
        df.to_excel('./downloadable_files/' + filename)
        endTime = datetime.now()
        writeLog({
            "timestamp": startTime.strftime('%d.%m.%Y %H:%M:%S'),
            "requestSeconds": (endTime-startTime).total_seconds(),
            'method': 'DownloadTimeToTopForecast'
        })
        return json.dumps({'filename': filename}, ensure_ascii=False), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route("/api/GetTrafficForecast/", methods=['POST'])
@requires_auth
def get_traffic():
    if request.method == "POST":
        startTime = datetime.now()
        file = request.files['file']
        df = pd.read_excel(file)
        traffic_data = df.to_dict('records')
        res = []
        for item in traffic_data:
            res.append({
                'query': item['Запрос'],
                'demand': item['Спрос'],
                'targetPosition': item['Целевая позиция'],
                'traffiForecast': round(getTrafficForecast([item['Спрос']], item['Целевая позиция'])[0], 2)
            })
        endTime = datetime.now()
        writeLog({
            "timestamp": startTime.strftime('%d.%m.%Y %H:%M:%S'),
            "requestSeconds": (endTime-startTime).total_seconds(),
            'method': 'GetTrafficForecast'
        })
        return json.dumps(res, ensure_ascii=False), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route("/api/DownloadTrafficForecast/", methods=['POST'])
@requires_auth
def download_traffic():
    if request.method == "POST":
        startTime = datetime.now()
        request_text = request.data
        data = json.loads(request_text)
        data = data['data']
        df = pd.DataFrame(data)
        filename = 'traffic ' + str(random.random())[2:] + '.xlsx'
        df.to_excel('./downloadable_files/' + filename)
        endTime = datetime.now()
        writeLog({
            "timestamp": startTime.strftime('%d.%m.%Y %H:%M:%S'),
            "requestSeconds": (endTime-startTime).total_seconds(),
            'method': 'DownloadTrafficForecast'
        })
        return json.dumps({'filename': filename}, ensure_ascii=False), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route("/api/GetAdTexts/", methods=['POST'])
@requires_auth
def get_ad_texts():
    if request.method == "POST":
        startTime = datetime.now()
        file = request.files['file']
        domain = request.form['domain']
        df = pd.read_excel(file)
        texts_data = df.to_dict('records')
        queries = []
        for item in texts_data: {
            queries.append({
               "QueryCleanForm": item['Запрос'],
               "QueryNormalWords": item['Запрос'].split(' '),
               "Url": item['Страница'],
               'NeedGenerateText': True
           })
        }
        res = getAdTexts(domain, queries)
        endTime = datetime.now()
        writeLog({
            "timestamp": startTime.strftime('%d.%m.%Y %H:%M:%S'),
            "requestSeconds": (endTime-startTime).total_seconds(),
            'method': 'GetAdTexts'
        })
        return json.dumps(res, ensure_ascii=False), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route("/api/DownloadAdTexts/", methods=['POST'])
@requires_auth
def download_ad_texts():
    if request.method == "POST":
        startTime = datetime.now()
        request_text = request.data
        data = json.loads(request_text)
        data = data['data']
        df = pd.DataFrame(data)
        filename = 'ad texts ' + str(random.random())[2:] + '.xlsx'
        df.to_excel('./downloadable_files/' + filename)
        endTime = datetime.now()
        writeLog({
            "timestamp": startTime.strftime('%d.%m.%Y %H:%M:%S'),
            "requestSeconds": (endTime-startTime).total_seconds(),
            'method': 'DownloadAdTexts'
        })
        return json.dumps({'filename': filename}, ensure_ascii=False), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route("/api/GetMetaTags/", methods=['POST'])
@requires_auth
def get_meta_tags():
    if request.method == "POST":
        startTime = datetime.now()
        file = request.files['file']
        domain = request.form['domain']
        df = pd.read_excel(file)
        texts_data = df.to_dict('records')
        queries = []
        for item in texts_data: {
            queries.append({
               "Query": item['Запрос'],
               "Url": item['Страница'],
               'RegionId': item['ID региона']
           })
        }
        print(queries)
        res = getMetatags(domain, queries)
        print(res)
        for query, texts in zip(queries, res):
            texts['Query'] = query['Query']
            texts['RegionId'] = query['RegionId']
            if texts['Description'] == '':
                texts['Description'] = query['Query']
            if texts['Title'] == '':
                texts['Title'] = query['Query']
        endTime = datetime.now()
        writeLog({
            "timestamp": startTime.strftime('%d.%m.%Y %H:%M:%S'),
            "requestSeconds": (endTime-startTime).total_seconds(),
            'method': 'GetMetaTags'
        })
        return json.dumps(res, ensure_ascii=False), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route("/api/DownloadMetaTags/", methods=['POST'])
@requires_auth
def download_meta_tags():
    if request.method == "POST":
        startTime = datetime.now()
        request_text = request.data
        data = json.loads(request_text)
        data = data['data']
        df = pd.DataFrame(data)
        filename = 'ad texts ' + str(random.random())[2:] + '.xlsx'
        df.to_excel('./downloadable_files/' + filename)
        endTime = datetime.now()
        writeLog({
            "timestamp": startTime.strftime('%d.%m.%Y %H:%M:%S'),
            "requestSeconds": (endTime-startTime).total_seconds(),
            'method': 'DownloadMetaTags'
        })
        return json.dumps({'filename': filename}, ensure_ascii=False), 200, {'Content-Type': 'application/json; charset=utf-8'}

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8903, debug=True)
