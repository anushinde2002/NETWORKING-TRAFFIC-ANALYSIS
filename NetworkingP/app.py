from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

from distutils.log import debug
from fileinput import filename
from datetime import datetime
from flask import *
import pandas as pd
import numpy as np
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
# # Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = '0123456789'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'anushinde@123'
app.config['MYSQL_DB'] = 'nasmas'
 
# Intialize MySQL
mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))

        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('index.html', msg=msg)


@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()

        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'        
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)


@app.route('/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))
    
    
@app.route('/profile')
def profile():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        return render_template('profile.html', account=account, username=session['username'])
    return redirect(url_for('login'))



@app.route('/sip_bytes')
def sip_bytes():
    if 'loggedin' in session:
       df = pd.read_csv('csv/sip_bytes.csv', low_memory=False)
       df = df.head(50)
       data = df.data.to_list()
       percentage = df.percentage.to_list()
       return render_template('sip_bytes_pareto.html',username=session['username'], data=data, percentage=percentage)
    return redirect(url_for('login'))

@app.route('/sip_connections')
def sip_connections():
    if 'loggedin' in session:
       df = pd.read_csv('csv/sip_connections.csv',low_memory=False)
       df = df.head(50)
       data = df.data.to_list()
       percentage = df.percentage.to_list()
       return render_template('sip_connections_pareto.html',username=session['username'], data=data, percentage=percentage)
    return redirect(url_for('login'))

@app.route('/sip_durations')
def sip_durations():
  if 'loggedin' in session:
      df = pd.read_csv('csv/sip_durations.csv',low_memory=False)
      df = df.head(50)
      data = df.data.to_list()
      percentage = df.percentage.to_list()
      return render_template('sip_durations_pareto.html',username=session['username'], data=data, percentage=percentage)
  return redirect(url_for('login'))

@app.route('/top_sips')
def top_sips():
    if 'loggedin' in session:
         return render_template('top_source_ips.html',username=session['username'])
    return redirect(url_for('login'))


@app.route('/dip_bytes')
def dip_bytes():
    if 'loggedin' in session: 
      df = pd.read_csv('csv/dip_bytes.csv', low_memory=False)
      df = df.head(50)
      data = df.data.to_list()
      percentage = df.percentage.to_list()
      return render_template('dip_bytes_pareto.html',username=session['username'], data=data, percentage=percentage)
    return redirect(url_for('login'))

@app.route('/dip_connections')
def dip_connections():
    if 'loggedin' in session:
      df = pd.read_csv('csv/dip_connections.csv', low_memory=False)
      df = df.head(50)
      data = df.data.to_list()
      percentage = df.percentage.to_list()
      return render_template('dip_connections_pareto.html',username=session['username'], data=data, percentage=percentage)
    return redirect(url_for('login'))

@app.route('/dip_durations')
def dip_durations():
    if 'loggedin' in session:
      df = pd.read_csv('csv/dip_durations.csv', low_memory=False)
      df = df.head(50)
      data = df.data.to_list()
      percentage = df.percentage.to_list()
      return render_template('dip_durations_pareto.html',username=session['username'], data=data, percentage=percentage)
    return redirect(url_for('login'))

@app.route('/top_dips')
def top_dips():
    if 'loggedin' in session:
         return render_template('top_destination_ips.html',username=session['username'])
    return redirect(url_for('login'))

@app.route('/traffic')
def traffic():
   if 'loggedin' in session:
       df = pd.read_csv('csv/cleaned_loged.csv', low_memory=False)
       hourly_table = pd.pivot_table(data=df,index=['hour'],values=['byte'],aggfunc={len,np.sum})
       hourly_table.to_csv("csv/hourly_conn_bytes.csv")
       hourly_conn_bytes = pd.read_csv("csv/hourly_conn_bytes.csv",skiprows=3,sep=',',names=['hour','connection','bytes'])
       hourly_conn_bytes.to_csv("csv/hourly_conn_bytes.csv",index=False)
       
       hours=hourly_conn_bytes.hour.to_list()
       connection=hourly_conn_bytes.connection.to_list()
       bytes=hourly_conn_bytes.bytes.to_list()
       duration=hourly_conn_bytes.connection.to_list()
       return render_template('traffic_conn_byte.html', hours=hours, connection=connection, bytes=bytes, duration=duration)
   return redirect(url_for('login'))

@app.route('/key_network_events')
def key_network_events():
    df = pd.read_csv('csv/cleaned_loged.csv', low_memory=False)
    df = df.head(50)
    events_list = ['src_ip', 'dst_ip', 'src_port', 'dst_port']
    result_dict = {}
    for hour in df.hour.unique():
       hour_dict = {}
       for event in events_list:
        df2 = df[df['hour'] == hour]
        event_bytes = df2.groupby(event).byte.sum().reset_index()
        max_bytes = event_bytes['byte'].max()
        max_event = event_bytes[event_bytes['byte'] == max_bytes][event].values[0]
        hour_dict[event] = max_event
        result_dict[hour] = hour_dict

        result_df = pd.DataFrame(result_dict).T  
        result_df.to_csv('csv/top_events_of_the_day.csv')
        # result_df=pd.read_csv('csv/top_events_of_the_day.csv',skiprows=1,sep=',',names=['hour', 'src_ip', 'dst_ip', 'src_port', 'dst_port'])
        result_df.to_csv('csv/top_events_of_the_day.csv',index=False, header=True)
        #header=True(to write the column names to the file.)
          
    return render_template('key_network_events_of_the_day.html')           
        
        
 
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")
    
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html")

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0",port=5001)