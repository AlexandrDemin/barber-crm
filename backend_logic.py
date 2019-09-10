#! /home/devel/anaconda2/envs/py35/bin/python3.6
# -*- coding: utf-8 -*-

import io
import pandas as pd
import numpy as np
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timedelta
import psycopg2
import requests
import time
import json
import math
import copy
import urllib.parse
import codecs
import random

# Получить проекты
def getProjects():
    client = MongoClient('mongodb://192.168.10.77:27017/')
    db = client.Offers
    apra_projects = db.apraProject
    projects = []
    for project in apra_projects.find({}):
        project['_id'] = str(project['_id'])
        projects.append(project)
    return projects

# Получить проект по projectid
def getProject(projectid):
    client = MongoClient('mongodb://192.168.10.77:27017/')
    db = client.Offers
    apra_projects = db.apraProject
    try:
        project = apra_projects.find({"projectId": int(projectid)})[0]
        project['_id'] = str(project['_id'])
        return project
    except:
        return None

# СЯ
def getSemCore(domain, directions = [], regions = [3], max_count = 300, minus_words = [], minus_phrases = []):
    data = {
       "method":"GetSemCore",
       "params" : {
           "request": {
               "Domain": domain,
               "Directions": directions,
               "RegionIds": regions,
               "BroadMinusPhrases": minus_words,
               "MinusPhrases": minus_phrases,
               "ResultCount": max_count,
               "CacheTime": "23:00:00"
           }
       }
    }
    url = 'http://192.168.10.37:12345/SemanticCoreService'
    req = requests.post(url, data=json.dumps(data, ensure_ascii=False).encode("utf-8"))
    return req.json()['result']['Queries']

# Терек
def getTerec(url, queries):
    url = 'http://192.168.10.55:12345/NewTeRecService'
    data = {
        "method":"Analyze",
        "params" : {
            "url": url,
            "queries": queries
        }
    }
    req = requests.post(url, data=json.dumps(data, ensure_ascii=False).encode("utf-8"))
    return req.text #.json()['result']

# Мета-теги
def getMetatags(domain, queries):
    url = 'http://192.168.10.55:12345/AutoSemcoreService'
    data = {
        "method":"GetTitleAndDescription",
        "params" : {
            "domain": domain,
            "requests": queries
        }
    }
    print(json.dumps(data, ensure_ascii=False)) 
    req = requests.post(url, data=json.dumps(data, ensure_ascii=False).encode("utf-8"))
    return req.json().get('result')

# Прогноз трафика
def getTrafficForecast(shows, position):
    url = 'http://ingress.production.k8s:30080/TrafficForecastService'
    data = {
        "id": 0,
        "jsonrpc":"2.0",
        "method":"gettrafficforecasts",
        "params" : {
            "shows": shows,
            "position": position
        }
    }
    req = requests.post(url, data=json.dumps(data, ensure_ascii=False).encode("utf-8"))
    return req.json()['result']

# Прогноз срока вывода в топ
def getTopTimeForecast(queries):
    time.sleep(2)
    queriesWithData = []
    for query in queries:
        f = 12
        if len(query) < 12:
            f = len(query) + 1
        elif (len(query.split(' ')) + 2) <=12:
            f = len(query.split(' ')) + 2
        elif query[0] == 'а':
            f = 6
        elif query[0] == 'т':
            f = 4
        elif query[-2:-1] == 'н':
            f = 5
        queriesWithData.append({
            "query": query,
            "monthToTopForecast": f
        })
    return queriesWithData

# Прогноз конверсии
def getConversionForecast(queries):
    url = 'http://ingress.production.k8s:30080/ConversionService'
    data = {
        "id": 0,
        "jsonrpc":"2.0",
        "method":"getconversionscores",
        "params" : {
            "queries": queries
        }
    }
    req = requests.post(url, data=json.dumps(data, ensure_ascii=False).encode("utf-8"))
    res = req.json()['result']
    queriesWithData = []
    maxConv = max(res)
    for query, conversion in zip(queries,res):
        queriesWithData.append({
            'query': query,
            'conversion': int(conversion/maxConv * 100)
        })
    sortedList = sorted(queriesWithData, key=lambda k: k['conversion'], reverse=True) 
    return sortedList

# Генерация текстов объявлений
def getAdTexts(domain, queries):
    url = 'http://192.168.10.55:12345/AllInSemCoreGeneratorService'
    data = {
       "method": "GenerateTextAndHeaders",
       "params": [
           queries,
           domain
       ]
    }
    req = requests.post(url, data=json.dumps(data, ensure_ascii=False).encode("utf-8"))
    return req.json()['result']
