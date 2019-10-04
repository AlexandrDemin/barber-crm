#!/usr/bin/env python
# coding: utf-8


import json
import psycopg2
import traceback

#DB
def prepareDataToUpsert(data):
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
    prepareDataToUpsert(data)
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
    return q
    
def generateQueryCreate(table,data):
    columns = '(\"' + "\",\"".join(list(data.keys() )) + '\")'
    prepareDataToUpsert(data)
    v = '(' + ",".join((list(data.values()))) + ')'
    
    values = v.replace('\'null\'','null')
    values = values.replace('[','array [')
    values = values.replace('}\']','}\']::json[]')

    q = f"""INSERT INTO {table} {columns}
    VALUES
    {values} RETURNING id"""
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

def getSessionsOperationsQuery(args):
    table = args['table']
    fields = ','.join(args['fields'])
    qdatefrompart = ''
    qdatetopart = ''
    idpart = ''
    statepart = ''
    officeIdpart = ''
    wherepartlist = []
        
    if 'dateFrom' in args['data']:
        date = args['data']['dateFrom']
        qdatefrompart = f"""\"dateOpened\" >= '{date}'""" 

    if 'dateTo' in args['data']:
        date = args['data']['dateTo']
        qdatetopart = f"""\"dateClosed\" <= '{date}'"""
        
    if 'id' in args['data']:
        _id = args['data']['id']
        idpart = f"""id = {_id}"""
        
    if 'state' in args['data']:
        state = args['data']['state']
        statepart = f"""state = '{state}'"""
        
    if '"officeId"' in args['data']:
        officeId = args['data']['"officeId"']
        officeIdpart = f"""\"officeId\" = {officeId}"""

    if 'employeeIds' in args['data']:
        fields_filtered = args['fields'].copy()
        fields_filtered.remove('"employees"')
        fieldsFiltered = ','.join(fields_filtered)
        employeeids = args['data']['employeeIds']
        employeeidslistformatted = [* map(str, employeeids)]
        employeelisttoquery = '\''+'\',\''.join(employeeidslistformatted)+ '\''
        employeeidspart = f"""s.employeesunnsted->>'userId' in ({employeelisttoquery})"""
        wherelist = [employeeidspart,qdatefrompart,qdatetopart,idpart,statepart,officeIdpart]
        wherelistfiltered = list(filter(None, wherelist))
        wherelocalpart = 'where ' + ' and '.join(wherelistfiltered)
        sessionquery = f"""select * from
        (select {fieldsFiltered},array_agg(employeesunnsted) as employees from
        (SELECT *,unnest(employees) employeesunnsted FROM {table}) s
        {wherelocalpart}
        group by {fieldsFiltered}) ssn
        """
    else:
        wherelist = [qdatefrompart,qdatetopart,idpart,statepart,officeIdpart]
        wherelistfiltered = list(filter(None, wherelist))
        if len(wherelistfiltered) != 0:
            wherelocalpart = 'where ' + ' and '.join(wherelistfiltered)
        else:
            wherelocalpart = ''
        sessionquery = f"""select * from
        (select {fields} from {table}
        {wherelocalpart}) ssn"""

    if 'withOperations' in args['data']:
        if args['data']['withOperations'] == 'true':
            args['data']['operationType'] = [1,2,3,4]

    if 'operationType' in args['data']:
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
        
    else:
        query = f'''{sessionquery}'''
    return query

def generateCustomerReportFinanceQuery(args):
    qdatefrompart1 = ''
    qdatetopart1 = ''
    qdatefrompart2 = ''
    qdatetopart2 = ''
    officeidspart = ''
    clientidspart = ''
    
    if 'dateFrom' in args['data']:
        date = args['data']['dateFrom']
        qdatefrompart1 = f"""\"datetime\" >= '{date}'"""
        qdatefrompart2 = f"""\"finishDatetime\" >= '{date}'"""
    
    if 'dateTo' in args['data']:
        date = args['data']['dateTo']
        qdatetopart1 = f"""\"datetime\" <= '{date}'"""
        qdatetopart2 = f"""\"finishDatetime\" <= '{date}'"""
    
    if 'clientIds' in args['data']:
        clientids = args['data']['clientIds']
        clientidslistformatted = [* map(str, clientids)]
        clientidslisttoquery = '('+','.join(clientidslistformatted) + ')'
        clientidspart = f"""\"clientId\" in {clientidslisttoquery}"""
        
    if 'officeIds' in args['data']:
        officeids = args['data']['clientIds']
        officeidslistformatted = [* map(str, officeids)]
        officeidslisttoquery = '('+','.join(officeidslistformatted) + ')'
        officeidspart = f"""\"officeId\" in {officeidslisttoquery}"""

    wherelist1 = [qdatefrompart1,qdatetopart1,clientidspart,officeidspart]
    wherelist2 = [qdatefrompart2,qdatetopart2,clientidspart,officeidspart]

    wherelistfiltered1 = list(filter(None, wherelist1))
    wherelistfiltered2 = list(filter(None, wherelist2))

    if len(wherelistfiltered1) != 0:
        where1 = 'where finance.' + ' and finance.'.join(wherelistfiltered1)
        where2 = 'where s.' + ' and s.'.join(wherelistfiltered2)
    else:
        where1 = ''
        where2 = ''
      
    query = f'''select * from (select finance.*,s.totalServiceSum,g.totalGoodsSum from
    (select datetime::date as datetime,count(*) as totalVisits,"officeId","clientId",
    sum("cashSum") as totalCash,sum("cashlessSum") as totalCashless,sum("discountSum") as totalDiscount,
    sum("cashlessSum") + sum("cashSum") as totalSum
    from 
    (select "officeId","clientId","finishDatetime" as datetime,"cashSum","cashlessSum","discountSum" from serviceoperation
    union
    select "officeId","clientId",datetime,"cashSum","cashlessSum","discountSum" from goodsoperation) u
    group by datetime::date,"officeId","clientId") finance
    left join
    (select "finishDatetime"::date as datetime,"officeId","clientId",sum("cashSum")+sum("cashlessSum") as totalServiceSum from serviceoperation
    group by "finishDatetime"::date,"officeId","clientId") s
    on finance."officeId"=s."officeId" and finance."clientId"=s."clientId" and finance.datetime=s.datetime
    left join
    (select datetime::date as datetime,"officeId","clientId",sum("cashSum")+sum("cashlessSum") as totalGoodsSum from goodsoperation
    group by datetime::date,"officeId","clientId") g
    on finance."officeId"=g."officeId" and finance."clientId"=g."clientId" and finance.datetime=g.datetime
    {where1}) x
    left join
    (select "officeId","clientId", array_agg(mastervisits) as  mastervisits from
    (select "officeId","clientId",json_build_object('name',usr.name,'count',count(*)) as mastervisits from serviceoperation s
    left join
    (select id,name from _user) usr
    on s."masterId"=usr.id
    {where2}
    group by "officeId","clientId",name) mv
    group by "officeId","clientId"
    ) as masternames
    on x."officeId"=masternames."officeId" and x."clientId"=masternames."clientId"'''

    return query

def generateCustomerReportVisitsQuery(args=None):
    
    lostdayscriterion = 60
    likelylostdayscriterion = 40
    loyalvisitscriterion = 3
    likelyloyalvisitscriterion = 2
    lastndays = 120
    
    if args:
        if 'lostdayscriterion' in args:
            lostdayscriterion = args['lostdayscriterion']
        if 'likelylostdayscriterion' in args:
            likelylostdayscriterion = args['likelylostdayscriterion']
        if 'loyalvisitscriterion' in args:
            loyalvisitscriterion = args['loyalvisitscriterion']
        if 'likelyloyalvisitscriterion' in args:
            likelyloyalvisitscriterion = args['likelyloyalvisitscriterion']
        if 'lastndays' in args:
            lastndays = args['lastndays']

    query = f"""select visits.*,lastvisit.lastvisitdatetime, 
    case 
        WHEN lastvisit.lastvisitdatetime < now() - interval '{lostdayscriterion} days'::interval THEN 'lost'
        WHEN lastvisit.lastvisitdatetime < now() - interval '{likelylostdayscriterion} days'::interval and
        lastvisit.lastvisitdatetime >= now() - interval '{lostdayscriterion} days'::interval THEN ' likely lost'
        when visits.lastndaysvisitscount >= {loyalvisitscriterion} then 'loyal'
        when visits.lastndaysvisitscount >= {likelyloyalvisitscriterion} then 'likely loyal'
        ELSE 'ambivalent'
    end as loyalty,
    case
        when visits.lastndaysvisitscount < visits.totalvisits then false
        else true
    end as newclient from 
    ((select "clientId", 
    count(*) as totalvisits,
    count(*) filter (where datetime >= now() - '{lastndays} days'::interval) as lastndaysvisitscount 
    from ( 
    select "clientId","finishDatetime"::date as datetime from serviceoperation
    union
    select "clientId",datetime::date as datetime from goodsoperation) v
    group by "clientId") visits
    inner join
    (select "clientId",max("finishDatetime"::date) as lastvisitdatetime from serviceoperation
    group by "clientId"
    union
    select "clientId",max(datetime::date) as lastvisitdatetime from goodsoperation
    group by "clientId") lastvisit
    on visits."clientId" = lastvisit."clientId")"""
    
    return query

def GenerateFinanceReportQuery(args=None):
    wherequery = "where datetime >= date_trunc('month', CURRENT_DATE)"
    if args:
        pass
    
    query = f"""select incomeoperationcount+expenseoperationcount as operationcount,
    totalincome."officeId",office.name as officename,
    totalincome.totalcash,totalincome.totalcashless,totalincome.totalincome,
    totalexpenses.totalExpenses,
    totalincome.totalIncome-totalexpenses.totalExpenses as totalrevenue from
    (
    (select count(*) as incomeoperationcount,"officeId",sum("cashSum") as totalcash,
    sum("cashlessSum") as totalcashless,sum("cashSum")+sum("cashlessSum") as totalIncome,
    array_agg(categoryIncome) as operationsIncome from 
    (select "officeId","finishDatetime" as datetime,"cashSum","cashlessSum","cashSum"+"cashlessSum" as totalIncome, 
    json_build_object('totalServiceIncome',"cashSum"+"cashlessSum")  as categoryIncome
    from serviceoperation
    union all
    select "officeId",datetime,"cashSum","cashlessSum","cashSum"+"cashlessSum" as totalIncome,
    json_build_object('totalGoodsIncome',"cashSum"+"cashlessSum")  as categoryIncome
    from goodsoperation) income
    {wherequery}
    group by "officeId") totalincome
    inner join
    (select count(*) as expenseoperationcount,"officeId",sum(totalExpenses) as totalExpenses from
    (select "officeId",datetime,"cashSum"+"cashlessSum" as totalExpenses from spendoperations
    union all
    select "officeId",datetime,"cashSum"+"cashlessSum" as totalExpenses from employeepayment) expenses
    {wherequery}
    group by "officeId") totalexpenses
    on totalincome."officeId" = totalexpenses."officeId"
    inner join
    (select id,name from office) office
    on totalincome."officeId" = office.id
    )"""
    
    return query

def generateQueryRead(args):
    table = args['table']
    additionalpart = ''
    orderpart = ''
    wherepart = ''
    fields = '*'
    
    if 'fields' in args:
        fields = ','.join(args['fields'])
    
    if 'type' in args:
        if args['type'] == 'GetSessions':
            query = getSessionsOperationsQuery(args)
            
        if args['type'] == 'generateCustomerReportFinance':
            query = generateCustomerReportFinanceQuery(args)  
            
        if args['type'] == 'GenerateCustomerReportVisits':
            query = GenerateCustomerReportVisitsQuery(args)
            
        if args['type'] == 'GenerateFinanceReport':
            query = GenerateFinanceReportQuery(args) 
            
        else:
            if args['type'] in ['GetAdmins','GetMasters']:
                if args['type'] == 'GetMasters':
                    fields = 'employee.' + ',employee.'.join(args['fields']) + ',b."servicePercent" as "masterServicePercent"'
                    additionalpart = f"""
                    left join
                    (select id,"servicePercent" from barbercategory) b
                    on employee."categoryId"=b.id"""

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
    print(query)
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
        stacktrace = traceback.format_exc()
        return {'error':e,'stacktrace':stacktrace}
