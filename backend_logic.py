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
        'table':'_user',
        'dataneeded':True,
        'fields':['name','"pictureUrl"','roles']
    },
    'GetCurrentSession':{
        'table':'session',
        'dataneeded':True,
        'type':'GetSessions',
        'fields':['id','"dateOpened"','"dateClosed"','"employees"','"officeId"','state']
    },
    'GetOffices':{
        'table':'office',
        'fields':['id','name','state']
    },
    'GetAdmins':{
        'table':'_user',
        'type':'GetAdmins',
        'fields':['id','name','"pictureUrl"','state','"servicesPercent"','"goodsPercent"']
    },
    'GetMasters':{
        'table':'_user',
        'type':'GetAdmins',
        'fields':['id','name','"pictureUrl"','state','"servicesPercent"','"goodsPercent"']
    },
    'GetServicesPrices':{
        'table':'service',
        'fields':['id','name','prices']
    },
    'GetServiceOperation':{
        'table':'serviceoperation',
        'dataneeded':True
    },
    'GetGoodsOperation':{
        'table':'goodsoperation',
        'dataneeded':True
    },
    'GetSpendOperation':{
        'table':'spendoperation',
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
    'GetSession':{
        'table':'session',
        'type':'GetSessions',
        'dataneeded':True
    },
    'GetSessionsWithOperations':{
        'table':'session',
        'type':'GetSessions',
        'dataneeded':True
    },
    'GetEmployeePaymentTypes':{
        
    }
}

# Получить проекты
def getData():
    return {
	    "message": "Дратути"
	}

# делим вход на то, что надо создать и то, что надо изменить:
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

#триггерим апсерт: список, который на апдейт, апдейтится, который на креэйт — креэйтится
def upsert(table,data):
    createlist,updatelist = splitCreateUpdate(data) # вызываем функцию, которая делит входящие данные на два списка — на создание и обновление
    result = []
    for i in createlist:
        query = generateQueryCreate(table,i) # создаем sql-запрос на создание записей
        r = gotobase("localhost","barbers","read_write","Rw_Us3r",query,output,commit=True) # выполняем запрос
        result.append(r) # добавляем к общему списку результатов
    for i in updatelist:
        query = generateQueryUpdate(table,i) # создаем sql-запрос на апдейт записей
        r = gotobase("localhost","barbers","read_write","Rw_Us3r",query,output,commit=True) # выполняем запрос
        result.append(r) # добавляем к общему списку результатов
    return result

#триггерим селект
def select(*args):
    query = generateQueryRead(args)
    result = gotobase("localhost","barbers","read_only","User_ro",query)
    return result

#форматируем результат
def getResult(result)
    if type(result) == list:
            result = json.dumps([*map(dict, result)])
    return result

#Отправляем данные на апсерт и получаем результат
def edit(table,data):
    result = upsert(table,data)
    result = getresult(result)
    return result

#Отправляем данные на селект и получаем результат
def get(configkey,*args):
    args = argsconfig[configkey]
    if 'dataneeded' in args:
        args['data'] = args
    result = select(args)
    result = getresult(result)
