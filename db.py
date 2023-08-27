from flaskext.mysql import MySQL
from flask import Flask
from flask import render_template, request, redirect, session

app=Flask(__name__)
app.secret_key="develoteca"
mysql=MySQL()

app.config['MYSQL_DATABASE_HOST']='127.0.0.1'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']='Santi1703#'
app.config['MYSQL_DATABASE_DB']='sitio'
mysql.init_app(app)