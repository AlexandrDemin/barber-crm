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

# Получить проекты
def getProjects():
    client = MongoClient('mongodb://192.168.10.77:27017/')
    db = client.Offers
    apra_projects = db.apraProjects
    projects = []
    for project in apra_projects.find({}):
        projects.append(project)
    return projects

# Получить проект по projectid
def getProject(projectid):
    client = MongoClient('mongodb://192.168.10.77:27017/')
    db = client.Offers
    apra_projects = db.apraProjects
    try:
        project = apra_projects.find({"projectId": projectid})[0]
        return project
    except:
        return None

# Проапдейтить что-то
def saveKeywords(offerid, keywords, rivals, not_rivals):
    client = MongoClient('mongodb://192.168.10.77:27017/')
    db = client.Offers
    collection = db.filterRivals
    existing = collection.count_documents({'offerid': offerid})
    if existing > 0:
        object_id = collection.find({'offerid': offerid})[0]['_id']
        result = collection.update_one(
            {'_id': ObjectId(object_id)},
            {'$set': {
                    'keywordsWithData': keywords,
                    'rivals': rivals,
                    'notRivals': not_rivals
                }
            }
        )
        raw_result = result.raw_result
        return raw_result
