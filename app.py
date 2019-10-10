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
import uuid
import datetime as dt

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__, static_folder='./front/dist/static/', template_folder="./front/dist/")
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
        
def uploadfiles(request):
    if 'file' in request.files:
        uploaded_files = request.files.getlist("file[]")
        for file in uploaded_files:
            pictureUrlsList = []
            if file.filename == '':
                pass
            elif file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                pictureUrl = os.path.join(app.config['UPLOAD_FOLDER']) + filename
                pictureUrlsList.append(pictureUrlsList)
        return pictureUrlsList
        
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
@requires_auth
def GetUserData():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetUserData'
        result = get(configkey,data)
        return result
    
@app.route('/api/GetEmployees/', methods=['POST'])
@requires_auth
def GetEmployees():
    if request.method == 'POST':
        configkey = 'GetEmployees'
        result = get(configkey)
        return result
    
@app.route('/api/GetEmployee/', methods=['POST'])
@requires_auth
def GetEmployee():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetEmployee'
        result = get(configkey,data)
        return result
    
@app.route('/api/GetAdmins/', methods=['POST'])
@requires_auth
def GetAdmins():
    if request.method == 'POST':
        configkey = 'GetAdmins'
        result = get(configkey)
        return result

@app.route('/api/GetMasters/', methods=['POST'])
@requires_auth
def GetMasters():
    if request.method == 'POST':
        configkey = 'GetMasters'
        result = get(configkey)
        return result

@app.route('/api/GetBarberCategories/', methods=['POST'])
@requires_auth
def GetBarberCategories():
    if request.method == 'POST':
        configkey = 'GetBarberCategories'
        result = get(configkey)
        return result
    
@app.route('/api/GetBarberCategory/', methods=['POST'])
@requires_auth
def GetBarberCategory():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetBarberCategory'
        result = get(configkey,data)
        return result
    
@app.route('/api/GetOffices/', methods=['POST'])
@requires_auth
def GetOffices():
    if request.method == 'POST':
        configkey = 'GetOffices'
        result = get(configkey)
        return result

@app.route('/api/GetOffice/', methods=['POST'])
@requires_auth
def GetOffice():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetOffice'
        result = get(configkey,data)
        return result
    
@app.route('/api/GetCurrentSession/', methods=['POST'])
@requires_auth
def GetCurrentSession():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetCurrentSession'
        result = get(configkey,data)
        return result

@app.route('/api/GetSession/', methods=['POST'])
@requires_auth
def GetSession():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetSession'
        result = get(configkey,data)
        return result

@app.route('/api/GetSessionsWithOperations/', methods=['POST'])
@requires_auth
def GetSessionsWithOperations():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetSessionsWithOperations'
        result = get(configkey,data)
        return result
    
@app.route('/api/GetServicesPrices/', methods=['POST'])
@requires_auth
def GetServicesPrices():
    if request.method == 'POST':
        configkey = 'GetServicesPrices'
        result = get(configkey)
        return result    

@app.route('/api/GetServiceOperation/', methods=['POST'])
@requires_auth
def GetServiceOperation():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetServiceOperation'
        result = get(configkey,data)
        return result

@app.route('/api/GetGoods/', methods=['POST'])
@requires_auth
def GetGoods():
    if request.method == 'POST':
        configkey = 'GetGoods'
        result = get(configkey)
        return result
    
@app.route('/api/GetGood/', methods=['POST'])
@requires_auth
def GetGood():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetGood'
        result = get(configkey,data)
        return result
    
@app.route('/api/GetGoodsOperation/', methods=['POST'])
@requires_auth
def GetGoodsOperation():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetGoodsOperation'
        result = get(configkey,data)
        return result

@app.route('/api/GetSpendTypes/', methods=['POST'])
@requires_auth
def GetSpendTypes():
    if request.method == 'POST':
        configkey = 'GetSpendTypes'
        result = get(configkey)
        return result
    
@app.route('/api/GetSpendType/', methods=['POST'])
@requires_auth
def GetSpendType():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetSpendType'
        result = get(configkey,data)
        return result
    
@app.route('/api/GetSpendOperation/', methods=['POST'])
@requires_auth
def GetSpendOperation():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetSpendOperation'
        result = get(configkey,data)
        return result

@app.route('/api/GetEmployeePaymentTypes/', methods=['POST'])
@requires_auth
def GetEmployeePaymentTypes():
    if request.method == 'POST':
        configkey = 'GetEmployeePaymentTypes'
        result = get(configkey)
        return result

@app.route('/api/GetEmployeePaymentType/', methods=['POST'])
@requires_auth
def GetEmployeePaymentType():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetEmployeePaymentType'
        result = get(configkey,data)
        return result    
    
@app.route('/api/GetEmployeePaymentOperation/', methods=['POST'])
@requires_auth
def GetEmployeePaymentOperation():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetEmployeePaymentOperation'
        result = get(configkey,data)
        return result

@app.route('/api/GetClient/', methods=['POST'])
@requires_auth
def GetClient():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetClient'
        result = get(configkey,data)
        return result
    
@app.route('/api/GetClients/', methods=['POST'])
@requires_auth
def GetClients():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetClients'
        result = get(configkey,data)
        return result

@app.route('/api/EditOffice/', methods=['POST'])
@requires_auth
def EditOffice():
    if request.method == 'POST':
        data = request.get_json()
        table = 'office'
        result = edit(table,data)
        return result 
    
@app.route('/api/EditSession/', methods=['POST'])
@requires_auth
def EditSession():
    if request.method == 'POST':
        data = request.get_json()
        table = 'session'
        result = edit(table,data)
        return result

@app.route('/api/EditClient/', methods=['POST'])
@requires_auth
def EditClient():
    if request.method == 'POST':
        data = request.get_json()
        table = 'client'
        pictureUrlsList = uploadfiles(request)
        if pictureUrlsList:
            data['pictureUrl'] = pictureUrlsList
        result = edit(table,data)
        return result

@app.route('/api/EditOperations/', methods=['POST'])
@requires_auth
def EditOperations():
    if request.method == 'POST':
        data = request.get_json()
        results = []
        firstservicewithpicture = True
        for elem in data:
            table = elem['operationType']
            if 'serviceoperation' in elem['operationType'] and firstservicewithpicture == True:
                pictureUrlsList = uploadfiles(request)
                if pictureUrlsList:
                    elem['photoUrls'] = pictureUrlsList
                    firstservicewithpicture = False
            data['"pictureUrl"'] = pictureUrlsList
            del elem['operationType']
            result = edit(table,elem)
            results.append(result)
        return results

@app.route('/api/EditEmployee/', methods=['POST'])
@requires_auth
def EditEmployee():
    if request.method == 'POST':
        data = request.get_json()
        table = 'employee'
        pictureUrlsList = uploadfiles(request)
        if pictureUrlsList:
            data['pictureUrl'] = pictureUrlsList[0]                     
        result = edit(table,data)
        return result
    
@app.route('/api/EditBarberCategory/', methods=['POST'])
@requires_auth
def EditBarberCategory():
    if request.method == 'POST':
        data = request.get_json()
        table = 'barbercategory'
        result = edit(table,data)
        return result    

@app.route('/api/EditEmployeePaymentType/', methods=['POST'])
@requires_auth
def EditEmployeePaymentType():
    if request.method == 'POST':
        data = request.get_json()
        table = 'employeepaymenttype'
        result = edit(table,data)
        return result    

@app.route('/api/EditGood/', methods=['POST'])
@requires_auth
def EditGood():
    if request.method == 'POST':
        data = request.get_json()
        table = 'good'
        result = edit(table,data)
        return result
    
@app.route('/api/EditService/', methods=['POST'])
@requires_auth
def EditService():
    if request.method == 'POST':
        data = request.get_json()
        table = 'service'
        result = edit(table,data)
        return result
    
@app.route('/api/EditSpendtype/', methods=['POST'])
@requires_auth
def EditSpendtype():
    if request.method == 'POST':
        data = request.get_json()
        table = 'spendtype'
        result = edit(table,data)
        return result
    
@app.route('/api/GenerateClientReport/', methods=['POST'])
@requires_auth
def GenerateCustomerReport():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GenerateClientReport'
        result = get(configkey,data)
        report = pd.DataFrame(result)
        filename = configkey+str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M"))+'_'+uuid.uuid4().hex
        report.to_excel('./downloadable_files/' + filename)
        return result, Response(report,headers={"Content-Disposition":f"""attachment;filename={filename}.xlsx"""})
    
@app.route('/api/GenerateFinanceReport/', methods=['POST'])
@requires_auth
def GenerateFinanceReport():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GenerateFinanceReport'
        result = get(configkey,data)
        report = pd.DataFrame(result)
        filename = configkey+str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M"))+'_'+uuid.uuid4().hex
        report.to_excel('./downloadable_files/' + filename)
        return result, Response(report,headers={"Content-Disposition":f"""attachment;filename={filename}.xlsx"""})
    
@app.route('/api/GenerateEmployeeReport/', methods=['POST'])
@requires_auth
def GenerateEmployeeReport():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GenerateEmployeeReport'
        result = get(configkey,data)
        report = pd.DataFrame(result)
        filename = configkey+str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M"))+'_'+uuid.uuid4().hex
        report.to_excel('./downloadable_files/' + filename)
        return result, Response(report,headers={"Content-Disposition":f"""attachment;filename={filename}.xlsx"""})

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
