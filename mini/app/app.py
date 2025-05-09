from lib2to3.pgen2.driver import Driver
from operator import ge
from tkinter import Y
# from django.shortcuts import render
from flask import Flask, render_template, request, redirect, flash
import numpy as np
import pandas as pd
from joblib import dump, load
import sklearn
import json
# import openpyxl
from pandas import DataFrame

import pypyodbc as odbc

DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = 'DESKTOP-T4TPA2L\SQLEXPRESS'
DATABASE_NAME = 'GP'
connection = f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={{{SERVER_NAME}}};
    DATABASE={{{DATABASE_NAME}}};
    Trust_Connection=yes;
"""

app = Flask(__name__)

@app.route('/bar-chart',methods=['GET'])
def barchart():
    return render_template("barchart.html");

@app.route('/pie-chart',methods=['GET'])
def piechart():
    return render_template("piechart.html");

@app.route('/histogram',methods=['GET'])
def histogram():
    return render_template("histogram.html");


@app.route('/visualize-top-x-crimes', methods=['GET'])
def visualizetopxcrimes():
    return render_template("India Map - Districts TopXCrime.html");

@app.route('/visualize', methods=['GET'])
def visualize():
    return render_template("India Map - Districts.html");


@app.route('/visualize-combination', methods=['GET', 'POST'])
def hello_world():
    record = ""
    request_type_str = request.method
    if request_type_str == 'GET':
        return render_template('map.html', data=record)
    else:
        arr = request.form.get('arr').split(',')
        print(arr)
        print(len(arr))
        conn = odbc.connect(connection)
        cursor = conn.cursor()
        if (len(arr) == 2):
            print('in')
            print(arr[1])
            sql_select_query = "select District_name from alldisc4 where " + arr[0] + "= ?"
            cursor.execute(sql_select_query, (arr[1],))
            records = str(cursor.fetchall()).replace('(', '').replace('),', '').replace(',)', '').replace('\'','').replace('[', '').replace(']', '')
        elif (len(arr) == 4):
            print('in')
            print(arr[1])
            sql_select_query = "select District_name from alldisc4 where " + arr[0] + "= ? and " + arr[2] + "= ?"
            cursor.execute(sql_select_query, (arr[1], arr[3],))
            records = str(cursor.fetchall()).replace('(', '').replace('),', '').replace(',)', '').replace('\'','').replace('[', '').replace(']', '')
            print(records)
        elif (len(arr) == 6):
            print('in')
            print(arr[1])
            sql_select_query = "select District_name from alldisc4 where " + arr[0] + "= ? and " + arr[2] + "= ? and " + \
                               arr[4] + "= ?"
            cursor.execute(sql_select_query, (arr[1], arr[3], arr[5],))
            records = str(cursor.fetchall()).replace('(', '').replace('),', '').replace(',)', '').replace('\'','').replace('[', '').replace(']', '')
            print(records)

        return render_template('map.html', data=records)


@app.route('/home')
def view():
    return render_template('view.html')


@app.route('/about')
def about():
    return render_template('about.html')


#login
@app.route('/', methods = ["GET", "POST"])
def login():
    request_type_str = request.method
    if request_type_str == 'GET':
        return render_template('login.html')
    else:
        arr = str(request.form.get('user_data')).split(',')
        conn = odbc.connect(connection)
        cursor = conn.cursor()
        sql_select_query = "select * from Users where username= ? AND password= ?"
        cursor.execute(sql_select_query, (arr[0],arr[1]))

        records = str(cursor.fetchall()).replace('(', '').replace('),', '').replace(',)', '').replace('\'','').replace('[', '').replace(']', '')
        if records == "":
            return redirect('/')

        return redirect('/home')
    
#register
@app.route('/register')
def register():
    request_type_str = request.method
    if request_type_str == 'GET':
        return render_template('register.html')
    else:
        arr = str(request.form.get('user_data')).split(',')
        conn = odbc.connect(connection)
        cursor = conn.cursor()
        sql_select_query = "select * from Users where username= ? AND password= ?"
        cursor.execute(sql_select_query, (arr[0], arr[1]))

        records = str(cursor.fetchall()).replace('(', '').replace('),', '').replace(',)', '').replace('\'', '').replace(
            '[', '').replace(']', '')
        if records != "":
            return redirect('/register')

        else:
            sql_insert_query = "insert into Users(username,password) values(?,?)"
            cursor.execute(sql_insert_query, (arr[0], arr[1]))
            conn.commit()

        return redirect('/')

#text search
@app.route('/preview')
def get_rows():
    return render_template('search.html')


@app.route('/predict', methods = ['GET', 'POST'])
def predict2():

    request_type_str = request.method
    if request_type_str == 'GET':
        return render_template('predict.html', data = "")
    else:

        datatst = pd.read_csv("test.csv")
        datatst = datatst.drop('Crime',1)

        column_names = datatst.columns
        print("post rquest")
        arr = str(request.form.get('test')).split(',')
        print(str(arr[2]))
        my_array = np.array([arr])
        datatst = pd.DataFrame(my_array, columns = column_names)

        datatst = datatst.drop('State_name',1)
        datatst = datatst.drop('District_name',1)

        X_test = datatst[[x for x in datatst.columns if x != 'Crime4']].values
        Y_test = datatst['Crime4'].values

        clf = load('model.joblib')

        y_pred = clf.predict(X_test)
        val = str(y_pred)
        val = val.replace(',', '').replace('[', '').replace(']', '').replace('\'', '')

        return render_template("predict.html", data = val)
        return str(y_pred)

