
import os
import pandas as pd
import pymysql
from flask import Flask, render_template, jsonify, request, redirect
from sqlalchemy import create_engine, inspect, MetaData, Table
import json

EXT_URL = os.environ.get('EXT_URL')
HOST = os.environ.get('HOST')
USER = os.environ.get('USER')
PASSWORD = os.environ.get('PASSWORD')
DATABASE = os.environ.get('DATABASE')
PORT = os.environ.get('PORT')


app = Flask(__name__)

db_url = f"mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}/{DATABASE}"
engine = create_engine(db_url)
metadata = MetaData(bind=engine)

# route 1
@app.route('/')
def welcome():
    return render_template("index.html")


@app.route('/data')
def covid_data():
    # connect to db
    covid_list = []
    # establish connection
    with engine.connect() as con:
        query_str = """SELECT * FROM covid"""
        res = con.execute(query_str)
        #get table's column names
        covid_table = Table('covid', metadata, autoload_with=engine)
        columns = [c.name for c in covid_table.columns]
        print(columns)
        #loop through the data and store in a list
        for row in res:
            covid_dict = dict(zip(columns, row)) 
            covid_list.append(covid_dict)
    # return json format of the data
    return jsonify(covid_list)


if __name__ == '__main':
    app.run(debug=True)