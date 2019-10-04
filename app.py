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
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__, static_folder='./front/dist/static/', template_folder="./front/dist/")
CORS(app)

def check_auth(username, password):
    if username == 'demo.user' and password == 'demo':
        return True
    return False

def authenticate():
    return Response(
    'Некорректный логин и пароль. Пожалуйста, перезапустите браузер и попробуйте ещё раз.', 401,
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

@app.route('/api/GetUserData/', methods=['POST'])
def GetUserData():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetUserData'
        result = get(configkey,data)
        return result
    
@app.route('/api/GetEmployees/', methods=['POST'])
def GetEmployees():
    if request.method == 'POST':
        configkey = 'GetEmployees'
        result = get(configkey)
        return result
    
@app.route('/api/GetEmployee/', methods=['POST'])
def GetEmployee():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetEmployee'
        result = get(configkey,data)
        return result
    
@app.route('/api/GetAdmins/', methods=['POST'])
def GetAdmins():
    if request.method == 'POST':
        configkey = 'GetAdmins'
        result = get(configkey)
        return result

@app.route('/api/GetMasters/', methods=['POST'])
def GetMasters():
    if request.method == 'POST':
        configkey = 'GetMasters'
        result = get(configkey)
        return result

@app.route('/api/GetBarberCategories/', methods=['POST'])
def GetBarberCategories():
    if request.method == 'POST':
        configkey = 'GetBarberCategories'
        result = get(configkey)
        return result
    
@app.route('/api/GetBarberCategory/', methods=['POST'])
def GetBarberCategory():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetBarberCategory'
        result = get(configkey,data)
        return result
    
@app.route('/api/GetOffices/', methods=['POST'])
def GetOffices():
    if request.method == 'POST':
        configkey = 'GetOffices'
        result = get(configkey)
        return result

@app.route('/api/GetOffice/', methods=['POST'])
def GetOffice():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetOffice'
        result = get(configkey,data)
        return result
    
@app.route('/api/GetCurrentSession/', methods=['POST'])
def GetCurrentSession():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetCurrentSession'
        result = get(configkey,data)
        return result

@app.route('/api/GetSession/', methods=['POST'])
def GetSession():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetSession'
        result = get(configkey,data)
        return result

@app.route('/api/GetSessionsWithOperations/', methods=['POST'])
def GetSessionsWithOperations():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetSessionsWithOperations'
        result = get(configkey,data)
        return result
    
@app.route('/api/GetServicesPrices/', methods=['POST'])
def GetServicesPrices():
    if request.method == 'POST':
        configkey = 'GetServicesPrices'
        result = get(configkey)
        return result    

@app.route('/api/GetServiceOperation/', methods=['POST'])
def GetServiceOperation():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetServiceOperation'
        result = get(configkey,data)
        return result

@app.route('/api/GetGoods/', methods=['POST'])
def GetGoods():
    if request.method == 'POST':
        configkey = 'GetGoods'
        result = get(configkey)
        return result
    
@app.route('/api/GetGood/', methods=['POST'])
def GetGood():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetGood'
        result = get(configkey,data)
        return result
    
@app.route('/api/GetGoodsOperation/', methods=['POST'])
def GetGoodsOperation():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetGoodsOperation'
        result = get(configkey,data)
        return result

@app.route('/api/GetSpendTypes/', methods=['POST'])
def GetSpendTypes():
    if request.method == 'POST':
        configkey = 'GetSpendTypes'
        result = get(configkey)
        return result
    
@app.route('/api/GetSpendType/', methods=['POST'])
def GetSpendType():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetSpendType'
        result = get(configkey,data)
        return result
    
@app.route('/api/GetSpendOperation/', methods=['POST'])
def GetSpendOperation():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetSpendOperation'
        result = get(configkey,data)
        return result

@app.route('/api/GetEmployeePaymentTypes/', methods=['POST'])
def GetEmployeePaymentTypes():
    if request.method == 'POST':
        configkey = 'GetEmployeePaymentTypes'
        result = get(configkey)
        return result

@app.route('/api/GetEmployeePaymentType/', methods=['POST'])
def GetEmployeePaymentType():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetEmployeePaymentType'
        result = get(configkey,data)
        return result    
    
@app.route('/api/GetEmployeePaymentOperation/', methods=['POST'])
def GetEmployeePaymentOperation():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetEmployeePaymentOperation'
        result = get(configkey,data)
        return result

@app.route('/api/GetClient/', methods=['POST'])
def GetClient():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetClient'
        result = get(configkey,data)
        return result
    
@app.route('/api/GetClients/', methods=['POST'])
def GetClients():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetClients'
        result = get(configkey,data)
        return result

@app.route('/api/EditOffice/', methods=['POST'])
def EditOffice():
    if request.method == 'POST':
        data = request.get_json()
        table = 'office'
        result = edit(table,data)
        return result 
    
@app.route('/api/EditSession/', methods=['POST'])
def EditSession():
    if request.method == 'POST':
        data = request.get_json()
        table = 'session'
        result = edit(table,data)
        return result

@app.route('/api/EditClient/', methods=['POST'])
def EditClient():
    if request.method == 'POST':
        data = request.get_json()
        table = 'client'
        result = edit(table,data)
        return result

@app.route('/api/EditOperations/', methods=['POST'])
def EditOperations():
    if request.method == 'POST':
        data = request.get_json()
        results = []
        for elem in data:
            table = elem['operationType']
            del elem['operationType']
            result = edit(table,elem)
            results.append(result)
        return results

@app.route('/api/EditEmployee/', methods=['POST'])
def EditEmployee():
    if request.method == 'POST':
        data = request.get_json()
        table = 'employee'
        result = edit(table,data)
        return result
    
@app.route('/api/EditBarberCategory/', methods=['POST'])
def EditBarberCategory():
    if request.method == 'POST':
        data = request.get_json()
        table = 'barbercategory'
        result = edit(table,data)
        return result    

# создать таблицу и сделать get
@app.route('/api/EditEmployeePaymentType/', methods=['POST'])
def EditEmployeePaymentType():
    if request.method == 'POST':
        data = request.get_json()
        table = 'employeepaymenttype'
        result = edit(table,data)
        return result    

@app.route('/api/EditGood/', methods=['POST'])
def EditGood():
    if request.method == 'POST':
        data = request.get_json()
        table = 'good'
        result = edit(table,data)
        return result
    
@app.route('/api/EditService/', methods=['POST'])
def EditService():
    if request.method == 'POST':
        data = request.get_json()
        table = 'service'
        result = edit(table,data)
        return result
    
@app.route('/api/EditSpendtype/', methods=['POST'])
def EditSpendtype():
    if request.method == 'POST':
        data = request.get_json()
        table = 'spendtype'
        result = edit(table,data)
        return result
    
@app.route('/api/GenerateCustomerReport/', methods=['POST'])
def GenerateCustomerReport():
    if request.method == 'POST':
        data = request.get_json()
        result = {}
        configkey = 'GenerateCustomerReportFinance'
        result1 = get(configkey,data)
        configkey = 'GenerateCustomerReportVisits'
        result2 = get(configkey)
        result["finance"] = result1
        result["visits"] = result2
        return result
    
@app.route('/api/GenerateFinanceReport/', methods=['POST'])
def GenerateFinanceReport():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GenerateFinanceReport'
        result = get(configkey,data)
        return result

@app.route('/static/<path:path>')
@requires_auth
def send_files(path):
    return send_from_directory(app.static_folder, path)

@app.route('/download/<path:filename>')
@requires_auth
def download(filename):
    directory = os.path.join(current_app.root_path, './downloadable_files/')
    return send_from_directory(directory=directory, filename=filename, as_attachment=True)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
@requires_auth
def front(path):
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return "Page not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
