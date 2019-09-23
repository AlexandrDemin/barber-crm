#!/usr/bin/env python
# coding: utf-8

# In[133]:


import json
import psycopg2


# # Создание базы, таблиц и пользователей

# In[ ]:


CREATE DATABASE barbers;

CREATE TABLE OFFICE(
id SERIAL PRIMARY KEY NOT NULL,
name TEXT NOT NULL,
city TEXT NOT NULL,
address TEXT NOT NULL,
coordinatex FLOAT NOT NULL,
coordinatey FLOAT NOT NULL,
state TEXT NOT NULL);

CREATE TABLE BARBERCATEGORY(
id SERIAL PRIMARY KEY NOT NULL,
"name" TEXT NOT NULL,
"servicePercent" FLOAT(2) NOT NULL,
"state" TEXT NOT NULL);

CREATE TABLE GOOD(
id SERIAL PRIMARY KEY NOT NULL,
name TEXT NOT NULL,
price FLOAT(2) NOT NULL,
state TEXT NOT NULL);

CREATE TABLE SPENDTYPE(
id SERIAL PRIMARY KEY NOT NULL,
name TEXT NOT NULL,
"defaultPrice" FLOAT(2),
state TEXT NOT NULL);

CREATE TABLE CLIENT(
id SERIAL PRIMARY KEY NOT NULL,
name TEXT NOT NULL,
contacts JSONB [],
comment TEXT);

CREATE TABLE _USER(
id SERIAL PRIMARY KEY NOT NULL,
name TEXT NOT NULL,
"pictureUrl" TEXT,
roles TEXT [],
salary FLOAT(2) NOT NULL,
"servicesPercent" FLOAT(2),    
"goodsPercent" FLOAT(2) NOT NULL,
"categoryId" INT,
state TEXT NOT NULL,
"clientRating" FLOAT(2),
"controlRating" FLOAT(2),
login TEXT,
password TEXT,
contacts JSONB);

CREATE TABLE SERVICEOPERATION(
id SERIAL PRIMARY KEY NOT NULL,
"officeId" INT,
"sessionId" INT,
"serviceId" INT NOT NULL,
"startdatetime" TIMESTAMP NOT NULL,
"finishdatetime" TIMESTAMP NOT NULL,
"adminId" INT NOT NULL,
"masterId" INT NOT NULL,    
"clientId" INT,
"cashSum" FLOAT(2),
"cashlessSum" FLOAT(2),
"discountSum" FLOAT(2),
"bonusSum" FLOAT(2), 
"totalRevenue" FLOAT(2),
"clientRating" FLOAT(2),
"review" TEXT, 
"photoUrls" TEXT [],
"comment" TEXT, 
"controlrating" FLOAT(2));


CREATE TABLE GOODSOPERATION(
id SERIAL PRIMARY KEY NOT NULL,
"officeId" INT,
"sessionId" INT,
"goodsIds" INT [] NOT NULL,
"datetime" TIMESTAMP NOT NULL,    
"adminId" INT NOT NULL,
"masterId" INT NOT NULL,    
"clientId" INT,
"cashSum" FLOAT(2),
"cashlessSum" FLOAT(2),
"discountSum" FLOAT(2),
"bonusSum" FLOAT(2),
"totalRevenue" FLOAT(2),
"comment" TEXT);

CREATE TABLE SPENDOPERATIONS(
id SERIAL PRIMARY KEY NOT NULL,
"officeId" INT,
"sessionId" INT,
"expenseTypeId" INT NOT NULL,
datetime TIMESTAMP NOT NULL,
sum FLOAT(2),
"cashSum" FLOAT(2),
"card" FLOAT(2),
"cashlessSum" INT NOT NULL,
"comment" TEXT);

CREATE TABLE EMPLOYEEPAYMENT(
id SERIAL PRIMARY KEY NOT NULL,
"officeId" INT,
"sessionId" INT,
"employeeId" INT NOT NULL,
"datetime" TIMESTAMP NOT NULL,
"totalSpent" FLOAT(2),
sum FLOAT(2),
"cashSum" FLOAT(2),
"card" FLOAT(2),
"cashlessSum" INT NOT NULL,
"comment" TEXT);

CREATE TABLE SESSION(
id SERIAL PRIMARY KEY NOT NULL,
"officeId" INT,
"dateOpened" TIMESTAMP NOT NULL,
"dateClosed" TIMESTAMP,
state TEXT NOT NULL,
"userId" INT NOT NULL,
employees JSON [],
"openCash" FLOAT(2) NOT NULL,
"closeCash" FLOAT(2),
"totalIncomeCash" FLOAT(2),
"totalIncomeCashless" FLOAT(2),
"totalIncome" FLOAT(2),
"totalExpense" FLOAT(2),
"totalProfit" FLOAT(2));

CREATE TABLE SERVICE(
id SERIAL PRIMARY KEY NOT NULL,
name TEXT NOT NULL,
prices JSONB [] NOT NULL,
state TEXT NOT NULL);

CREATE ROLE read_only WITH LOGIN PASSWORD 'User_ro';
GRANT SELECT on ALL tables in schema public to read_only;

CREATE ROLE read_write WITH LOGIN PASSWORD 'Rw_Us3r';
GRANT SELECT,INSERT on ALL tables in schema public to read_write;

CREATE ROLE admin WITH LOGIN PASSWORD 'Adm1n1strat0r';
GRANT ALL PRIVILEGES ON DATABASE barbers to admin;


# # Наполнение таблиц

# In[ ]:


usr = {'name':'_user','data':[{ # id:1,
'name':'Иванов Диего Михайлович',
'pictureUrl':'www.mysite.com',
'roles':['officeAdmin'],
'currentdepartmentid':1,
'salary':100000,
'goodshare':0.1,
'qualification':'null',
'status':'working',
'clientrating':'null',
'controlrating':'null',
'login':'login',
'password':'password'},
{ # id:2,
'name':'Парикмахеров Парикмахер Парикмахерович',
'pictureUrl':'www.wikipedia.org',
'roles':['manager'],
'currentdepartmentid':1,
'salary':200000,
'goodshare':0.1,
'qualification':'null',
'status':'working',
'clientrating':'null',
'controlrating':'null',
'login':'login2',
'password':'password2'},
{ # id:3,
'name':'Морковная Залупа Павловна',
'pictureUrl':'www.vk.com',
'roles':['master'],
'currentdepartmentid':1,
'salary':50000,
'goodshare':0.1,
'qualificationid':1,
'status':'working',
'clientrating':10,
'controlrating':10,
'login':'login3',
'password':'password3'},
{ # id:4,
'name':'Барберов Бородач Ножницевич',
'pictureUrl':'www.ingate.ru',
'roles':['master'],
'currentdepartmentid':1,
'salary':50000,
'goodshare':0.1,
'qualificationid':2,
'status':'working',
'clientrating':10,
'controlrating':10,
'login':'login3',
'password':'password3'}]
}

bq = {'name':'barberqualification','data':[{ #'id':1,
'name':'Старший мастер',
'serviceshare': 0.5,
'status':'active'},
{ #'id':2,
'name':'Младший мастер',
'serviceshare': 0.2,
'status':'active'}]}

cl = {'name':'client','data':[{ #id:1,
'name':'Клиентов Клиент Клиентович',
'contacts':{
    'phone':'+79996669966',
    'mail':'mail@mail.com',
    'vk':'vk.com'
            }
   },{ #id:2,
'name':'Клиентов Клиент Клиентович',
'contacts':{
    'phone':'+79009009090',
    'mail':'mail2@mail.com',
    'vk':'vk2.com'
            }
   }]
}

srvc = {'name':'service','data':[{ #'id':1,
'name':'Стрижка мужская',
'prices': [500.00,600.00,700.00,800.00],
'status':'active'},
{ #'id':2,
'name':'Стрижка женская',
'prices':[1000.00,1100.00,1200.00,1300.00],
'status':'active'}]}

srvops = {'name':'serviceoperation','data':[{ #'id':1,
'clientid':1,
'officeid':1,
'startdatetime':'2018-12-31 11:00:00.00',
'finishdatetime':'2018-12-31 12:00:00.00',
'serviceid':1,
'totalrevenue':'null',
'cash':'null',
'card':'null',
'discount':'null',
'photoUrl':['www.ingate.ru'],
'userid':3,
'clientrating':9,
'controlrating':9},
{ #'id':2,
'clientid':2,
'officeid':1,
'startdatetime':'2018-12-31 12:00:00.00',
'finishdatetime':'2018-12-31 13:00:00.00',
'serviceid':2,
'totalrevenue':'null',
'cash':'null',
'card':'null',
'discount':'null',
'photoUrls':['www.ingate.ru'],
'userid':4,
'clientrating':10,
'controlrating':10}]
}

gd = {'name':'good','data':[{ #'id':1,
'name':'Шампунь',
'price':500.00,
'status':'active'},
{ #'id':2,
'name':'Кока-кола',
'price':100.00,
'status':'active'}]
}

gdops = {'name':'goodoperation','data':[{ #'id':1,
'clientid':1,
'officeid':1,
'datetime':'2018-12-31 12:00:00.00',
'goodid':1,
'totalrevenue':'null',
'cash':'null',
'card':'null',
'discount':'null',
'userid':3},
{ #'id':2,
'clientid':2,
'office':1,
'datetime':'2018-12-31 13:00:00.00',
'goodid':2,
'totalrevenue':'null',
'cash':'null',
'card':'null',
'discount':'null',
'userid':1}]}

exptp = {'name':'expensetype','data':[{ #'id':1,
'name':'Уборка',
'defaultprice':5000,
'status':'active'},
{ #'id':2,
'name':'Аренда',
'defaultprice':'null',
'status':'active'}]}

exp = {'name':'expenses','data':[{ #'id':1,
'officeid':1,
'datetime':'2018-12-30 09:00:00.00',
'goodid':1,  
'totalspent':5000,
'cash':1000,
'card':4000,
'userid':1},
{ #'id':2,
'officeid':1,
'datetime':'2018-12-30 09:00:00.00',
'goodid':1,  
'totalspent':10000,
'cash':5000,
'card':5000,
'userid':2}]
}

prsnlpmt = {'name':'personnelpayment','data':[{ #'id':1,
'officeid':1,
'datetime':'2018-12-30 09:00:00.00',
'userid':3,
'type':'ndfl',
'totalspent':1000,
'comment':''},
{ #'id':2,
'officeid':1,
'datetime':'2018-12-30 09:00:00.00',
'userid':4,
'type':'penalty',
'totalspent':-300,
'comment':'Сломал ножницы'}]
}

ofc = {'name':'office','data':[{ #'id':1,
'name':'Тула 1',
'city':'Тула',
'address':'г. Тула, ул. Демонстрации, 51',
'coordinatex':0.1,
'coordinatey':0.1,
'status':'open'},
{ #'id':2,
'name':'Воронеж 1',
'city':'Воронеж',
'address':'somewhere',
'coordinatex':0.1,
'coordinatey':0.1,
'status':'open'}]
}

ssn = {'name':'session','data':[{ #'id':1,
'officeid':1,
'opendate':'2018-12-30 09:00:00.00',
'closedate':'2018-12-30 23:00:00.00',
'status':'closed',
'userid':1,
'barbers':[
        {'userid':3,'starttime':'10:00','endtime':'18:00'},
        {'userid':4,'starttime':'14:00','endtime':'22:00'}
        ],
'admins':[
        {'userid':1,'starttime':'09:00','endtime':'23:00'}
        ],
'opencash':20000,
'closecash':30000 ,
'totalincomecash':10000 ,
'totalincomecashless':10000,
'totalincome':20000,
'totalexpense':5000,
'totalprofit':15000    
},
{ #'id':2,
'officeid':1,
'opendate':'2018-12-31 09:00:00.00',
'closedate':'null',
'status':'open',
'userid':1,
'barbers':[
        {'userid':3,'starttime':'10:00','endtime':'18:00'},
        {'userid':4,'starttime':'14:00','endtime':'22:00'}
        ],
'admins':[
        {'userid':1,'starttime':'09:00','endtime':'23:00'}
        ],
'opencash':0,
'closecash':20000,
'totalincomecash':20000 ,
'totalincomecashless':15000,
'totalincome':35000,
'totalexpense':15000,
'totalprofit':20000     
}]
}

tables = [usr,bq,cl,srvc,srvops,gd,gdops,exptp,exp,prsnlpmt,ofc,ssn]


# In[ ]:



for table in tables:
    tablename = table['name']
    columns = (str(tuple(table['data'][0].keys()))).replace('\'','')

    final_string = ''
    for item in table['data']:
        
        for key,value in item.items():
            if type(value) == dict:
                new_value = json.dumps(value)
                item[key] = new_value
            if type(value) == list:
                for i in range(len(value)):
                    if type(value[i]) == dict:
                        value[i] = json.dumps(value[i])
                
        v = (str(tuple(item.values())))
        final_string = final_string+',\n'+v
    values = final_string[2:].replace('\'null\'','null')
    values = values.replace('[','array [')
    values = values.replace('}\']','}\']::json[]')

    q = f"""INSERT INTO {tablename} {columns}
    VALUES
    {values}"""
    
    conn = psycopg2.connect(host="localhost",database="barbers")
    cur = conn.cursor()
    try:
        cur.execute(q)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(q,e, sep = '\n')  


# # CRUD

# ## Update

# In[ ]:


#update
def update(inputparams,host,database,user,password):
    table = inputparams['params']['table']

    baseq = f"""UPDATE {table} 
    SET """
    queryparts = []

    for key,value in inputparams['params']['conditions'].items():
        if key == 'id':
            continue
        else:
            if type(value) == list:
                value = 'array ' + str(value)
            elif type(value) == dict:
                value = json.dumps(value)            
            qpart = f"""{key} = {value}"""
        queryparts.append(qpart)
    setquery = ', '.join(queryparts)

    _id = inputparams['params']['conditions']['id']
    idquery = f'''
    where id = {_id}'''

    q = baseq + setquery + idquery

    conn = psycopg2.connect(host=host,database=database, user=user, password=password)
    cur = conn.cursor()
    try:
        cur.execute(q)
        records = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        print(e, sep = '\n')


# ## Read

# In[ ]:


#read
def read(inputparams,host,database,user,password):
    table = inputparams['params']['table']

    if 'conditions' not in data['params']:
        q = f"""select * from {table}"""
    else:
        baseq = f"""select * from {table} where """
        first_key = [data['params']['conditions'].keys()][0]
        queryparts = []
        for key,value in data['params']['conditions'].items():
            if type(value) == list:
                value = tuple(set(value))
                qpart = f"""{key} in {value}"""
            else:
                qpart = f"""{key} = {value}"""
            queryparts.append(qpart)
        wherequery = ' and '.join(queryparts)
        q = baseq + wherequery

    conn = psycopg2.connect(host=host,database=database, user=user, password=password)
    cur = conn.cursor()
    try:
        cur.execute(q)
        records = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        print(e, sep = '\n')


# ## Create

# In[1]:


def create(inputparams,host,database,user,password):

    table = createparams['params']['table']
    columns = (str(tuple(createparams['params']['conditions'].keys()))).replace('\'','')

    final_string = ''
    for key,value in createparams['params']['conditions'].items():
        if type(value) == dict:
            new_value = json.dumps(value)
            item[key] = new_value
        if type(value) == list:
            for i in range(len(value)):
                if type(value[i]) == dict:
                    value[i] = json.dumps(value[i])

    v = (str(tuple(createparams['params']['conditions'].values())))
    final_string = final_string+',\n'+v
    values = final_string[2:].replace('\'null\'','null')
    values = values.replace('[','array [')
    values = values.replace('}\']','}\']::json[]')

    q = f"""INSERT INTO {table} {columns}
    VALUES
    {values}"""

    conn = psycopg2.connect(host=host,database=database, user=user, password=password)
    cur = conn.cursor()
    try:
        cur.execute(q)
        records = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        print(e, sep = '\n')


# ## Delete

# In[2]:


def delete(delete,host,database,user,password):
    table = delete['params']['table']

    baseq = f"""DELETE FROM {table} 
    SET """
    queryparts = []

    _id = delete['params']['conditions']['id']
    idquery = f'''
    where id = {_id}'''

    q = baseq + idquery

    conn = psycopg2.connect(host=host,database=database, user=user, password=password)
    cur = conn.cursor()
    try:
        cur.execute(q)
        records = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        print(e, sep = '\n')

