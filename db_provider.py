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
"servicePercent" FLOAT(2),    
"goodsPercent" FLOAT(2) NOT NULL,
"categoryId" INT,
state TEXT NOT NULL,
"clientRating" FLOAT(2),
"controlRating" FLOAT(2),
login TEXT,
password TEXT,
contacts JSONB []);

CREATE TABLE SERVICEOPERATION(
id SERIAL PRIMARY KEY NOT NULL,
"officeId" INT,
"sessionId" INT,
"serviceId" INT NOT NULL,
"startDatetime" TIMESTAMP NOT NULL,
"finishDatetime" TIMESTAMP NOT NULL,
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
"controlRating" FLOAT(2));


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
"cashlessSum" INT,
"comment" TEXT);

CREATE TABLE EMPLOYEEPAYMENT(
id SERIAL PRIMARY KEY NOT NULL,
"officeId" INT,
"sessionId" INT,
"employeeId" INT NOT NULL,
"datetime" TIMESTAMP NOT NULL,
type TEXT NOT NULL,
sum FLOAT(2),
"cashSum" FLOAT(2),
"cashlessSum" INT,
"comment" TEXT);

CREATE TABLE SESSION(
id SERIAL PRIMARY KEY NOT NULL,
"officeId" INT,
"dateOpened" TIMESTAMP NOT NULL,
"dateClosed" TIMESTAMP,
state TEXT NOT NULL,
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
prices JSONB NOT NULL,
state TEXT NOT NULL);

CREATE ROLE read_only WITH LOGIN PASSWORD 'User_ro';
GRANT SELECT on ALL tables in schema public to read_only;

CREATE ROLE read_write WITH LOGIN PASSWORD 'Rw_Us3r';
GRANT SELECT,INSERT on ALL tables in schema public to read_write;

CREATE ROLE admin WITH LOGIN PASSWORD 'Adm1n1strat0r';
GRANT ALL PRIVILEGES ON DATABASE barbers to admin;


# # Наполнение таблиц

# In[ ]:


ofc = {'name':'office','data':[{ #'Id':1,
'name':'Тула 1',
'city':'Тула',
'address':'г. Тула, ул. Демонстрации, 51',
'coordinatex':0.1,
'coordinatey':0.1,
'state':'open'},
{ #'Id':2,
'name':'Воронеж 1',
'city':'Воронеж',
'address':'somewhere',
'coordinatex':0.2,
'coordinatey':0.2,
'state':'open'}]
}

bq = {'name':'barbercategory','data':[{ #'Id':1,
'name':'Старший мастер',
'servicePercent': 0.5,
'state':'active'},
{ #'Id':2,
'name':'Младший мастер',
'servicePercent': 0.2,
'state':'active'}]}

gd = {'name':'good','data':[{ #'Id':1,
'name':'Шампунь',
'price':500.00,
'state':'active'},
{ #'Id':2,
'name':'Кока-кола',
'price':100.00,
'state':'active'}]
}

exptp = {'name':'spendtype','data':[{ #'Id':1,
'name':'Уборка',
'defaultPrice':5000,
'state':'active'},
{ #'Id':2,
'name':'Аренда',
'defaultPrice':'null',
'state':'active'}]}

cl = {'name':'client','data':[{ #Id:1,
    'name':'Клиентов Клиент Клиентович',
    'contacts':[{
        'phone':'+79996669966',
        'mail':'mail@mail.com',
        'vk':'vk.com'
                }]
   },
    { #Id:2,
    'name':'Клиентов Клиент Клиентович',
    'contacts':[{
        'phone':'+79009009090',
        'mail':'mail2@mail.com',
        'vk':'vk2.com'
                }]
   }]
}

usr = {'name':'_user','data':[{ # Id:1,
'name':'Иванов Диего Михайлович',
'pictureUrl':'www.mysite.com',
'roles':['officeAdmin'],
'salary':100000,
'servicePercent':0.1,
'goodsPercent':0.1,
'categoryId':'null',
'state':'working',
'clientRating':'null',
'controlRating':'null',
'login':'login',
'password':'password'},
{ # Id:2,
'name':'Парикмахеров Парикмахер Парикмахерович',
'pictureUrl':'www.wikipedia.org',
'roles':['manager'],
'salary':200000,
'servicePercent':0.1,
'goodsPercent':0.1,
'categoryId':'null',
'state':'working',
'clientRating':'null',
'controlRating':'null',
'login':'login2',
'password':'password2'},
{ # Id:3,
'name':'Морковная Залупа Павловна',
'pictureUrl':'www.vk.com',
'roles':['master'],
'salary':50000,
'servicePercent':0.1,
'goodsPercent':0.1,
'categoryId':1,
'state':'working',
'clientRating':10,
'controlRating':10,
'login':'login3',
'password':'password3'},
{ # Id:4,
'name':'Барберов Бородач Ножницевич',
'pictureUrl':'www.ingate.ru',
'roles':['master'],
'salary':50000,
'servicePercent':0.1,
'goodsPercent':0.1,
'categoryId':2,
'state':'working',
'clientRating':10,
'controlRating':10,
'login':'login3',
'password':'password3'}]
}

srvops = {'name':'serviceoperation','data':[{ #'Id':1,
    'officeId':1,
    'sessionId':1,
    'serviceId':1,
    'startDatetime':'2018-12-31 11:00:00.00',
    'finishDatetime':'2018-12-31 12:00:00.00',    
    'adminId':1,    
    'masterId':4,    
    'clientId':1,
    'photoUrls':['www.ingate.ru'],
    'clientRating':'null',
    'controlRating':'null'},
{ #'Id':2,
    'officeId':1,
    'sessionId':1,
    'serviceId':2,    
    'startDatetime':'2018-12-31 12:00:00.00',
    'finishDatetime':'2018-12-31 13:00:00.00',
    'adminId':1,    
    'masterId':3,    
    'clientId':2,
    'photoUrls':['www.ingate.ru'],
    'clientRating':10,
    'controlRating':10}]
}

gdops = {'name':'goodsoperation','data':[{ #'Id':1,
    'clientId':1,
    'officeId':1,
    'sessionId':1,
    'adminId':1,    
    'masterId':4,
    'datetime':'2018-12-31 12:00:00.00',
    'goodsIds':[1]
},
{ #'Id':2,
    'clientId':1,
    'officeId':1,
    'sessionId':1,
    'adminId':1,    
    'masterId':4,
    'datetime':'2018-12-31 13:00:00.00',
    'goodsIds':[1]
}]}

exp = {'name':'spendoperations','data':[{ #'Id':1,
    'officeId':1,
    'sessionId':1,
    'datetime':'2018-12-30 09:00:00.00',
    'expenseTypeId':1,  
    'sum':5000,
    'cashSum':1000,
    'cashlessSum':4000
},
{ #'Id':2,
    'officeId':1,
    'sessionId':1,
    'datetime':'2018-12-30 09:00:00.00',
    'expenseTypeId':1,  
    'sum':10000,
    'cashSum':5000,
    'cashlessSum':5000
}]}

prsnlpmt = {'name':'employeepayment','data':[{ #'Id':1,
    'officeId':1,
    'datetime':'2018-12-30 09:00:00.00',
    'sessionId':1,
    'employeeId':3,
    'type':'ndfl',
    'sum':1000,
    'comment':'null'
},
{ #'Id':2,
    'officeId':1,
    'datetime':'2018-12-30 09:00:00.00',
    'sessionId':1,
    'employeeId':4,
    'type':'penalty',
    'sum':-300,
    'comment':'Сломал ножницы'
}]}


srvc = {'name':'service','data':[{ #'Id':1,
'name':'Стрижка мужская',
'prices': {1:500.00,2:600.00,3:700.00,4:800.00},
'state':'active'},
{ #'Id':2,
'name':'Стрижка женская',
'prices':{1:1000.00,2:1100.00,3:1200.00,4:1300.00},
'state':'active'}]}

ssn = {'name':'session','data':[{ #'Id':1,
'officeId':1,
'dateOpened':'2018-12-30 09:00:00.00',
'dateClosed':'2018-12-30 23:00:00.00',
'state':'closed',
'employees':[
        {'userId':3,'starttime':'10:00','endtime':'18:00'},
        {'userId':4,'starttime':'14:00','endtime':'22:00'},
        {'userId':1,'starttime':'09:00','endtime':'23:00'}
        ],
'openCash':20000,
'closeCash':30000 ,
'totalIncomeCash':10000 ,
'totalIncomeCashless':10000,
'totalIncome':20000,
'totalExpense':5000,
'totalProfit':15000    
},
{ #'Id':2,
'officeId':1,
'dateOpened':'2018-12-31 09:00:00.00',
'dateClosed':'null',
'state':'open',
'employees':[
        {'userId':3,'starttime':'10:00','endtime':'18:00'},
        {'userId':4,'starttime':'14:00','endtime':'22:00'},
        {'userId':1,'starttime':'09:00','endtime':'23:00'}
        ],
'opencash':0,
'closeCash':'null',
'totalIncomeCash':'null' ,
'totalIncomeCashless':'null',
'totalIncome':'null',
'totalExpense':'null',
'totalProfit':'null'  
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

