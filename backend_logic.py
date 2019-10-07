#! python3
# -*- coding: utf-8 -*-

import io
import pandas as pd
from datetime import datetime, timedelta
import requests
import time
import json
import math
import copy
import urllib.parse
import codecs
import random

# на основе этих конфигов выполняются селекты в базу
argsconfig = {
    'GetUserData':{
        'table':'employee',
        'dataneeded':True,
        'fields':['name','"pictureUrl"','roles']
    },
    'GetEmployees':{
        'table':'employee'
    },
    'GetEmployee':{
        'table':'employee',
        'dataneeded':True
    },
    'GetAdmins':{
        'table':'employee',
        'type':'GetAdmins',
        'fields':['id','name','"pictureUrl"','state','"servicePercent"','"goodsPercent"']
    },
    'GetMasters':{
        'table':'employee',
        'type':'GetMasters',
        'fields':['id','name','"pictureUrl"','state','"servicePercent"','"goodsPercent"']
    },
    'GetBarberCategories':{
        'table':'barbercategory'
    },
    'GetBarberCategory':{
        'table':'barbercategory',
        'dataneeded':True
    },
    'GetOffices':{
        'table':'office',
        'fields':['id','name','state']
    },
    'GetOffice':{
        'table':'office',
        'fields':['id','name','state'],
        'dataneeded':True
    },
    'GetCurrentSession':{
        'table':'session',
        'type':'GetSessions',
        'dataneeded':True,
        'fields':['id','"dateOpened"','"dateClosed"','"employees"','"officeId"','state']
    },
    'GetSession':{
        'table':'session',
        'type':'GetSessions',
        'dataneeded':True,
        'fields':['id','"dateOpened"','"dateClosed"','"employees"','"officeId"','state']
    },
    'GetSessionsWithOperations':{
        'table':'session',
        'type':'GetSessions',
        'dataneeded':True,
        'fields':['id','"dateOpened"','"dateClosed"','"employees"','"officeId"','state']
    },
    'GetServicesPrices':{
        'table':'service',
        'fields':['id','name','prices']
    },
    'GetServiceOperation':{
        'table':'serviceoperation',
        'dataneeded':True
    },
    'GetGoods':{
        'table':'good'
    },
    'GetGood':{
        'table':'good',
        'dataneeded':True
    },
    'GetGoodsOperation':{
        'table':'goodsoperation',
        'dataneeded':True
    },
    'GetSpendTypes':{
        'table':'spendtype'
    },
    'GetSpendType':{
        'table':'spendtype',
        'dataneeded':True
    },
    'GetSpendOperation':{
        'table':'spendoperation',
        'dataneeded':True
    },
    'GetEmployeePaymentTypes':{
        'table':'employeepaymenttype'
    },
    'GetEmployeePaymentType':{
        'table':'employeepaymenttype',
        'dataneeded':True
    },
    'GetEmployeePaymentOperation':{
        'table':'employeepayment',
        'dataneeded':True
    },
    'GetClient':{
        'table':'client',
        'dataneeded':True
    },
    'GetClients':{
        'table':'client',
        'type':'GetClients',
        'dataneeded':True
    },
    'GenerateEmployeeReport':{
        'type':'GenerateEmployeeReport',
        'dataneeded':True
    },
    'GenerateCustomerReportFinance':{
        'type':'GenerateCustomerReportFinance',
        'dataneeded':True
    },
    'GenerateCustomerReportVisits':{
        'type':'GenerateCustomerReportVisits'
    },
    'GenerateFinanceReport':{
        'type':'GenerateFinanceReport',
        'dataneeded':True
    }
}


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%d.%m.%Y %H:%M")
        return json.JSONEncoder.default(self, obj)
    
def splitCreateUpdate(data):
    createlist = []
    updatelist = []
    if type(data) is dict:
        if data['id'] == 'null':
            del data['id']
            createlist.append(data)
        else:
            updatelist.append(data)
    elif type(data) is list:
        for item in data:
            if item['id'] == 'null':
                del item['id']
                createlist.append(item)
            else:
                updatelist.append(item)        
    return createlist,updatelist

def upsert(table,data):
    createlist,updatelist = splitCreateUpdate(data)
    table = table
    result = []
    for i in createlist:
        query = generateQueryCreate(table,i)
        r = goToBase("localhost","barbers","admin","Adm1n1strat0r",query,commit=True)
        result.append(r)
    for i in updatelist:
        query = generateQueryUpdate(table,i)
        r = goToBase("localhost","barbers","admin","Adm1n1strat0r",query,commit=True)
        result.append(r)
    result = json.dumps(result)
    return result

def select(args=None):
    query = generateQueryRead(args)
    result = goToBase("localhost","barbers","read_only","User_ro",query)
    return result

def getResult(result):
    getResult.result = result
    if type(result) == list:
        if len(result) == 1:
            result = json.dumps(result[0],ensure_ascii=False, cls=DateEncoder)
        else:
            result = json.dumps([*map(dict, result)],ensure_ascii=False, cls=DateEncoder)
    return result
            
def edit(table,data):
    result = upsert(table,data)
    result = getResult(result)
    return result

def get(configkey,args=None):
    raw_data = argsconfig[configkey]
    if 'dataneeded' in raw_data:
        raw_data['data'] = args
    result = select(raw_data)
    result = getResult(result)
    return result
