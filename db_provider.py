#!/usr/bin/env python
# coding: utf-8


import json
import psycopg2

#DB
def prepareData(data):
    for key,value in data.items():
        if type(value) == dict:
            data[key] = json.dumps(value)
        elif type(value) == list:
            for i in range(len(value)):
                if type(value[i]) == dict:
                    value[i] = str(json.dumps(value[i]))
            data[key] = str(value)
        elif type(value) == str:
            data[key] = '\''+str(value)+'\''
        else:
            data[key] = str(value)
    return data

def generateQueryUpdate(table,data):
    _id = data['id']
    del data['id']
    baseq = f"""UPDATE {table} 
    SET """
        
    queryparts = []
    prepareData(data)
    for key,value in data.items():
        qpart = f"""{key} = {value}"""
        queryparts.append(qpart)
    setquery = ', '.join(queryparts)
    setquery = setquery.replace('\'null\'','null')
    setquery = setquery.replace('[','array [')
    setquery = setquery.replace('}\']','}\']::json[]')
    
    idquery = f"""
    where id = {_id}"""
    q = baseq + setquery + idquery + '\nRETURNING id'
    print(q)
    return q
    
def generateQueryCreate(table,data):
    columns = '(\"' + "\",\"".join(list(data.keys() )) + '\")'
    prepareData(data)
    v = '(' + ",".join((list(data.values()))) + ')'
    
    values = v.replace('\'null\'','null')
    values = values.replace('[','array [')
    values = values.replace('}\']','}\']::json[]')

    q = f"""INSERT INTO {table} {columns}
    VALUES
    {values} RETURNING id"""
    print(q)
    return q

def generateWhere(data):
    baseq = f"""
    where """
    wherepartslist = []
    for key,value in data.items():
        wherepart = f"""{key} = {value}"""
        wherepartslist.append(wherepart)
    wherestring = ' and '.join(wherepartslist)
    whereclause = baseq + wherestring
    return whereclause

def generateQueryRead(args=None):
    table = args['table']
    orderpart = ''
    wherepart = ''
    fields = '*'
    
    if 'fields' in args:
        fields = ','.join(args['fields'])
    
    if 'type' in args:
        if args['type'] == 'GetAdmins':
            role = rolesdict[args['type']]
            wherepart = f"""
            where 'officeAdmin' = ANY (roles)"""
            orderpart = f"""
            order by state desc, name asc"""
        
        if args['type'] == 'GetMasters':
            wherepart = f"""
            where 'master' = ANY (roles)"""
            orderpart = f"""
            order by state desc, name asc"""
            
        elif args['type'] == 'GetClients':
            string = args['data']['q'].lower()
            wherepart = f"""
            where name ilike '%{string}%'
            or  text(contacts) ilike '%{string}%'"""
            orderpart = f"""
            order by name asc"""
            
    else:    
        if 'data' in args:
            wherepart = generateWhere(args['data'])            
            
    query = f"""select {fields} from {table}{wherepart}{orderpart}"""
    return query

def goToBase(host,database,user,password,query,commit=False):
    conn = psycopg2.connect(host=host,database=database, user=user, password=password)
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute(query)
        if commit == True:
            conn.commit()
        result_data = cur.fetchall()
        cur.close()
        conn.close()
        if len(result_data) == 0:
            if commit == False:
                return {'error':'Нет таких данных'}
            else:
                return {'error':'Не удалось добавить данные'}
        else:
            return result_data
    except Exception as e:
        return {'error':e}
