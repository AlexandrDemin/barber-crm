#!/usr/bin/env python
# coding: utf-8


import json
import psycopg2

#DB
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

def getSessionsQuery(args):
    table = args['table']
    fields = ','.join(args['fields'])
    qdatefrompart = ''
    qdatetopart = ''
    wherepartlist = []

    if 'dateFrom' in args['data']:
        date = args['data']['dateFrom']
        qdatefrompart = f"""\"dateOpened\" >= '{date}'""" 

    if 'dateTo' in args['data']:
        date = args['data']['dateTo']
        qdatetopart = f"""\"dateClosed\" <= '{date}'"""

    if 'employeeIds' in args['data']:
        fields_filtered = args['fields'].copy()
        fields_filtered.remove('"employees"')
        fields = ','.join(fields_filtered)
        employeeids = args['data']['employeeIds']
        employeeidslistformatted = [* map(str, employeeids)]
        employeelisttoquery = '\''+'\',\''.join(employeeidslistformatted)+ '\''
        employeeidspart = f"""s.employeesunnsted->>'userId' in ({employeelisttoquery})"""
        wherelist = [employeeidspart,qdatefrompart,qdatetopart]
        wherelistfiltered = list(filter(None, wherelist))
        wherelocalpart = ' and '.join(wherelistfiltered)
        sessionquery = f"""select * from
        (select {fields},array_agg(employeesunnsted) as employees from
        (SELECT *,unnest(employees) employeesunnsted FROM {table}) s
        where {wherelocalpart}
        group by {fields}) ssn
        """
    else:
        wherelist = [qdatefrompart,qdatetopart]
        wherelistfiltered = list(filter(None, wherelist))
        wherelocalpart = ' and '.join(wherelistfiltered)
        sessionquery = f"""select * from
        (select {fields} from {table}) ssn
        where {wherelocalpart}"""

    if 'withOperations' in args['data']:
        args['data']['operationType'] = [1,2,3,4]

    if 'operationType' in args['data']:
        # фильтрация по id сессий
        operationtypes = {1:"serviceoperation",2:"goodsoperation",3:"spendoperation",4:"employeepayment"}
        querypartslist = []
        for item in args['data']['operationType']:
            table = operationtypes[item]
            if operationtypes[item] in ['serviceoperation','goodsoperation']:
                if 'clientIds' in args['data']:
                    clientids = args['data']['clientIds']
                    clientidslistformatted = [* map(str, clientids)]
                    clientidslisttoquery = '('+','.join(clientidslistformatted) + ')'
                    clientidspart = f"""
                    where \"clientId\" in {clientidslisttoquery}"""
                else:
                    clientidspart = ''
            qpart = f"""select "sessionId",'{table}' as type,row_to_json({table}) as params from {table}{clientidspart}"""
            querypartslist.append(qpart)
        unions = "\nunion all\n".join(querypartslist)
        queryoperations = f'''select c."sessionId",array_agg(row_to_json(c)::jsonb-'sessionId') as "Operations" from
        (select concatenated."sessionId",concatenated.type,array_agg(params) as operations from
        ({unions}) concatenated
        group by "sessionId",type) c
        group by "sessionId"'''

    query = f'''{sessionquery}
    inner join
    ({queryoperations}) operations
    on ssn.id = operations."sessionId"'''
    return query

def generateQueryRead(args=None):
    table = args['table']
    additionalpart = ''
    orderpart = ''
    wherepart = ''
    fields = '*'
    
    if 'fields' in args:
        fields = ','.join(args['fields'])
    
    if 'type' in args:
        if args['type'] == 'GetSessions':
            query = getSessionsQuery(args)
            
        else:
            if args['type'] in ['GetAdmins','GetMasters']:
                if args['type'] == 'GetMasters':
                    fields = '_user.' + ',_user.'.join(args['fields']) + ',b."servicePercent" as "masterServicePercent"'
                    additionalpart = f"""
                    left join
                    (select id,"servicePercent" from barbercategory) b
                    on _user."categoryId"=b.id"""

                rolesdict = {'GetAdmins':'officeAdmin','GetMasters':'master'}
                role = rolesdict[args['type']]
                wherepart = f"""
                where '{role}' = ANY (roles)"""
                orderpart = f"""
                order by state desc, name asc"""

            elif args['type'] == 'GetClients':
                string = args['data']['q'].lower()
                wherepart = f"""
                where name ilike '%{string}%'
                or  text(contacts) ilike '%{string}%'"""
                orderpart = f"""
                order by name asc"""
                
            if 'data' in args:
                wherepart = generateWhere(args['data'])
                
            query = f"""select {fields} from {table}{additionalpart}{wherepart}{orderpart}"""
        
    else:    
        if 'data' in args:
            wherepart = generateWhere(args['data'])            
            
        query = f"""select {fields} from {table}{additionalpart}{wherepart}{orderpart}"""
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
