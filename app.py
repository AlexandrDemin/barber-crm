#! /home/devel/anaconda2/envs/py35/bin/python3.6
# -*- coding: utf-8 -*-

from flask import Flask, abort, url_for, render_template, request, Response, current_app, send_from_directory
import json
from flask_cors import CORS
from clickhouse_driver import Client
from backend_logic import *
import codecs
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from functools import wraps
import gc


app = Flask(__name__, static_folder='./front/dist/static/', template_folder="./front/dist/")
CORS(app)

def check_auth(username, password):
    if username == 'offeruser' and password == 'D_f$7u-SVX9v"h;j':
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

@app.route("/api/GetRivals/", methods=['POST'])
@requires_auth
def get_rivals():
    if request.method == "POST":
        startTime = datetime.now()
        request_text = request.data
        ipStr = request.remote_addr
        userName = 'unknown'
        try: 
            result = subprocess.run(['nbtscan', ipStr], stdout=subprocess.PIPE)
            userName = result.stdout.decode('utf-8').split(ipStr)[2].split(' ')[2]
        except:
            pass
        data = json.loads(request_text)
        offerid = data['offerid']
        if offerid[:7] == 'http://':
            offerid = offerid[7:].split('/')[3]
        elif '/' in offerid:
            offerid = offerid.split('/')[3]
        maxRivalsCount = int(data['maxRivalsCount'])
        sqiDiffCoef = int(data['sqiDiffCoef'])
        maxPos = int(data['maxPos'])
        minCountInSerm = int(data['minCountInSerm'])
        keywords, rivals, startDate, keywordsStr, regionsStr, regions = getRivalsAndData(offerid, maxRivalsCount, sqiDiffCoef, maxPos, minCountInSerm)
        res = {
            'keywords': keywords,
            'rivals': rivals,
            'startDate': startDate,
            'keywordsStr': keywordsStr,
            'regionsStr': regionsStr,
            'regions': regions,
            'offerid': offerid
        }
        res_to_save = res
        res_to_save['maxRivalsCount'] = maxRivalsCount
        res_to_save['sqiDiffCoef'] = sqiDiffCoef
        res_to_save['maxPos'] = maxPos
        res_to_save['minCountInSerm'] = minCountInSerm
        saveFilterRivalsObject(res_to_save)
        endTime = datetime.now()
        writeLog({
            "timestamp": startTime.strftime('%d.%m.%Y %H:%M:%S'),
            'ip': request.remote_addr,
            'userName': userName,
            "requestSeconds": (endTime-startTime).total_seconds(),
            'method': 'GetRivals',
            "requestData": request_text.decode('utf-8')
        })
        return json.dumps(res, ensure_ascii=False), 200, {'Content-Type': 'application/json; charset=utf-8'}
 
@app.route("/api/LoadData/", methods=['POST'])
@requires_auth
def load_data():
    if request.method == "POST":
        startTime = datetime.now()
        request_text = request.data
        ipStr = request.remote_addr
        userName = 'unknown'
        try: 
            result = subprocess.run(['nbtscan', ipStr], stdout=subprocess.PIPE)
            userName = result.stdout.decode('utf-8').split(ipStr)[2].split(' ')[2]
        except:
            pass
        data = json.loads(request_text)
        offerid = data['offerid']
        res = getFilterRivalsObjectByOfferId(offerid)
        res.pop('_id', None)
        endTime = datetime.now()
        writeLog({
            "timestamp": startTime.strftime('%d.%m.%Y %H:%M:%S'),
            'ip': request.remote_addr,
            'userName': userName,
            "requestSeconds": (endTime-startTime).total_seconds(),
            'method': 'LoadData',
            "offerid": offerid
        })
        return json.dumps(res, ensure_ascii=False), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route("/api/GetKeywordsRivals/", methods=['POST'])
@requires_auth
def get_keywords_rivals():
    if request.method == "POST":
        startTime = datetime.now()
        request_text = request.data
        ipStr = request.remote_addr
        userName = 'unknown'
        try: 
            result = subprocess.run(['nbtscan', ipStr], stdout=subprocess.PIPE)
            userName = result.stdout.decode('utf-8').split(ipStr)[2].split(' ')[2]
        except:
            pass
#         try:
        data = json.loads(request_text)
        keywords = data['keywords']
        rivals = data['rivals']
        maxPos = data['maxPos']
        startDate = data['startDate']
        keywordsStr = data['keywordsStr']
        regionsStr = data['regionsStr']
        regions = data['regions']
        minCountInSerm = data['minCountInSerm']
        offerid = data['offerid']
        all_keywords, notRivals = getKeywordsRivals(keywords, rivals, maxPos, startDate, keywordsStr, regionsStr, regions, minCountInSerm)
#         except:
#             res = {'error': True}
        saveKeywords(offerid, all_keywords, rivals, notRivals)
        endTime = datetime.now()
        writeLog({
            "timestamp": startTime.strftime('%d.%m.%Y %H:%M:%S'),
            'ip': request.remote_addr,
            'userName': userName,
            "requestSeconds": (endTime-startTime).total_seconds(),
            'method': 'GetKeywordsRivals',
            'offerid': offerid
        })
        return json.dumps({'keywords': all_keywords, 'notRivals': notRivals}, ensure_ascii=False), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route("/api/GetKeywordsToRemove/", methods=['POST'])
@requires_auth
def get_keywords_to_remove():
    if request.method == "POST":
        startTime = datetime.now()
        request_text = request.data
        ipStr = request.remote_addr
        userName = 'unknown'
        try: 
            result = subprocess.run(['nbtscan', ipStr], stdout=subprocess.PIPE)
            userName = result.stdout.decode('utf-8').split(ipStr)[2].split(' ')[2]
        except:
            pass
#         try:
        data = json.loads(request_text)
        keywords = data['keywords']
        regions = data['regions']
        minKeywordRivals = int(data['minKeywordRivals'])
        offerid = data['offerid']
        res = getKeywordsToRemove(keywords, minKeywordRivals, regions)
#         except:
#             res = {'error': True}
        saveKeywordsToRemove(offerid, res, minKeywordRivals)
        endTime = datetime.now()
        writeLog({
            "timestamp": startTime.strftime('%d.%m.%Y %H:%M:%S'),
            'ip': request.remote_addr,
            'userName': userName,
            "requestSeconds": (endTime-startTime).total_seconds(),
            'method': 'GetKeywordsToRemove',
            'offerid': offerid
        })
        return json.dumps(res, ensure_ascii=False), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route("/api/GetSerm/", methods=['POST'])
@requires_auth
def get_serm():
    if request.method == "POST":
        startTime = datetime.now()
        request_text = request.data
        ipStr = request.remote_addr
        userName = 'unknown'
        try: 
            result = subprocess.run(['nbtscan', ipStr], stdout=subprocess.PIPE)
            userName = result.stdout.decode('utf-8').split(ipStr)[2].split(' ')[2]
        except:
            pass
#         try:
        data = json.loads(request_text)
        keyword = data['keyword']
        regionId = data['regionId']
        searchEngine = data['searchEngine']
        isMobile = data['isMobile']
        maxPos = int(data['maxPos'])
        startDate = data['startDate']
        rivals = data['rivals']
        regions = data['regions']
        notRivals = data['notRivals']
        res = getSerm(keyword, regionId, searchEngine, isMobile, maxPos, startDate, rivals, regions, notRivals)
#         except:
#             res = {'error': True}
        endTime = datetime.now()
        writeLog({
            "timestamp": startTime.strftime('%d.%m.%Y %H:%M:%S'),
            'ip': request.remote_addr,
            'userName': userName,
            "requestSeconds": (endTime-startTime).total_seconds(),
            'method': 'GetKeywordsToRemove'
        })
        return json.dumps(res, ensure_ascii=False), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route("/api/ExportToExcel/", methods=['POST'])
@requires_auth
def export_to_excel():
    if request.method == "POST":
        startTime = datetime.now()
        request_text = request.data
        ipStr = request.remote_addr
        userName = 'unknown'
        try: 
            result = subprocess.run(['nbtscan', ipStr], stdout=subprocess.PIPE)
            userName = result.stdout.decode('utf-8').split(ipStr)[2].split(' ')[2]
        except:
            pass
#         try:
        data = json.loads(request_text)
        offerid = data['offerid']
        maxRivalsCount = int(data['maxRivalsCount'])
        keywords = data['keywords']
        regions = data['regions']
        minKeywordRivals = int(data['minKeywordRivals'])
        sqiDiffCoef = int(data['sqiDiffCoef'])
        maxPos = int(data['maxPos'])
        minCountInSerm = int(data['minCountInSerm'])
        keywordsToRemove = data['keywordsToRemove']
        rivals = data['rivals']
        filename = 'Rivals ' + offerid + ' ' + startTime.strftime('%d.%m.%y %H-%M-%S') + '.xlsx'
        info = [{
            'Id КП': offerid,
            'Макс. кол-во конкурентов': maxRivalsCount,
            'Макс. отклонение ИКС': sqiDiffCoef,
            'Макс. позиция для поиска конкурентов': maxPos,
            'Мин. кол-во раз, сколько сайт должен встречаться в выдаче, чтобы считаться конкурентом': minCountInSerm,
            'Мин. кол-во конкурентов для запроса': minKeywordRivals
        }]
        keywordsToDeleteForExcel = []
        for item in keywordsToRemove:
            for key in item['keywordsToDelete']:
                keywordsToDeleteForExcel.append({
                    'Регион': item['region'],
                    'Ключ для удаления': key
                })
        writer = pd.ExcelWriter('./downloadable_files/' + filename)
        info_df = pd.DataFrame(info)
        info_df.to_excel(writer, index=False, sheet_name='Метаданные', freeze_panes = (1,0))
        regions_df = pd.DataFrame(regions).rename(columns={'name': 'Регион'})['Регион'].to_frame()
        regions_df.to_excel(writer, index=False, sheet_name='Регионы', freeze_panes = (1,0))
        rivals_df = pd.DataFrame(rivals).rename(columns={
            'domain': 'Сайт',
            'isExcluded': 'Не конкурент',
            'countInSerm': 'Встречается в выдаче',
        })[['Сайт', 'Не конкурент', 'Встречается в выдаче']]
        rivals_df.to_excel(writer, index=False, sheet_name='Конкуренты', freeze_panes = (1,0))
        all_keywords_df = pd.DataFrame(keywords).rename(columns={
            'keyword': 'Запрос',
            'regionName': 'Регион',
            'searchEngine': 'ПС',
            'isMobile': 'Мобильная выдача',
            'rivalsCount': 'Кол-во конкурентов'
        })[['Запрос', 'Кол-во конкурентов', 'Регион', 'ПС', 'Мобильная выдача']]
        all_keywords_df.to_excel(writer, index=False, sheet_name='Запросы', freeze_panes = (1,0))
        keywordsToDeleteForExcel_df = pd.DataFrame(keywordsToDeleteForExcel)
        keywordsToDeleteForExcel_df.to_excel(writer, index=False, sheet_name='Запросы для удаления', freeze_panes = (1,0))
        writer.save()
#         except:
#             res = {'error': True}
        endTime = datetime.now()
        writeLog({
            "timestamp": startTime.strftime('%d.%m.%Y %H:%M:%S'),
            'ip': request.remote_addr,
            'userName': userName,
            "requestSeconds": (endTime-startTime).total_seconds(),
            'method': 'GetKeywordsToRemove'
        })
        return filename

@app.route("/api/GetDomainInfo/", methods=['POST'])
@requires_auth
def get_domain_info():
    if request.method == "POST":
        data = json.loads(request.data)
        domain = data['domain'].replace('https://', '').replace('http://', '').replace('www.', '')
        r = requests.get('http://192.168.4.158:8911/' + domain)
        res = r.json()
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8901, debug=True)
