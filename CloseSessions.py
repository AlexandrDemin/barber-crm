#!/usr/bin/env python
# coding: utf-8


import json
import psycopg2
from psycopg2.extras import RealDictCursor
import traceback
import datetime

def getResult(result):
    if type(result) == list:
        if len(result) == 1:
            result = json.dumps(result[0],ensure_ascii=False)
        else:
            result = json.dumps([*map(dict, result)],ensure_ascii=False)
    else:
        result = json.dumps(result,ensure_ascii=False)
    return result

def dbCloseSessions():
    now = str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
    conn = psycopg2.connect(host='localhost',database='barbers',user="read_write",password="Rw_Us3r")
    cur = conn.cursor(cursor_factory=RealDictCursor)
    query = f"""UPDATE session 
    SET state='closed', "dateClosed" = '{now}'
    WHERE state='open'
    RETURNING id"""
    print(query)
    try:
        cur.execute(query)
        conn.commit()
        result_data = cur.fetchall()
        cur.close()
        conn.close()
        if len(result_data) == 0:
                return {'error':'Не удалось изменить данные'}
        else:
            return result_data
    except Exception as e:
        stacktrace = traceback.format_exc()
        return {'error':e,'stacktrace':stacktrace}
    
    
def closeSessions():
    result = dbCloseSessions()
    result = getResult(result)
    return result

closeSessions()

