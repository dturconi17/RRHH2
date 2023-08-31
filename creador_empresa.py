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

@app.route('/empresa')
def empresa():

    logs.logs1('Creador de Empresa')

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("""Select id, empresa, 
                   CONCAT(DAY(fecha), '/',MONTH(fecha), '/',YEAR(fecha)), 
                   (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = creado_por),
                   cuit,
                   domicilio
                   from empresas""")
    empresas=cursor.fetchall()
    conexion.commit
   
    return render_template("/admin/empresas.html", empresas=empresas)

@app.route('/admin/empresa/guardar', methods=['POST'])
def admin_empresas_guardar():

    logs.logs1('Guardar Empresa')

    _empresa = request.form['txtEmpresa']
    _domicilio = request.form['txtDomicilio']
    _cuit = request.form['txtCuit']

    tiempo = datetime.now()
    
    sql = "INSERT INTO `empresas` (empresa, creado_por, fecha, domicilio, cuit) VALUES (%s, %s, %s, %s, %s);"
    datos=(_empresa, session["usuario"], tiempo, _domicilio, _cuit)
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()

    return redirect('/empresa')

@app.route('/admin/empresa/guardar_editar', methods=['POST'])
def admin_empresas_guardar_editar():

    logs.logs1('Guardar Editar Empresa')

    _id = request.form['txtId']
    _empresa = request.form['txtEmpresa']
    _domicilio = request.form['txtDomicilio']
    _cuit = request.form['txtCuit']

    tiempo = datetime.now()
    
    sql = "update `empresas` set empresa = %s, creado_por = %s, fecha = %s, domicilio = %s, cuit = %s where id = %s;"
    datos=(_empresa, session["usuario"], tiempo, _domicilio, _cuit, _id)
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()

    return redirect('/empresa')

@app.route('/admin/empresa/borrar', methods=['POST'])
def admin_empresa_borrar():
    
    logs.logs1('Borrar Empresa')
 
    _id = request.form['txtId']

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("delete from empresas WHERE id=%s", (_id))
    libros=cursor.fetchall()
    conexion.commit()
    return redirect('/empresa')

@app.route('/admin/empresa/editar', methods=['POST'])
def admin_empresa_editar():

    logs.logs1('Editar Empresa')

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("""Select id, empresa, 
                   CONCAT(DAY(fecha), '/',MONTH(fecha), '/',YEAR(fecha)), 
                   (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = creado_por),
                   cuit,
                   domicilio
                   from empresas where id = 1""")
    empresas=cursor.fetchall()
    conexion.commit
   
    return render_template("/admin/empresas_editar.html", empresas=empresas)