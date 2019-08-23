#! /home/devel/anaconda2/envs/py35/bin/python3.6
# -*- coding: utf-8 -*-

from clickhouse_driver import Client
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
from requests_futures.sessions import FuturesSession
import math
import copy
import urllib.parse
session = FuturesSession()

# Получить конкурентов
def getRivalsAndData(offerid, maxRivalsCount, sqiDiffCoef, maxPos, minCountInSerm):
    # Получить данные КП
    offer = getOffer(offerid)

    # Получить ключи из КП
    keywords = []
    keywordTexts = []
    for keyword in offer['KeywordsToSave']:
        text = keyword[1]['Text'].lower()
        keywords.append({
            'id': keyword[0],
            'text': keyword[1]['Text']
        })
        if "'" in text:
            text = text.replace("'", "''")
        keywordTexts.append(text)
    keywordsStr = u"'" + u"', '".join(keywordTexts) + u"'"

    # Получить дату создания из КП
    startDate = offer['CreationTime'] - timedelta(days=5)
    startDate = startDate.strftime('%Y-%m-%d')

    # Получить домен из КП
    offerDomain = offer['Domain'].replace('www.', '')

    # Получить регионы из КП
    offerRegions = getOfferRegions(offer)

    # Получить id регионов из КП для Яндекса и Гугла
    regions = getRegionIds(offerRegions)
    regionsStr = u"'" + u"', '".join([x['yaId'] for x in regions])\
            + u"', '" + u"', '".join([x['gId'] for x in regions]) + u"'"

    rivals = getRivals(keywordsStr, startDate, regionsStr, maxPos, maxRivalsCount, sqiDiffCoef, offerDomain, minCountInSerm)
    return keywords, rivals, startDate, keywordsStr, regionsStr, regions

# Получить КП по id
def getOffer(offerid):
    client = MongoClient('mongodb://192.168.10.77:27017/')
    db = client.Offers
    offers = db.offers
    offer = {}
    for offer in offers.find({"_id": ObjectId(offerid)}):
        offer = offer
    return offer

# Получить уникальные регионы запросов КП
def getOfferRegions(offer):
    regions = []
    for keyword in offer['KeywordsStatisticsToSave']:
        regions.append(keyword[1]['RegionId'])
    regions = set(regions)
    return list(regions)

# Получить яндексовые и гугловые id регионов
def getRegionIds(offerRegions):
    regionIdsStr = ', '.join(str(x) for x in offerRegions)
    query = """
    SELECT r.regionid AS regionId, r."value" AS yaRegion, r2."value" AS gRegion, r3."name"
    FROM regiondetails AS r
    JOIN regiondetails AS r2 ON r.regionid=r2.regionid AND r2.regiontype=1
    JOIN region AS r3 ON r.regionid=r3.id
    WHERE r.regiontype=0 AND r.regionid IN ({})

    """.format(regionIdsStr)

    conn = psycopg2.connect(dbname="Regions", user="read_only", password="User_ro",host="192.168.10.38")
    cur = conn.cursor()
    cur.execute(query)
    df = pd.DataFrame(cur.fetchall())
    cur.close()
    conn.close()

    df = df.rename(columns={
        0: "regionId",
        1: "yaId",
        2: "gId",
        3: "name",
    })

    regionsWithQuotes = df.to_dict('records')
    regions = []

    for region in regionsWithQuotes:
        regions.append({
            'regionId': region['regionId'],
            'yaId': region['yaId'][1:-1],
            'gId': region['gId'][1:-1],
            'name': region['name'],
        })
    return regions

# Запустить асинхронное получение Яндекс ИКС по домену
def getSqiPromise(domain):
    data = {
        "jsonrpc":"2.0",
        "method":"GetYandexSqi",
        "params": {
            "host": domain
        }
    }
    return session.post('http://192.168.10.37:12345/YandexSqiService', data=json.dumps(data, ensure_ascii=False).encode('utf-8'))

# Получить Яндекс ИКС из асинхронного запроса
def getSqiResult(sqiPromise, domain):
    if not isinstance(sqiPromise, int):
        r = sqiPromise.result()
        sqi = r.json()["result"]["Sqi"]
        if sqi == 0 and 'yandex.ru' in domain:
            sqi = 1000000
        return sqi
    else:
        return sqiPromise

# Получить Яндекс ИКС по домену
def getSqi(domain):
    data = {
        "jsonrpc":"2.0",
        "method":"GetYandexSqi",
        "params": {
            "host": domain
        }
    }
    r = requests.post('http://192.168.10.37:12345/YandexSqiService', data=json.dumps(data, ensure_ascii=False).encode('utf-8'))
    sqi = r.json()["result"]["Sqi"]
    if sqi == 0 and 'yandex.ru' in domain:
        sqi = 1000000
    return sqi

def getRivals(keywordsStr, startDate, regionsStr, maxPos, maxRivalsCount, sqiDiffCoef, offerDomain, minCountInSerm):
    
    # Получить конкурентов из базы
    query =f"""
        select domain, count(*)
        from secache3
        where
            keyword in ({keywordsStr})
            and date >= '{startDate}'
            and regionId in ({regionsStr})
            and position <= {maxPos}
            and isMobile = 0
        group by domain
        having count(*) >= {minCountInSerm}
        order by count(*) desc
        limit {maxRivalsCount}
    """
    client = Client(host = '192.168.10.101', user = 'read_only', password = 'User_ro')
    data = client.execute(query)
    client.disconnect()

    # Получить популярные домены из файла конфига
    excluded_domains = []
    with io.open("./popular-domains.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            excluded_domains.append(str.strip(line))
    excluded_domains.append(offerDomain)

    # Заполнить данные по доменам
    domains = []
    ourSqi = getSqi(offerDomain)
    hasOfferDomain = False
    for domain in data:
        domainSqi = getSqi(domain[0])
        isExcluded = False
        for ex in excluded_domains:
            if ex == domain[0] or '.' + ex in domain[0]:
                isExcluded = True
        domains.append({
            'domain': domain[0],
            'countInSerm': domain[1],
            'isExcluded': isExcluded,
            'sqi': getSqiPromise(domain[0]),
            'isOfferDomain': domain[0] == offerDomain
        })
        if domain[0] == offerDomain:
            hasOfferDomain = True
    if not hasOfferDomain:
        domains.append({
            'domain': offerDomain,
            'countInSerm': 0,
            'isExcluded': False,
            'sqiDiff': 1,
            'sqi': ourSqi,
            'isOfferDomain': True
        })
    for domain in domains:
        try:
            sqi = getSqiResult(domain['sqi'], domain['domain'])
            domain['sqi'] = sqi,
            domain['sqiDiff'] = sqi / ourSqi
            if(domain['sqiDiff']) > sqiDiffCoef:
                domain['isExcluded'] = True
        except:
            domain['sqi'] = 0
            domain['sqiDiff'] = 0
    return domains

def getRegionName(keyword, regions):
    for region in regions:
        if (keyword['searchEngine'] == 1 and region['yaId'] == keyword['regionId']) or (keyword['searchEngine'] == 2 and region['gId'] == keyword['regionId']):
            return region['name']

def getKeywordsRivals(keywords, rivals, maxPos, startDate, keywordsStr, regionsStr, regions, minCountInSerm):
    # Получить строку из неконкурентов
    notRivals = []
    for domain in rivals:
        if domain['isExcluded'] or domain['isOfferDomain']:
            notRivals.append(domain['domain'])

    # Получить редко встречающихся конкурентов из базы
    query =f"""
        select domain
        from secache3
        where
            keyword in ({keywordsStr})
            and date >= '{startDate}'
            and regionId in ({regionsStr})
            and position <= {maxPos}
            and isMobile = 0
        group by domain
        having count(*) < {minCountInSerm}
    """
    client = Client(host = '192.168.10.101', user = 'read_only', password = 'User_ro', settings={'max_query_size':500000})
    rareRivals = client.execute(query)
    client.disconnect()
    
    for rival in rareRivals:
        notRivals.append(rival[0])
    
    notRivalsStr = u"'" + u"', '".join(notRivals) + u"'"

    # Получить количество конкурентов по ключам
    query =f"""
        select searchEngine, isMobile, keyword, regionId, count(*)
        from secache3
        where
            keyword in ({keywordsStr})
            and date >= '{startDate}'
            and regionId in ({regionsStr})
            and position <= {maxPos}
            and domain not in ({notRivalsStr})
            and isMobile = 0
        group by time, searchEngine, isMobile, keyword, regionId
        having time=max(time)
        order by count(*) desc
    """
    client = Client(host = '192.168.10.101', user = 'read_only', password = 'User_ro', settings={'max_query_size':500000})
    data = client.execute(query)
    client.disconnect()
    df = pd.DataFrame(data)
    df = df.rename(columns={
        0: "searchEngine",
        1: "isMobile",
        2: "keyword",
        3: "regionId",
        4: "rivalsCount",
    })
    all_keywords = df.to_dict('records')
    for keyword in keywords:
        if len(df[df['keyword'] == keyword['text']].index) == 0:
            all_keywords.append({
                "id": keyword['id'],
                'keyword': keyword['text'],
                "searchEngine": None,
                "isMobile": None,
                "regionId": None,
                "regionName": '—',
                "rivalsCount": 0
            })
    for keyword in all_keywords:
        if not 'regionName' in keyword:
            keyword['regionName'] = getRegionName(keyword, regions)
    return all_keywords, notRivals

def getKeywordsToRemove(all_keywords, minKeywordRivals, regions):
    keywordsToDelete = []
    keywordsByRegion = {}
    allRegionsName = 'Все регионы'
    noRegionStr = '—'
    regionsCount = len(regions)
    for region in regions:
        for keyword in all_keywords:
            if region['name'] == keyword['regionName']:
                if region['name'] in keywordsByRegion:
                    keywordsByRegion[region['name']].append(keyword)
                else:
                    keywordsByRegion[region['name']] = [keyword]
            if keyword['regionName'] == noRegionStr:
                if regionsCount == 2:
                    regionName = regions[0]['name']
                    if regionName in keywordsByRegion:
                        keywordsByRegion[regionName].append(keyword)
                    else:
                        keywordsByRegion[regionName] = [keyword]
                else:
                    if allRegionsName in keywordsByRegion:
                        keywordsByRegion[allRegionsName].append(keyword)
                    else:
                        keywordsByRegion[allRegionsName] = [keyword]
    for region in keywordsByRegion:
        df = pd.DataFrame(keywordsByRegion[region])
        keywords = list(set(df[df['rivalsCount'] < minKeywordRivals]['keyword'].tolist()))
        if len(keywords) > 0:
            keywordsToDelete.append({
                'region': region,
                'keywordsToDelete': keywords
            })
    return keywordsToDelete

# Получить выдачу
def getSerm(keyword, regionId, searchEngine, isMobile, maxPos, startDate, rivals, regions, notRivals):
    query =f"""
        select distinct keyword, regionId, searchEngine, isMobile, domain, position, foundUrl
        from secache3
        where
            keyword = '{keyword}'
            and date >= '{startDate}'
            and regionId = '{regionId}'
            and position <= {maxPos}
            and isMobile = {isMobile}
        group by time, keyword, regionId, searchEngine, isMobile, domain, position, foundUrl
        having time=max(time)
        order by position
    """
    client = Client(host = '192.168.10.101', user = 'read_only', password = 'User_ro')
    data = client.execute(query)
    client.disconnect()
    df = pd.DataFrame(data)
    df = df.rename(columns={
        0: "keyword",
        1: "regionId",
        2: "searchEngine",
        3: "isMobile",
        4: "domain",
        5: "position",
        6: "foundUrl"
    })
    res = df.to_dict('records')
    for s in res:
        s['foundUrl'] = urllib.parse.unquote(s['foundUrl'])
        for rival in rivals:
            if rival['domain'] == s['domain']:
                s['isExcluded'] = rival['isExcluded']
        for notRival in notRivals:
            if notRival == s['domain']:
                s['isExcluded'] = True
    return res

def saveFilterRivalsObject(filter_rivals_object):
    client = MongoClient('mongodb://192.168.10.77:27017/')
    db = client.Offers
    collection = db.filterRivals
    existing = collection.count_documents({'offerid': filter_rivals_object['offerid']})
    if existing > 0:
        object_id = collection.find({'offerid': filter_rivals_object['offerid']})[0]['_id']
        result = collection.update_one(
            {'_id': object_id},
            {'$set': filter_rivals_object}
        )
        raw_result = result.raw_result
        return str(object_id)
    else:
        local_copy = copy.deepcopy(filter_rivals_object)
        result = collection.insert_one(local_copy)
        result_id = result.inserted_id
        return str(result_id)

def getFilterRivalsObjectByOfferId(offer_id):
    client = MongoClient('mongodb://192.168.10.77:27017/')
    db = client.Offers
    collection = db.filterRivals
    try:
        result = collection.find({'offerid': offer_id})[0]
        return result
    except:
        return None

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

def saveKeywordsToRemove(offerid, keywords_to_remove, minKeywordRivals):
    client = MongoClient('mongodb://192.168.10.77:27017/')
    db = client.Offers
    collection = db.filterRivals
    existing = collection.count_documents({'offerid': offerid})
    if existing > 0:
        object_id = collection.find({'offerid': offerid})[0]['_id']
        result = collection.update_one(
            {'_id': ObjectId(object_id)},
            {'$set': {
                    'keywordsToRemove': keywords_to_remove,
                    'minKeywordRivals': minKeywordRivals
                }
            }
        )
        raw_result = result.raw_result
        return raw_result
