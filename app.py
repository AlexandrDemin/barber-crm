#!/usr/bin/env python
# coding: utf-8

from flask import Flask, abort, url_for, render_template, request, Response, current_app, send_from_directory, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_user import login_required
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.wrappers import Request, Response
import json
from flask_cors import CORS
from backend_logic import *
import db_provider 
import os
from functools import wraps
import time
from werkzeug.utils import secure_filename
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor
import uuid
import datetime as dt
import traceback
import re
import io
from datetime import date,datetime, timedelta
import requests
import time
import json
import math
import copy
import urllib.parse
import codecs
import random
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

app = Flask(__name__, static_folder='./front/dist/static/', template_folder="./front/dist/")
CORS(app)

engine = create_engine('postgresql://read_write:Rw_Us3r@localhost/barbers', convert_unicode=True, echo=False)
Base = declarative_base()
Base.metadata.reflect(engine)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://read_write:Rw_Us3r@localhost/barbers'
app.config['SECRET_KEY'] = 's9cr9tk94'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)

login_manager = LoginManager()
login_manager.init_app(app)

class User(db.Model, UserMixin):
    __table__ = db.Model.metadata.tables['employee']

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def geterrorcode(data):
    if type(data) == dict:
        if 'error' in data:
            return 500
    else:
        return 200

@app.route('/api/Login/', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        login = data['login']
        password = data['password']
        try:
            user = User.query.filter_by(id=1).first()
            # user = User.query.filter_by(login=login,password=password).first()
            login_user(user)
            return 'Success'
        except:
            return 'Login Failed'

@app.route('/logout', methods=['POST'])
# @login_required
def logout():
    logout_user()
    return 'Logged out'

def writeLog(logEntry):
    with codecs.open("log.txt", "a", "utf-8") as logFile:
        json.dump(logEntry, logFile, ensure_ascii=False)
        logFile.write('\n')
        
@app.route('/api/GetCurrentUser/', methods=['POST'])
# @login_required
def GetCurrentUser():
    if request.method == 'POST':
        user = User.query.filter_by(id = current_user.id).first().__dict__
        del user['_sa_instance_state']
        return user

@app.route('/api/GetUserData/', methods=['POST'])
# @login_required
def GetUserData():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetUserData'
        result = get(configkey,data)
        return result,geterrorcode(result)
    
@app.route('/api/GetEmployees/', methods=['POST'])
# @login_required
def GetEmployees():
    if request.method == 'POST':
        configkey = 'GetEmployees'
        result = get(configkey)
        return result
    
@app.route('/api/GetEmployee/', methods=['POST'])
# @login_required
def GetEmployee():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetEmployee'
        result = get(configkey,data)
        return result
    
@app.route('/api/GetAdmins/', methods=['POST'])
# @login_required
def GetAdmins():
    if request.method == 'POST':
        configkey = 'GetAdmins'
        result = get(configkey)
        return result

@app.route('/api/GetMasters/', methods=['POST'])
# @login_required
def GetMasters():
    if request.method == 'POST':
        configkey = 'GetMasters'
        result = get(configkey)
        return result

@app.route('/api/GetBarberCategories/', methods=['POST'])
# @login_required
def GetBarberCategories():
    if request.method == 'POST':
        configkey = 'GetBarberCategories'
        result = get(configkey)
        return result
    
@app.route('/api/GetBarberCategory/', methods=['POST'])
# @login_required
def GetBarberCategory():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetBarberCategory'
        result = get(configkey,data)
        return result
    
@app.route('/api/GetOffices/', methods=['POST'])
# @login_required
def GetOffices():
    if request.method == 'POST':
        configkey = 'GetOffices'
        result = get(configkey)
        return result

@app.route('/api/GetOffice/', methods=['POST'])
# @login_required
def GetOffice():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetOffice'
        result = get(configkey,data)
        return result
    
@app.route('/api/GetCurrentSession/', methods=['POST'])
# @login_required
def GetCurrentSession():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetCurrentSession'
        result = get(configkey,data)
        if 'warning' in json.loads(result):
            result = {}
        return result

@app.route('/api/GetSession/', methods=['POST'])
# @login_required
def GetSession():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetSession'
        result = get(configkey,data)
        return result

@app.route('/api/GetSessions/', methods=['POST'])
# @login_required
def GetSessions():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetSessionsWithOperations'
        result = get(configkey,data)
        return result
    
@app.route('/api/GetServicesPrices/', methods=['POST'])
# @login_required
def GetServicesPrices():
    if request.method == 'POST':
        configkey = 'GetServicesPrices'
        result = get(configkey)
        return result

@app.route('/api/GetService/', methods=['POST'])
# @login_required
def GetService():
    if request.method == 'POST':
        configkey = 'GetService'
        data = request.get_json()
        result = get(configkey, data)
        return result

@app.route('/api/GetServiceOperation/', methods=['POST'])
# @login_required
def GetServiceOperation():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetServiceOperation'
        result = get(configkey,data)
        return result

@app.route('/api/GetGoods/', methods=['POST'])
# @login_required
def GetGoods():
    if request.method == 'POST':
        configkey = 'GetGoods'
        result = get(configkey)
        return result
    
@app.route('/api/GetGood/', methods=['POST'])
# @login_required
def GetGood():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetGood'
        result = get(configkey,data)
        return result
    
@app.route('/api/GetGoodsOperation/', methods=['POST'])
# @login_required
def GetGoodsOperation():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetGoodsOperation'
        result = get(configkey,data)
        return result

@app.route('/api/GetSpendTypes/', methods=['POST'])
# @login_required
def GetSpendTypes():
    if request.method == 'POST':
        configkey = 'GetSpendTypes'
        result = get(configkey)
        return result
    
@app.route('/api/GetSpendType/', methods=['POST'])
# @login_required
def GetSpendType():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetSpendType'
        result = get(configkey,data)
        return result
    
@app.route('/api/GetSpendOperation/', methods=['POST'])
# @login_required
def GetSpendOperation():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetSpendOperation'
        result = get(configkey,data)
        return result

@app.route('/api/GetEmployeePaymentTypes/', methods=['POST'])
# @login_required
def GetEmployeePaymentTypes():
    if request.method == 'POST':
        configkey = 'GetEmployeePaymentTypes'
        result = get(configkey)
        return result

@app.route('/api/GetEmployeePaymentType/', methods=['POST'])
# @login_required
def GetEmployeePaymentType():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetEmployeePaymentType'
        result = get(configkey,data)
        return result    
    
@app.route('/api/GetEmployeePaymentOperation/', methods=['POST'])
# @login_required
def GetEmployeePaymentOperation():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetEmployeePaymentOperation'
        result = get(configkey,data)
        return result

@app.route('/api/GetClient/', methods=['POST'])
# @login_required
def GetClient():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetClient'
        result = get(configkey,data)
        return result
    
@app.route('/api/GetClients/', methods=['POST'])
# @login_required
def GetClients():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GetClients'
        result = get(configkey,data)
        return result

@app.route('/api/EditOffice/', methods=['POST'])
# @login_required
def EditOffice():
    if request.method == 'POST':
        data = request.get_json()
        table = 'office'
        result = edit(table,data)
        return result 
    
@app.route('/api/EditSession/', methods=['POST'])
# @login_required
def EditSession():
    if request.method == 'POST':
        data = request.get_json()
        table = 'session'
        result = edit(table,data)
        return result

@app.route('/api/EditClient/', methods=['POST'])
# @login_required
def EditClient():
    if request.method == 'POST':
        data = request.get_json()
        table = 'client'
        result = edit(table,data)
        return result

@app.route('/api/EditOperations/', methods=['POST'])
# @login_required
def EditOperations():
    if request.method == 'POST':
        data = request.get_json()
        results = []
        firstservicewithpicture = True
        for elem in data:
            table = elem['operationType']
            del elem['operationType']
            result = edit(table,elem)
            results.append(json.loads(result))
        return json.dumps(results)

@app.route('/api/EditEmployee/', methods=['POST'])
# @login_required
def EditEmployee():
    if request.method == 'POST':
        data = request.get_json()
        table = 'employee'
        result = edit(table,data)
        return result
    
@app.route('/api/EditBarberCategory/', methods=['POST'])
# @login_required
def EditBarberCategory():
    if request.method == 'POST':
        data = request.get_json()
        table = 'barbercategory'
        result = edit(table,data)
        return result    

@app.route('/api/EditEmployeePaymentType/', methods=['POST'])
# @login_required
def EditEmployeePaymentType():
    if request.method == 'POST':
        data = request.get_json()
        table = 'employeepaymenttype'
        result = edit(table,data)
        return result    

@app.route('/api/EditGood/', methods=['POST'])
# @login_required
def EditGood():
    if request.method == 'POST':
        data = request.get_json()
        table = 'good'
        result = edit(table,data)
        return result
    
@app.route('/api/EditService/', methods=['POST'])
# @login_required
def EditService():
    if request.method == 'POST':
        data = request.get_json()
        table = 'service'
        result = edit(table,data)
        return result
    
@app.route('/api/EditSpendType/', methods=['POST'])
# @login_required
def EditSpendtype():
    if request.method == 'POST':
        data = request.get_json()
        table = 'spendtype'
        result = edit(table,data)
        return result
    
@app.route('/api/GenerateClientReport/', methods=['POST'])
# @login_required
def GenerateCustomerReport():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GenerateClientReport'
        result = get(configkey,data)
        return result
    
@app.route('/api/GenerateFinanceReport/', methods=['POST'])
# @login_required
def GenerateFinanceReport():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GenerateFinanceReport'
        result = get(configkey,data)
        return result
    
@app.route('/api/GenerateEmployeeReport/', methods=['POST'])
# @login_required
def GenerateEmployeeReport():
    if request.method == 'POST':
        data = request.get_json()
        configkey = 'GenerateEmployeeReport'
        result = get(configkey,data)
        return result

@app.route('/api/GenerateReportFile/', methods=['POST'])
# @login_required
def GenerateReportFile():
    if request.method == 'POST':
        data = request.get_json()
        if type(data) == dict:
            report = pd.DataFrame(data, index = [0])
        else:
            report = pd.DataFrame(data)
        filename = str(datetime.now().strftime("%Y-%m-%d-%H-%M"))+'_'+uuid.uuid4().hex+'.xlsx'
        report.to_excel('./downloadable_files/' + filename)
        return json.dumps({'filename': filename}, ensure_ascii=False), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/static/<path:path>')
def send_files(path):
    return send_from_directory(app.static_folder, path)

@app.route('/download/<path:filename>')
# @login_required
def download(filename):
    directory = os.path.join(current_app.root_path, './downloadable_files/')
    return send_from_directory(directory=directory, filename=filename, as_attachment=True)

@app.route("/login", methods=["GET", "POST"])
def login_form():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        try:
            user = User.query.filter_by(id=1).first()
            # user = User.query.filter_by(login=login,password=password).first()
            login_user(user)
            redirect_url = request.args.get("next") or '/'
            return redirect(redirect_url)   
        except:
            return abort(401)
    else:
        return render_template('login.html')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
@login_required
def front(path):
    return render_template('index.html')

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login?next=' + request.path)

@app.errorhandler(404)
def page_not_found(e):
    return "Page not found", 404
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
