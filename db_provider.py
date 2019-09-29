#!/usr/bin/env python
# coding: utf-8


import json
import psycopg2

# функция для подготовки данных для вставки в sql-запрос
def prepareData(data):
    for key,value in data.items():
        if type(value) == dict:
            data[key] = json.dumps(value) # перегоняем словарь в json
        elif type(value) == list:
            for i in range(len(value)):
                if type(value[i]) == dict:
                    value[i] = str(json.dumps(value[i])) # если внутри списков есть словари, их тоже в json
            data[key] = str(value) # список в виде корректного string
        elif type(value) == str: # чтобы отделить string и числа
            data[key] = '\''+str(value)+'\''
        else:
            data[key] = str(value)
    return data

# генерация запроса на апдейт данных
def generateQueryUpdate(table,data):
    _id = data['id']
    del data['id'] # дальше ID не понадобится, а если оставить, то будет мешаться
    # генерируем начало запроса с названием таблицы на апдейт
    baseq = f"""UPDATE {table} 
    SET """
        
    queryparts = []
    prepareData(data) # инициируем подготовку данных, чтобы их можно было вставлять в sql запрос и он потом работал
    for key,value in data.items(): # если бы мы здесь оставили бы ID, то ID бы попал в текст запроса на изменение
        qpart = f"""{key} = {value}""" # это формат апдейта данных, слева колонка, справа новое значение
        queryparts.append(qpart)
    setquery = ', '.join(queryparts)
    setquery = setquery.replace('\'null\'','null') # null без кавычек
    setquery = setquery.replace('[','array [') # массивы в нужном формате
    setquery = setquery.replace('}\']','}\']::json[]') # json в нужном формате
    
    idquery = f"""
    where id = {_id}""" # обновляем только для данного ID
    q = baseq + setquery + idquery + '\nRETURNING id' # Собираем итоговый запрос, Returning нужен для того, чтобы потом получить ID обновленных объектов
    return q

# генерируем запрос на создание новых записей
def generateQueryCreate(table,data):
    columns = '(\"' + "\",\"".join(list(data.keys() )) + '\")' # все колонки оборачиваем в двойные кавычки, потому что они не регистронезависимые
    prepareData(data) # подготавливаем данные для вставки в sql-запрос
    v = '(' + ",".join((list(data.values()))) + ')' # генерируем часть запроса с values
    
    values = v.replace('\'null\'','null') # null без кавычек
    values = values.replace('[','array [') # массивы в нужном формате
    values = values.replace('}\']','}\']::json[]') # json в нужном формате
    
    # Собираем итоговый запрос, Returning нужен для того, чтобы потом получить ID созданных объектов
    q = f"""INSERT INTO {table} {columns}
    VALUES
    {values} RETURNING id""" 
    return q

# генерация части запроса, которая идет после where на основе входных параметров
def generateWhere(data):
    baseq = f"""
    where """
    wherepartslist = []
    for key,value in data.items():
        wherepart = f"""{key} = {value}"""
        wherepartslist.append(whereclause)
    wherestring = ' and '.join(wherepartslist) # соединение всех кусков в один через and
    whereclause = baseq + wherestring # формирование итогового куска
    return whereclause

# создание запроса на select
def generateQueryRead(*args):
    table = args['table']
    orderpart = '' # по дефолту часть order by отсутствует
    wherepart = '' # по дефолту часть where отсутствует
    fields = '*' # по дефолту в запросе будут выбраны все поля
    
    # далее в зависимости от полей и значений во входных аргументах формируется разный select
    if 'fields' in args: # выбор полей, если надо получить не все
        fields = ','.join(args['fields'])
    
    # ветка формирования селектов со сложной логикой
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
    # стандартная ветка, где нужно просто сформировать where на основе входящих параметров        
    else:    
        if 'data' in args:
            wherepart = generateWhere(args['data'])            
            
    query = f"""select {fields} from {table}{wherepart}{orderpart}""" #собрали итоговый запрос
    

# функция для отправки запроса в базу.
def gotobase(host,database,user,password,query,commit=False): # Если commit=True, то в базу вносятся изменения. Нужно для апсерта.
    conn = psycopg2.connect(host=host,database=database,user=user,password=password)
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute(query)
        if commit == True: # вносим изменение в базу
            conn.commit()
        result_data = cur.fetchall()
        cur.close()
        conn.close()
        if len(result_data) == 0: # если ничего не пришло
            if commit == False:
                return {'error':'Нет таких данных'}
            else:
                return {'error':'Не удалось добавить данные'}
        else:
            return result_data
    except Exception as e:
        return {'error':e}
