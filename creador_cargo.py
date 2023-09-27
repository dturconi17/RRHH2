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

@app.route('/cargos')
def cargos():

    logs.logs1('Creador de Cargo')

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("""Select id, cargo_general, cargo_sub, 
                   CONCAT(DAY(fecha), '/',MONTH(fecha), '/',YEAR(fecha)), 
                   (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = creador)
                   from cargos""")
    rep_cargos=cursor.fetchall()
    conexion.commit
   
    return render_template("/admin/cargos.html", rep_cargos=rep_cargos)

@app.route('/admin/cargo/guardar', methods=['POST'])
def admin_cargos_guardar():

    logs.logs1('Guardar Cargo')

    _cargo = request.form['Cargo']
    _subcargo = request.form['Subcargo']
    

    tiempo = datetime.now()
    
    sql = "INSERT INTO `cargos` (cargo_general, cargo_sub, creador, fecha) VALUES (%s, %s, %s, %s);"
    datos=(_cargo, _subcargo, session["usuario"], tiempo, )
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()

    return redirect('/cargos')

@app.route('/admin/cargo/guardar_editar', methods=['POST'])
def admin_cargos_guardar_editar():

    logs.logs1('Guardar Editar Cargo')

    _id = request.form['txtId']

    _cargo = request.form['Cargo']
    _subcargo = request.form['Subcargo']

    tiempo = datetime.now()
    
    sql = "update `cargos` set cargo_general = %s, cargo_sub = %s, creador = %s, fecha = %s where id = %s;"
    datos=(_cargo, _subcargo, session["usuario"], tiempo, _id)
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()

    return redirect('/cargos')

@app.route('/admin/cargo/borrar', methods=['POST'])
def admin_cargo_borrar():
    
    logs.logs1('Borrar Cargo')
 
    _id = request.form['txtId']

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("delete from cargos WHERE id=%s", (_id))
    libros=cursor.fetchall()
    conexion.commit()
    return redirect('/cargos')

@app.route('/admin/cargo/editar', methods=['POST'])
def admin_cargo_editar():

    logs.logs1('Editar Cargo')

    _id = request.form['txtId']

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("""Select id, cargo_general, cargo_sub, 
                   CONCAT(DAY(fecha), '/',MONTH(fecha), '/',YEAR(fecha)), 
                   (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = creador)
                   from cargos where id = %s;""", (_id))
    rep_cargos=cursor.fetchall()
    conexion.commit
   
    return render_template("/admin/cargo_editar.html", rep_cargos=rep_cargos)