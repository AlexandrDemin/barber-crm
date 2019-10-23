#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import psycopg2
import traceback

createdatabase = "CREATE DATABASE BARBERS;"
conn = psycopg2.connect(host='localhost',database='postgres', user='postgres', password='postgres')
conn.autocommit = True
cur = conn.cursor()
try:
    cur.execute(createdatabase)
    cur.close()
    conn.close()
    print('success')
        
except Exception as e:
        stacktrace = traceback.format_exc()
        print('error',e,'stacktrace',stacktrace)
        
tables_and_roles = """
CREATE TABLE EMPLOYEE(
id SERIAL PRIMARY KEY NOT NULL,
name TEXT NOT NULL,
"photo" JSONB,
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

CREATE TABLE BARBERCATEGORY(
id SERIAL PRIMARY KEY NOT NULL,
"name" TEXT NOT NULL,
"servicePercent" FLOAT(2) NOT NULL,
"state" TEXT NOT NULL);

CREATE TABLE OFFICE(
id SERIAL PRIMARY KEY NOT NULL,
name TEXT NOT NULL,
city TEXT NOT NULL,
address TEXT NOT NULL,
coordinatex FLOAT NOT NULL,
coordinatey FLOAT NOT NULL,
state TEXT NOT NULL);

CREATE TABLE SESSION(
id SERIAL PRIMARY KEY NOT NULL,
"officeId" INT NOT NULL,
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
prices JSONB [] NOT NULL,
state TEXT NOT NULL);

CREATE TABLE SERVICEOPERATION(
id SERIAL PRIMARY KEY NOT NULL,
"officeId" INT NOT NULL,
"sessionId" INT NOT NULL,
"serviceId" INT NOT NULL,
"startDatetime" TIMESTAMP NOT NULL,
"finishDatetime" TIMESTAMP NOT NULL,
"adminId" INT NOT NULL,
"masterId" INT NOT NULL,    
"clientId" INT,
"cashSum" FLOAT(2),
"cashlessSum" FLOAT(2),
"discountSum" FLOAT(2),
"adminBonusSum" FLOAT(2),
"masterBonusSum" FLOAT(2),
"totalRevenue" FLOAT(2),
"clientRating" FLOAT(2),
"review" TEXT, 
"photos" JSONB [],
"comment" TEXT, 
"controlRating" FLOAT(2));

CREATE TABLE GOOD(
id SERIAL PRIMARY KEY NOT NULL,
name TEXT NOT NULL,
price FLOAT(2) NOT NULL,
state TEXT NOT NULL);

CREATE TABLE GOODSOPERATION(
id SERIAL PRIMARY KEY NOT NULL,
"officeId" INT NOT NULL,
"sessionId" INT NOT NULL,
"goodsIds" INT [] NOT NULL,
"datetime" TIMESTAMP NOT NULL,    
"adminId" INT NOT NULL,
"masterId" INT NOT NULL,    
"clientId" INT,
"cashSum" FLOAT(2),
"cashlessSum" FLOAT(2),
"discountSum" FLOAT(2),
"adminBonusSum" FLOAT(2),
"masterBonusSum" FLOAT(2),
"totalRevenue" FLOAT(2),
"comment" TEXT);

CREATE TABLE SPENDTYPE(
id SERIAL PRIMARY KEY NOT NULL,
name TEXT NOT NULL,
"defaultSum" FLOAT(2),
state TEXT NOT NULL);

CREATE TABLE SPENDOPERATION(
id SERIAL PRIMARY KEY NOT NULL,
"officeId" INT NOT NULL,
"sessionId" INT NOT NULL,
"expenseTypeId" INT NOT NULL,
datetime TIMESTAMP NOT NULL,
sum FLOAT(2),
"cashSum" FLOAT(2),
"cashlessSum" INT,
"comment" TEXT);

CREATE TABLE EMPLOYEEPAYMENTTYPE(
id SERIAL PRIMARY KEY NOT NULL,
name TEXT NOT NULL,
"defaultSum" FLOAT(2),
state TEXT NOT NULL);

CREATE TABLE EMPLOYEEPAYMENT(
id SERIAL PRIMARY KEY NOT NULL,
"officeId" INT NOT NULL,
"sessionId" INT NOT NULL,
"employeeId" INT NOT NULL,
"datetime" TIMESTAMP NOT NULL,
"employeePaymentTypeId" INT NOT NULL,
sum FLOAT(2),
"cashSum" FLOAT(2),
"cashlessSum" INT,
"comment" TEXT);

CREATE TABLE CLIENT(
id SERIAL PRIMARY KEY NOT NULL,
name TEXT NOT NULL,
contacts JSONB [],
"photo" JSONB,
comment TEXT);

CREATE ROLE read_only WITH LOGIN PASSWORD 'User_ro';
GRANT SELECT on ALL tables in schema public to read_only;
GRANT CONNECT ON DATABASE barbers to read_only;
GRANT USAGE ON SCHEMA public  to read_only;

CREATE ROLE read_write WITH LOGIN PASSWORD 'Rw_Us3r';
GRANT SELECT,INSERT,UPDATE on ALL tables in schema public to read_write;
GRANT USAGE ON SCHEMA public  to read_write;
GRANT CONNECT ON DATABASE barbers to read_write;

CREATE ROLE admin WITH LOGIN PASSWORD 'Adm1n1strat0r';

ALTER DEFAULT PRIVILEGES in schema public
GRANT SELECT ON TABLES to read_only;
ALTER DEFAULT PRIVILEGES
GRANT USAGE ON SCHEMAS to read_only;
ALTER DEFAULT PRIVILEGES in schema public
GRANT SELECT,INSERT ON TABLES to read_write;
ALTER DEFAULT PRIVILEGES
GRANT USAGE ON SCHEMAS to read_write;
ALTER DEFAULT PRIVILEGES in schema public
GRANT ALL PRIVILEGES ON TABLES to admin;
ALTER DEFAULT PRIVILEGES
GRANT ALL PRIVILEGES ON SCHEMAS to admin;
ALTER DEFAULT PRIVILEGES in schema public
GRANT ALL PRIVILEGES ON FUNCTIONS to admin;
"""

conn = psycopg2.connect(host='localhost',database='barbers', user='postgres', password='postgres')
con.autocommit = True
cur = conn.cursor()
try:
    cur.execute(tables_and_roles)
    cur.close()
    conn.close()
    print('Success')
        
except Exception as e:
    stacktrace = traceback.format_exc()
    print('error',e,'stacktrace',stacktrace)

