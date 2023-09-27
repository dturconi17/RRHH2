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

@app.route('/usuarios')
def usuarios():

    logs.logs1('Listado Usuarios')

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT id, nombre_usuario, nombre, apellidos, orden, funcion, aprobacion, estructura, cargo FROM usuario")
    usuarios=cursor.fetchall()
    conexion.commit
    
    return render_template("/admin/usuarios.html", usuarios=usuarios)

@app.route('/usuarios/borrar', methods=['POST'])
def usuarios_borrar():

    logs.logs1('Borrar Usuarios')

    _id = request.form['Idusuario']

    sql = "delete from `usuario` where id = %s;"
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,_id)
    conexion.commit()
    
    return redirect("/usuarios")


@app.route('/usuarios/reseteo', methods=['POST'])
def usuarios_reseteo():

    logs.logs1('Reseteo Clave')

    _id = request.form['Idusuario']

    sql = "update `usuario` set clave_usuario = 'Clave123' where id = %s;"
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,_id)
    conexion.commit()
    
    return redirect("/usuarios")



@app.route('/alta_usuario')
def alta_usuario():

    logs.logs1('Alta Usuarios')

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select empresa, id from empresas")
    empresas=cursor.fetchall()
    conexion.commit

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select concat(cargo_general,' - ',cargo_sub), id from cargos")
    niveles=cursor.fetchall()
    conexion.commit

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select concat((select nivel from niveles where tipo_area = niveles.id),' ',area), id from estructuras")
    estructura=cursor.fetchall()
    conexion.commit

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select  id, descripcion from aprobaciones")
    aprobacion=cursor.fetchall()
    conexion.commit

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select  id, nivel from niveles where id in (1,15)")
    admin=cursor.fetchall()
    conexion.commit

    return render_template("admin/alta_usuario.html", admin=admin, niveles = niveles, empresas = empresas, estructura=estructura, aprobacion = aprobacion)

@app.route('/alta/usuarionuevo', methods=['POST'])
def alta_usuarionuevo():

    logs.logs1('Graba Usuarios')

     
    _nombre = request.form['nombre']
    _apellido = request.form['apellido']
    _sexo = request.form['sexo']
    _mail = request.form['mail']
    _funcion = request.form['Admin']
    _documento = request.form['documento']
    tiempo = datetime.now()
    _empresa = request.form['Empresa']
    _fecha_incorporacion = request.form['fecha_incorporacion']
    _estructura = request.form['Estructura']
    _aprobacion = request.form['Aprobacion']
    _cargo = request.form['Cargo']

    _usuarionuevo = _nombre[0:1].lower() + _apellido[0:1].lower() + _documento[-5:]
    

    sql = """INSERT INTO `usuario` 
    (nombre_usuario, clave_usuario, nombre, apellidos, documento, sexo, mail, 
    empresa, funcion, estructura, aprobacion, fecha_incorporacion, creador, fecha_alta, orden, cargo) 
    VALUES 
    (%s, 'Clave123', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,0,%s);"""

    datos=(_usuarionuevo, _nombre, _apellido, _documento, _sexo, _mail, _empresa, _funcion, _estructura, _aprobacion, _fecha_incorporacion, session["usuario"], tiempo, _cargo)
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()
    return redirect("/usuarios")


@app.route('/usuarios/editar_usuarionuevo', methods=['POST'])
def editar_usuarionuevo():

    logs.logs1('Edita Usuarios')

    _Idusuario = request.form['Idusuario']
    _nombre = request.form['nombre']
    _apellido = request.form['apellido']
    _sexo = request.form['sexo']
    _mail = request.form['mail']
    _funcion = request.form['funcion']
    _documento = request.form['documento']
    _empresa = request.form['empresa']
    _gerencia = request.form['gerencia']
    _jefatura = request.form['jefatura']
    tiempo = datetime.now()
    _fecha_incorporacion = request.form['fecha_incorporacion']

    print (_fecha_incorporacion)

    sql = "update `usuario` set `nombre` = %s, `apellidos` = %s, `sexo` = %s, `mail` = %s, `funcion` = %s, `fecha_alta` = %s, documento = %s, creador = %s, empresa = %s, gerencia = %s, jefatura =%s, fecha_incorporacion = %s  where id = %s;"
    datos=(_nombre,_apellido, _sexo, _mail, _funcion,  tiempo, _documento, session["usuario"], _empresa, _gerencia, _jefatura,  _fecha_incorporacion, _Idusuario)
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()

    return redirect("/usuarios")


@app.route('/usuarios/editar', methods=['POST'])
def editar_usuario():

    logs.logs1('Edita Listado Usuarios')

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select nivel, id from niveles")
    niveles=cursor.fetchall()
    conexion.commit

    _Idusuario = request.form['Idusuario']

    sql = """select id, nombre_usuario, fecha_incorporacion, nombre, apellidos, 
    documento, sexo, mail, funcion, empresa, orden, funcion, aprobacion
    from usuario where id = %s;"""

    datos=(_Idusuario)
    conexion= mysql.connect()
    editar = conexion.cursor()
    editar.execute(sql,datos)
    conexion.commit()
    return render_template("/admin/editar_usuario.html", editar=editar, niveles=niveles) 