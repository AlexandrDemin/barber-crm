#!/usr/bin/env python
# coding: utf-8


import json
import psycopg2
from psycopg2.extras import RealDictCursor
import traceback
import re

#DB
def generateDateQueryPart(columnname,sign,dateraw):
    dateregexp = re.compile(r'(\d\d)\.(\d\d)\.(\d\d\d\d)')
    try:
        d = dateregexp.search(dateraw)
        date = d.group(3)+'-'+d.group(2)+'-'+d.group(1)
        qdatepart = f"""{columnname} {sign} '{date}'"""
    except:
        date = dateraw
        qdatepart = f"""{columnname} {sign} {date}"""
    return qdatepart

def generateIdsQueryPart(idslist,fieldname):
    listformatted = [* map(str, idslist)]
    listtoquery = '('+','.join(listformatted) + ')'
    idspart = f"""{fieldname} in {listtoquery}"""
    return idspart

def generateWhereFromList(wherelist):
    wherelistfiltered = list(filter(None, wherelist))
    if len(wherelistfiltered) != 0:
        where = 'where ' + ' and '.join(wherelistfiltered)
    else:
        where = ''
    return where

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
        qpart = f"""\"{key}\" = {value}"""
        queryparts.append(qpart)
    setquery = ', '.join(queryparts)
    setquery = setquery.replace('None','null')
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
    
    values = v.replace('None','null')
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
        if type(value) == str:
            wherepart = f"""\"{key}\" = '{value}'"""
        else:
            wherepart = f"""\"{key}\" = {value}"""
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
    officeidspart = ''
    wherepartlist = []
        
    if 'dateFrom' in args['data']:
        dateraw = args['data']['dateFrom']
        qdatefrompart = generateDateQueryPart('"dateOpened"','>=',dateraw)

    if 'dateTo' in args['data']:
        dateraw = args['data']['dateTo']
        qdatefrompart = generateDateQueryPart('"dateOpened"','<=',dateraw)
        
    if 'id' in args['data']:
        _id = args['data']['id']
        idpart = f"""id = {_id}"""
        
    if 'state' in args['data']:
        state = args['data']['state']
        statepart = f"""state = '{state}'"""
        
    if 'officeId' in args['data']:
        officeid = args['data']['officeId']
        officeidspart = f"""\"officeId\" = {officeid}"""

    if 'employeeIds' in args['data']:
        fields_filtered = args['fields'].copy()
        fields_filtered.remove('"employees"')
        fieldsFiltered = ','.join(fields_filtered)
        employeeids = args['data']['employeeIds']
        employeeidslistformatted = [* map(str, employeeids)]
        employeelisttoquery = '\''+'\',\''.join(employeeidslistformatted)+ '\''
        employeeidspart = f"""s.employeesunnsted->>'userId' in ({employeelisttoquery})"""
        wherelist = [employeeidspart,qdatefrompart,qdatetopart,idpart,statepart,officeidspart]
        wherelistfiltered = list(filter(None, wherelist))
        wherelocalpart = 'where ' + ' and '.join(wherelistfiltered)
        sessionquery = f"""select * from
        (select {fieldsFiltered},array_agg(employeesunnsted) as employees from
        (SELECT *,unnest(employees) employeesunnsted FROM {table}) s
        {wherelocalpart}
        group by {fieldsFiltered}) ssn
        """
    else:
        wherelist = [qdatefrompart,qdatetopart,idpart,statepart,officeidspart]
        wherelocalpart = generateWhereFromList(wherelist)
        sessionquery = f"""select * from
        (select {fields} from {table}
        {wherelocalpart}) ssn"""

    if 'withOperations' in args['data']:
        if args['data']['withOperations'] == True:
            args['data']['operationType'] = ['serviceoperation','goodsoperation',"spendoperation","employeepayment"]

    if 'operationType' in args['data']:
        if args['data']['operationType'] = []:
            args['data']['operationType'] = ['serviceoperation','goodsoperation',"spendoperation","employeepayment"]
        clientidspart = ''
        querypartslist = []
        for item in args['data']['operationType']:
            table = item
            if item in ['serviceoperation','goodsoperation']:
                if 'clientIds' in args['data']:
                    clientids = args['data']['clientIds']
                    clientidspartlist = [generateIdsQueryPart(clientids,'"clientId"')]
                    clientidspart = generateWhereFromList(clientidspartlist)
            qpart = f"""select "sessionId" as id,row_to_json({table})::jsonb||jsonb_build_object('type', '{table}') as params from {table} {clientidspart}"""
            querypartslist.append(qpart)
        unions = "\nunion all\n".join(querypartslist)
        queryoperations = f'''select concatenated.id,array_agg(params::jsonb-'sessionId') as operations from
        ({unions}) concatenated
        group by id'''

        query = f'''{sessionquery}
        left join
        ({queryoperations}) operations
        using (id)'''
        
    else:
        query = f'''{sessionquery}'''
    return query

def GenerateClientReportQuery(args):
    officeidspart = ''
    clientidspart = ''
    
    if 'period' in args['data']:
        dateraw = args['data']['period']
    else:
        dateraw = "date_trunc('day',now())"
    datepart = generateDateQueryPart('yearmonth','=',dateraw)
    
    if 'clientIds' in args['data']:
        clientids = args['data']['clientIds']
        clientidspart = generateIdsQueryPart(clientids,'"clientId"')
        
    if 'officeIds' in args['data']:        
        officeids = args['data']['officeIds']
        officeidspart = generateIdsQueryPart(officeids,'"officeId"')
        
    wherelist = [datepart,clientidspart,officeidspart]
    
    where = generateWhereFromList(wherelist)
    
    globalquery = 'select * from'
    officegrouping = ''
    globalqueryallofficepart = f'''sum(totalcash) as totalcash,
sum(totalcashless) as totalcashless,
sum(totaldiscount) as totaldiscount,
sum(totalservicesum) as totalservicesum,
sum(totalgoodssum) as totalgoodssum,
sum(totalsum) as totalsum,
sum(totalvisitsduringperiod)::int as totalvisitsduringperiod'''
    
    if args['data']['groupingtype'] == 'office':
        globalquery = f'''select "officeId",
{globalqueryallofficepart}
from'''
        officegrouping = 'group by "officeId"'
    
    if args['data']['groupingtype'] == 'all':
        globalquery = f"""select
{globalqueryallofficepart}
from""" 
    
    lostdayscriterion = 60
    likelylostdayscriterion = 40
    loyalvisitscriterion = 3
    likelyloyalvisitscriterion = 2
    lastndays = 120
    
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

    query = f"""{globalquery} 
(select yearmonth,"officeId","clientId",
sum("cashSum") as totalCash,sum("cashlessSum") as totalCashless,sum("discountSum") as totalDiscount,
sum("cashSum")filter (where type = 'service') + sum("cashlessSum")filter (where type = 'service')  as totalServiceSum,
sum("cashSum")filter (where type = 'good') + sum("cashlessSum")filter (where type = 'good') as totalGoodsSum,
sum("cashlessSum") + sum("cashSum") as totalSum
from 
(select 'service' as type,"officeId","clientId", date_trunc('month',"finishDatetime") as yearmonth,"cashSum","cashlessSum","discountSum" from serviceoperation
union
select 'good' as type,"officeId","clientId",date_trunc('month',datetime) as yearmonth,"cashSum","cashlessSum","discountSum" from goodsoperation) u
group by yearmonth,"officeId","clientId") finance
left join
(select "officeId","clientId",yearmonth, array_agg(mastervisits) as  mastervisits from
(select date_trunc('month',"finishDatetime") as yearmonth,"officeId","clientId",json_build_object('name',usr.name,'count',count(*)) as mastervisits from serviceoperation s
left join
(select id,name from employee) usr
on s."masterId"=usr.id
group by "officeId","clientId",name,yearmonth) mv
group by "officeId","clientId",yearmonth
) as masternames
using (yearmonth,"officeId","clientId")
left join
(select "officeId","clientId",yearmonth,count(*) as totalvisitsduringperiod from (select "officeId","clientId", date_trunc('month',"finishDatetime") as yearmonth from serviceoperation
union
select "officeId","clientId",date_trunc('month',datetime) as yearmonth from goodsoperation) cnt
group by "officeId","clientId",yearmonth
) visitcount
using (yearmonth,"officeId","clientId")
left join
(select id as "clientId",name from client) cl
using ("clientId")
left join
(select visits.*,lastvisit.lastvisitdatetime,
case 
    WHEN lastvisit.lastvisitdatetime < now() - interval '60 days'::interval THEN 'lost'
    WHEN lastvisit.lastvisitdatetime < now() - interval '40 days'::interval and
    lastvisit.lastvisitdatetime >= now() - interval '60 days'::interval THEN ' likely lost'
    when visits.lastndaysvisitscount >= 3 then 'loyal'
    when visits.lastndaysvisitscount >= 2 then 'likely loyal'
    ELSE 'ambivalent'
end as loyalty,
case
    when visits.lastndaysvisitscount < visits.totalvisits then false
    else true
end as newclient from 
((select "clientId","officeId",
count(*) as totalvisits,
count(*) filter (where datetime >= now() - '120 days'::interval) as lastndaysvisitscount 
from ( 
select "officeId","clientId","finishDatetime"::date as datetime from serviceoperation
union
select "officeId","clientId",datetime::date as datetime from goodsoperation) v
group by "officeId","clientId") visits
inner join
(select "officeId","clientId",max("finishDatetime"::date) as lastvisitdatetime from serviceoperation
group by "officeId","clientId"
union
select "officeId","clientId",max(datetime::date) as lastvisitdatetime from goodsoperation
group by "officeId","clientId") lastvisit
using ("officeId","clientId"))) visitstats
using ("officeId","clientId")
{where}
{officegrouping}"""
    
    return query

def GenerateFinanceReportQuery(args):
    globalquery = 'select * from'
    globalqueryclose = ''
    
    officeidspart = ''
        
    if 'period' in args['data']:
        dateraw = args['data']['period']
    else:
        dateraw = "date_trunc('month',now())"
    datepart = generateDateQueryPart("yearmonth",'=',dateraw)
        
    if 'officeIds' in args['data']:
        officeids = args['data']['officeIds']
        officeidspart = generateIdsQueryPart(officeids,'"officeId"')
    
    wherelist = [datepart,officeidspart]
    where = generateWhereFromList(wherelist)

    if args['data']['groupingtype'] == 'all':
        globalquery = f"""select 
sum(operationcount) as operationcount,sum(serviceoperationcount)::int as serviceoperationcount,sum(goodsoperationcount)::int as goodsoperationcount, sum(spendoperationcount)::int as spendoperationcount,
sum(serviceIncome) as serviceIncome,sum(goodsIncome) as goodsIncome,
sum(totalcash) as totalcash,sum(totalcashless) as totalcashless,
sum(totalIncome) as totalIncome,sum(totalspend) as totalspend,sum(totalrevenue) as totalrevenue,
sum(totalemployees)::int as totalemployees, sum(total_time) as total_time
from""" 
    
    query = f"""{globalquery}
(select "officeId",yearmonth,
count(*)::int as operationcount,count(*) filter (where category = 'serviceoperation') as serviceoperationcount,count(*) filter (where category = 'goodsoperation') as goodsoperationcount,
count(*) filter (where category = 'spend') as spendoperationcount,
sum("cashSum")filter (where category = 'serviceoperation')+sum("cashlessSum")filter (where category = 'serviceoperation') as serviceIncome,
sum("cashSum")filter (where category = 'goodsoperation')+sum("cashlessSum")filter (where category = 'goodsoperation') as goodsIncome,
sum("cashSum") as totalcash, sum("cashlessSum") as totalcashless,
sum(totalIncome) as totalIncome, sum(totalspend) as totalspend, sum(totalIncome) - sum(totalspend) as totalrevenue
from 
(select 'serviceoperation' as category,"officeId",date_trunc('month',"finishDatetime") as yearmonth,"cashSum","cashlessSum","cashSum"+"cashlessSum" as totalIncome, null::float as totalspend
from serviceoperation
union all
select 'goodsoperation' as category,"officeId",date_trunc('month',datetime) as yearmonth,"cashSum","cashlessSum","cashSum"+"cashlessSum" as totalIncome, null::float as totalspend
from goodsoperation
union all
select 'spend' as category,"officeId",date_trunc('month',datetime) as yearmonth, null as "cashSum", null as "cashlessSum", null::float as totalIncome,"cashSum"+"cashlessSum" as totalspend from spendoperation
union all
select 'spend' as category,"officeId",date_trunc('month',datetime) as yearmonth, null as "cashSum", null as "cashlessSum", null::float as totalIncome,"cashSum"+"cashlessSum" as totalspend from employeepayment) finance
group by "officeId",yearmonth) finance
left join
(select "officeId", count(distinct employeeid) as totalemployees,sum(total_time) as total_time,yearmonth from
(select "officeId",date_trunc('month',"dateOpened") as yearmonth,
cast((unnest(employees)->'userId')::text as int) as employeeid,
cast((unnest(employees)->'workHours')::text as int) as total_time
from session) a
group by "officeId",yearmonth) worktime 
using ("officeId",yearmonth)
{where}"""
    
    return query

def GenerateEmployeeReportQuery(args):
    officeidspart = ''
    employeeidspart = ''
    
    wherepartyearmonth = ''
    wherepartemployeeid = ''
    wherepart = ''
    
    if 'period' in args['data']:
        dateraw = args['data']['period']
    else:
        dateraw = "date_trunc('day',now())"
    datepart = generateDateQueryPart('yearmonth','=',dateraw)
        
    if 'employeeIds' in args['data']:
        employeeids = args['data']['employeeIds']
        employeeidspart = generateIdsQueryPart(employeeids,'employeeid')
        
    if 'officeIds' in args['data']:
        officeids = args['data']['officeIds']
        officeidspart = generateIdsQueryPart(officeids,'"officeId"')
    
    wherelist = [datepart,employeeidspart,officeidspart]
    wherepart = generateWhereFromList(wherelist)
    
    wherelistemployee = [employeeidspart]
    wherepartemployeeid = generateWhereFromList(wherelistemployee)
    
    wherelistdate = [datepart]
    wherepartyearmonth = generateWhereFromList(wherelistdate)

    employeeinfopart = f"""-- сперва выбираем общую справочную информацию по всем работникам
    select * from (select 'a' as joinfield, id as employeeid,name,roles,"categoryId",salary,"servicePercent","goodsPercent",state from employee) u
    {wherepartemployeeid}) userinfo"""

    employeepaymentspart = f"""-- присоединяем данные по выплатам сотрудникам: зарплата, премия (за услуги и проданные товары), штрафы
    left join
    (select * from (select "officeId","employeeId" as employeeid,date_trunc('month',datetime) as yearmonth,
    sum(sum)filter (where "employeePaymentTypeId" = 1) as paidsalary, 
    sum(sum)filter (where "employeePaymentTypeId" = 2) as paidbonus,
    sum(sum)filter (where "employeePaymentTypeId" = 3) as penalty
    from employeepayment
    group by "employeeId",yearmonth,"officeId") p
    {wherepart}) payments
    using (employeeid)"""

    barberservicepercentpart = f"""-- присоединяем коэффициент отчисления за услуги барберу, который зависит от категории
    left join
    (select id as "categoryId","servicePercent" as barberservicepercent from barbercategory) barberservicepercent
    using ("categoryId")"""

    servicebonuspart = f"""-- присоединяем сумму, полученную с операций по услугам админами
    left join
    (select * from (select "officeId", date_trunc('month',"finishDatetime") as yearmonth,
    "adminId" as employeeid,
    sum("cashSum"+"cashlessSum") as totalServiceSum, 
    null as servicecount 
    from serviceoperation
    group by "officeId",yearmonth,"adminId"
    -- объединяем с аналогичными данными по мастерам
    union
    select "officeId", date_trunc('month',"finishDatetime") as yearmonth,
    "masterId" as employeeid,
    sum("cashSum"+"cashlessSum") as totalServiceSum, 
    count(*)::int as servicecount 
    from serviceoperation
    group by "officeId",yearmonth,"masterId")ss
    {wherepart}) servicesum
    using (employeeid)"""

    goodsbonuspart = f"""-- присоединяем сумму, полученную с операций по товарам админами
    left join
    (select * from (select "officeId",date_trunc('month',datetime) as yearmonth,
    "adminId" as employeeid,
    sum("cashSum"+"cashlessSum") as totalGoodsSum 
    from goodsoperation
    group by "officeId",yearmonth,"adminId"
    -- объединяем с аналогичными данными по мастерам
    union
    select "officeId",date_trunc('month',datetime) as yearmonth,
    "masterId" as employeeid,
    sum("cashSum"+"cashlessSum") as totalGoodsSum 
    from goodsoperation
    group by "officeId",yearmonth,"masterId")g
    {wherepart}) goodssum
    using (employeeid)"""

    worktimepart = f"""-- присоединяем количество часов, отработанных работниками, их достаем из json-ов
    left join 
    (select "officeId",employeeid, sum(total_time) as total_time,yearmonth from
    (select "officeId",date_trunc('month',"dateOpened") as yearmonth,
    cast((unnest(employees)->'userId')::text as int) as employeeid,
    cast((unnest(employees)->'workHours')::text as int) as total_time
    from session) a
    {wherepart}
    group by "officeId",employeeid,yearmonth) worktime
    using (employeeid)"""

    repeatingvisitscount = f"""    -- присоединяем рассчитанное количество повторных визитов
    -- здесь во вложенном запросе сперва считается количество уникальных комбинаций мастер-клиент
    -- затем комбинация мастер-клиент встречается больше 1 раза, то к счетчику повторных визитов прибавляется 1
    left join 
    (select employeeid,sum(CASE WHEN repeatingvisitscount > 1 THEN 1 ELSE 0 END)::int as repeatingvisitscount from
	(select "masterId" as employeeid, count(*) as repeatingvisitscount from serviceoperation 
	where ("masterId", "clientId") in (
	(select "masterId", "clientId" from (SELECT DISTINCT "officeId",date_trunc('month',"finishDatetime") as yearmonth,"masterId", "clientId" FROM serviceoperation) sd 
	{wherepart}))
	group by "masterId", "clientId") repeatingvisits
	group by employeeid) repeatingvisitscount
    using (employeeid)"""
        
    totalworkinghourspart = f"""-- присоединяем общее число рабочих часов в периоде по дням, когда хотя бы в одном отделении была хотя бы одна операция
    -- просто перем список дат операций, урезанных до дня, считаем количество уникальных дней и умножаем на 8
    left join
    (select 'a' as joinfield, '8 hours'::interval*count(*) as estimatedworkhours from
    (select date_trunc('day',"finishDatetime") as yearmonthday,date_trunc('month',"finishDatetime") as yearmonth from serviceoperation
    union
    select date_trunc('day',datetime) as yearmonthday,date_trunc('month',datetime) as yearmonth from goodsoperation
    union
    select date_trunc('day',datetime) as yearmonthday,date_trunc('month',datetime) as yearmonth from spendoperation
    union
    select date_trunc('day',datetime) as yearmonthday,date_trunc('month',datetime) as yearmonth from employeepayment)d
    {wherepartyearmonth}) dayswithoperations
    using (joinfield)"""
    
    
    officenamejoinpart = f"""-- отдельно к верхнеуровневому селекту джоиним названия офисов
    -- джоиним именно к верхнеуровневому, потому что на более низком уровне у нашей референтной таблицы employee нет привязанных офисов
    left join
    (select id as "officeId",name as officename from office) office
    using ("officeId")"""
    
    globalquery = 'select * from'
    officegrouping = ''
    globalqueryallofficepart = f'''sum(salary) as totalsalary,sum(paidsalary) as totalpaidsalary,sum(penalty) as totalpenalty,sum(unpaidsalary) as totalunpaidsalary,
    sum(servicecount) as totalservicecount,sum(repeatingvisitscount) as totalrepeatingvisitscount,sum(totalServiceSum) as totaltotalServiceSum,
    sum(servicebonus) as totalservicebonus,
    sum(goodsbonus) as totalgoodsbonus,
    sum(paidbonus) as totalpaidbonus,
    sum(unpaidbonus) as totalunpaidbonus,
    sum(workload) as totalworkload'''
    
    if args['data']['groupingtype'] == 'office':
        globalquery = f'''select "officeId",
    {globalqueryallofficepart}
    from'''
        officegrouping = 'group by "officeId"'

    if args['data']['groupingtype'] == 'all':
        globalquery = f'''select
    {globalqueryallofficepart}
    from'''
        officenamejoinpart = ''

    query = f"""{globalquery}
    -- следующий селект - селект поверх большого числа джоинов. 
    -- в нем выбираются все нужные параметры и высчитываются недостающие
    (select name, worktime."officeId" as "officeId",state, roles,
    salary,paidsalary,penalty,salary - paidsalary + penalty as unpaidsalary,
    "categoryId","servicePercent" as adminservicepercent, barberservicepercent,
    servicecount, repeatingvisitscount, totalServiceSum,
    totalServiceSum * (case 
    when barberservicepercent is not null then barberservicepercent
    else "servicePercent" end) as servicebonus,
    "goodsPercent",totalGoodsSum,totalGoodsSum * "goodsPercent" as goodsbonus,
    paidbonus, totalServiceSum * (case 
    when barberservicepercent is not null then barberservicepercent
    else "servicePercent" end) + totalGoodsSum * "goodsPercent" - paidbonus as unpaidbonus,
    total_time,estimatedworkhours,EXTRACT(epoch FROM total_time)/ EXTRACT(epoch FROM estimatedworkhours) as workload
    from
    ({employeeinfopart}
    {employeepaymentspart}
    {barberservicepercentpart}
    {servicebonuspart}
    {goodsbonuspart}
    {worktimepart}
    {repeatingvisitscount}
    {totalworkinghourspart}
    ) reportmain
    {officenamejoinpart}
    {officegrouping}
    """
    
    return query

def generateQueryRead(args):
    if 'table' in args:
        table = args['table']
    else:
        table = ''
    additionalpart = ''
    orderpart = ''
    wherepart = ''
    fields = '*'
    
    if 'fields' in args:
        fields = ','.join(args['fields'])
    
    if 'type' in args:
        if args['type'] == 'GetSessions':
            query = getSessionsOperationsQuery(args)
            
        elif args['type'] == 'GenerateClientReport':
            query = GenerateClientReportQuery(args)  
            
        elif args['type'] == 'GenerateEmployeeReport':
            query = GenerateEmployeeReportQuery(args)
            
        elif args['type'] == 'GenerateFinanceReport':
            query = GenerateFinanceReportQuery(args)
            
        else:
            if 'data' in args:
                wherepart = generateWhere(args['data'])
            
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
                
            elif args['type'] == 'GetClient':
                fields = 'client.*,operations."Operations"'
                orderpart = f"""
                order by name asc"""
                additionalpart = f"""
left join
(select c."clientId",array_agg(row_to_json(c)::jsonb-'clientId') as "Operations" from
(select concatenated."clientId",concatenated.type,array_agg(params::jsonb-'clientId') as operations from
(select "clientId",'serviceoperation' as type,row_to_json(serviceoperation) as params from serviceoperation 
union all
select "clientId",'goodsoperation' as type,row_to_json(goodsoperation) as params from goodsoperation) concatenated
group by "clientId",type) c
group by "clientId") operations
on client.id = operations.\"clientId\""""
                                
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
            result_data = result_data[0]
        else:
            result_data = cur.fetchall()
        cur.close()
        conn.close()
        if len(result_data) == 0:
            if commit == False:
                return {'warning':'Нет таких данных'}
            else:
                return {'error':'Не удалось добавить данные'}
        else:
            return result_data
    except Exception as e:
        stacktrace = traceback.format_exc()
        return {'error':str(e),'stacktrace':stacktrace}

