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
import logs

@app.route('/reglas_vacaciones')
def reglas_vacaciones():

    logs.logs1('Listar Reglas Vacaciones')

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("""Select id, desde, hasta, dias, 
                   (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = creado_por), 
                   CONCAT(DAY(fecha), '/',MONTH(fecha), '/',YEAR(fecha))
                   from reglas_vacaciones order by desde asc""")
    reglas=cursor.fetchall()
    conexion.commit

    return render_template("/admin/regla_vacaciones.html", reglas = reglas)

@app.route('/admin/reglas_vacaciones/guardar', methods=['POST'])
def reglas_vacaciones_guardar():

    logs.logs1('Guardar Reglas Vacaciones')

    _desde = request.form['desde']
    _hasta = request.form['hasta']
    _dias = request.form['dias']
    
    tiempo = datetime.now()
    
    sql = "INSERT INTO reglas_vacaciones (desde, hasta, dias, creado_por, fecha) VALUES (%s, %s, %s, %s, %s);"
    datos=(_desde, _hasta, _dias, session["usuario"], tiempo)
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()

    return redirect('/reglas_vacaciones')

@app.route('/admin/reglas_vacaciones/borrar', methods=['POST'])
def reglas_vacaciones_borrar():
    
    logs.logs1('Borrar Reglas Vacaciones')

    _id = request.form['txtId']

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("delete from reglas_vacaciones WHERE id=%s", (_id))
    libros=cursor.fetchall()
    conexion.commit()
    return redirect('/reglas_vacaciones')

@app.route('/admin/reglas_vacaciones/editar', methods=['POST'])
def admin_reglas_vacaciones_editar():

    logs.logs1('Editar Reglas Vacaciones')

    _id = request.form['txtId']

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("""Select id, desde, hasta, dias, 
                   CONCAT(DAY(fecha), '/',MONTH(fecha), '/',YEAR(fecha)), 
                   (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = creado_por)
                   from reglas_vacaciones where id = %s;""", (_id))
    reglas=cursor.fetchall()
    conexion.commit
   
    return render_template("/admin/regla_vacaciones_editar.html", reglas=reglas)

@app.route('/admin/reglas_vacaciones/guardar_editar', methods=['POST'])
def admin_reglas_vacaciones_guardar_editar():

    logs.logs1('Guardar Editar Reglas Vacaciones')

    _id = request.form['txtId']
    _desde = request.form['desde']
    _hasta = request.form['hasta']
    _dias = request.form['dias']
    
    tiempo = datetime.now()
    
    sql = "update reglas_vacaciones set desde = %s, hasta = %s, dias = %s, creado_por = %s, fecha = %s where id = %s;"
    datos=(_desde, _hasta, _dias, session["usuario"], tiempo, _id)
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()

    return redirect('/reglas_vacaciones')