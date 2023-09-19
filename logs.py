import os
from flask import Flask
from flask import render_template, request, redirect, session
from flaskext.mysql import MySQL
from datetime import datetime, timedelta
from flask import send_from_directory
from tkinter import *
from tkinter import messagebox
from django import template
from django.db import models
from db import *

def logs1(variable1):

    if not 'login' in session:
        return redirect("/login")
    
    sql = "insert into logueo (fecha, sitio, usuario) values (now(),  %s, %s );"
    datos= (variable1, session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit() 