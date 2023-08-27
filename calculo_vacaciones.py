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
from usuarios import *
from logueo import *
from listar_cronograma import *



@app.route('/cargarvacaciones')
def cargarvacaciones():

    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'cargarvacaciones',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()        
 
    tiempo = datetime.now().year

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select periodo, count(*), sum(dias_totales), sum(dias_tomados), sum(dias_pendientes), sum(dias_por_aprobarse), (select case when activo = 0 then 'Activar' else 'Ya activo' end from periodos_activos where periodos_activos.periodo = stock_vacaciones.periodo and periodos_activos.tipo_licencia = 'Vacaciones'), (select case when activo = 0 then 'btn btn-info btn-sm' else 'btn btn-success btn-sm' end from periodos_activos where periodos_activos.periodo = stock_vacaciones.periodo and periodos_activos.tipo_licencia = 'Vacaciones'), sum(dias_aprobados)  from stock_vacaciones group by periodo")
    calculo=cursor.fetchall()
    conexion.commit

    return render_template("/admin/cargarvacaciones.html", calculo = calculo, tiempo = tiempo)

@app.route('/cargarvacaciones/borrar', methods=['POST'])
def cargarvacaciones_borrar():

    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'cargarvacaciones_borrar',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   

    _periodo = request.form['Periodo']

    sql = "delete from `stock_vacaciones` where periodo = %s;"
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,_periodo)
    conexion.commit()
    
    sql = "delete from periodos_activos where periodo = %s and tipo_licencia = 'Vacaciones';"
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,_periodo)
    conexion.commit()
    

    return redirect("/cargarvacaciones")

@app.route('/cargarvacaciones/entrar', methods=['POST'])
def cargarvacaciones_entrar():

    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'listar_vacaciones_por_empleado',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   

    _periodo = request.form['Periodo']

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT *, case when dias = 7 then 'Editar' else 'Revisar' end from stock_vacaciones where periodo = %s", (_periodo))
    listar=cursor.fetchall()
    conexion.commit

    return render_template("/admin/listar_empleado.html", listar = listar)



@app.route('/admin/cargarvacaciones/grabar', methods=['POST'])
def admin_cargarvacaciones_grabar():

    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'admin_cargarvacaciones_grabar',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()        
 
    _Idvacaciones = request.form['Idvacaciones']
    _dias_totales = request.form['dias_totales']
    _dias_tomados = request.form['dias_tomados']
    _dias_pendientes = request.form['dias_pendientes']
    _dias_por_aprobarse = request.form['dias_por_aprobarse']
    _dias_aprobados = request.form['dias_aprobados']
    tiempo = datetime.now()

    sql = "update stock_vacaciones set dias_totales = %s, dias_tomados = %s, dias_pendientes = %s, dias_por_aprobarse = %s, usuario_modifica = %s, fecha_modifica = %s, dias_aprobados = %s where id = %s;"

    datos=(_dias_totales,_dias_tomados,_dias_pendientes, _dias_por_aprobarse, session["usuario"], tiempo, _dias_aprobados,_Idvacaciones)
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()

    return redirect("/listarempleado")

@app.route('/alta_periodo')
def alta_periodo():
    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'alta_periodo',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   
    
    tiempo = datetime.now()

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("drop table periodo_nuevo")
    drop_periodo=cursor.fetchall()
    conexion.commit

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("create table periodo_nuevo as (SELECT year(now()) as periodo, nombre_usuario, year(now())-year(fecha_incorporacion) antiguedad, now() creacion, 0 dias FROM usuario where year(fecha_incorporacion) > 1900)")
    create_periodo=cursor.fetchall()
    conexion.commit

    sql = "update `periodo_nuevo` set `dias` = (SELECT dias from reglas_vacaciones where periodo_nuevo.antiguedad between reglas_vacaciones.desde and reglas_vacaciones.hasta)"
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql)
    conexion.commit()

    sql = "delete from stock_vacaciones where periodo = year(now());"
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql)
    conexion.commit()

    sql = "insert into stock_vacaciones (id_empleado, periodo, dias_totales, dias_tomados, dias_pendientes, dias_por_aprobarse, usuario_modifica, fecha_modifica, dias_aprobados) select nombre_usuario, cast(periodo as char), dias, 0, dias, 0, %s, now(), 0 from periodo_nuevo;"
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, session["usuario"])
    conexion.commit()

    sql = "delete from periodos_activos where periodo = year(now()) and tipo_licencia = 'Vacaciones';"
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql)
    conexion.commit()

    sql = "insert into periodos_activos (periodo, tipo_licencia, activo, creado_por, fecha) values (year(now()), 'Vacaciones',0,%s,%s);"
    conexion= mysql.connect()
    cursor = conexion.cursor()
    datos=(session["usuario"], tiempo)
    cursor.execute(sql, datos)
    conexion.commit()


    return redirect("/cargarvacaciones")


@app.route('/reglas_vacaciones')
def reglas_vacaciones():

    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'reglas_vacaciones',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("Select id, desde, hasta, dias, (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = creado_por), fecha from reglas_vacaciones order by desde asc")
    reglas=cursor.fetchall()
    conexion.commit

    return render_template("/admin/regla_vacaciones.html", reglas = reglas)

@app.route('/admin/reglas_vacaciones/guardar', methods=['POST'])
def reglas_vacaciones_guardar():

    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'insertar_reglas_vacaciones',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   

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
    
    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'borrar_reglas_vacaciones',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   

    _id = request.form['txtId']

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("delete from reglas_vacaciones WHERE id=%s", (_id))
    libros=cursor.fetchall()
    conexion.commit()
    return redirect('/reglas_vacaciones')

@app.route('/listarvacaciones')
def listar():
    
    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'listar_vacaciones',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT *, case when dias_totales < 8 then 'btn btn-warning btn-sm' else 'btn btn-info btn-sm' end, case when dias_totales < 8 then 'Revisar' else 'Editar' end from stock_vacaciones")
    listar=cursor.fetchall()
    conexion.commit

    return render_template("/admin/listar_vacaciones.html", listar = listar)


@app.route('/admin/vacaciones/borrar', methods=['POST'])
def admin_vacaciones_borrar():
    
    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'borrar_vacaciones_individuales',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   

    _id = request.form['Idvacaciones']
    print (_id)

    sql = "delete from stock_vacaciones where id = %s;"
    datos= (_id)
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()
    
    return redirect ("/listarvacaciones")


@app.route('/admin/vacaciones/grabar', methods=['POST'])
def admin_vacaciones_grabar():

    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'grabar_vacaciones_individuales',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   
 
    _Idvacaciones = request.form['Idvacaciones']
    _dias_totales = request.form['dias_totales']
    _dias_tomados = request.form['dias_tomados']
    _dias_pendientes = request.form['dias_pendientes']
    _dias_por_aprobarse = request.form['dias_por_aprobarse']
    _dias_aprobados = request.form['dias_aprobados']
    tiempo = datetime.now()

    sql = "update stock_vacaciones set dias_totales = %s, dias_tomados = %s, dias_pendientes = %s, dias_por_aprobarse = %s, usuario_modifica = %s, fecha_modifica = %s, dias_aprobados = %s where id = %s;"

    datos=(_dias_totales,_dias_tomados,_dias_pendientes, _dias_por_aprobarse, session["usuario"], tiempo, _dias_aprobados, _Idvacaciones)
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()

    return redirect("/listarvacaciones")

@app.route('/admin/vacaciones/editar', methods=['POST'])
def admin_vacaciones_editar():

    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'editar_vacaciones_individuales',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   

    _id = request.form['Idvacaciones']

    sql = "select *, (select concat(nombre,' ', apellidos) from usuario where nombre_usuario = id_empleado), (select concat(day(fecha_incorporacion), '-', month(fecha_incorporacion),'-',year(fecha_incorporacion)) from usuario where nombre_usuario = id_empleado), concat(day(fecha_modifica), '-', month(fecha_modifica),'-',year(fecha_modifica)) from stock_vacaciones where id = %s;"
    datos=(_id)
    conexion= mysql.connect()
    editar = conexion.cursor()
    editar.execute(sql,datos)
    conexion.commit()

    return render_template("/admin/editar_vacaciones.html", editar = editar)

@app.route('/vacaciones_alta_empleado')
def admin_vacaciones_alta_empleado():

    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'alta_vacaciones_individuales',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   

    sql = "select distinct(periodo) from stock_vacaciones;"
    
    conexion= mysql.connect()
    periodo = conexion.cursor()
    periodo.execute(sql)
    conexion.commit()

    sql = "select concat(nombre, ' ', apellidos), nombre_usuario, concat(day(fecha_incorporacion), '-', month(fecha_incorporacion),'-',year(fecha_incorporacion)) from usuario group by concat(nombre , ' ' , apellidos), nombre_usuario;"
    
    conexion= mysql.connect()
    usuario = conexion.cursor()
    usuario.execute(sql)
    conexion.commit()


    return render_template("/admin/agregar_vacaciones.html", periodo = periodo, usuario = usuario)

@app.route('/admin/vacaciones/grabar_manual', methods=['POST'])
def admin_vacaciones_grabar_manual():

    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'grabado_vacaciones_individuales',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   
 
    _IdEmpleado = request.form['IdEmpleado']
    _IdPeriodo = request.form['IdPeriodo']
    _dias_totales = request.form['dias_totales']
    _dias_tomados = request.form['dias_tomados']
    _dias_pendientes = request.form['dias_pendientes']
    _dias_por_aprobarse = request.form['dias_por_aprobarse']
    _dias_aprobados = request.form['dias_aprobados']
    tiempo = datetime.now()

    sql = "insert into stock_vacaciones (id_empleado, periodo, dias_totales, dias_tomados, dias_pendientes, dias_por_aprobarse, usuario_modifica, fecha_modifica, dias_aprobados) values (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
    datos=(_IdEmpleado, _IdPeriodo, _dias_totales,_dias_tomados,_dias_pendientes, _dias_por_aprobarse, session["usuario"], tiempo, _dias_aprobados)
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()

    return redirect("/listarvacaciones")

@app.route('/cargarvacaciones/activar', methods=['POST'])
def cargarvacaciones_activar():

    if not 'login' in session:
        return redirect("/login")

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'activar_periodo_vacaciones',%s );"
    datos= (session["usuario"])
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()   

    sql = "update `periodos_activos` set activo = 1 where periodo = 2023 and tipo_licencia = 'Vacaciones';"
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql)
    conexion.commit()
    
    return redirect("/cargarvacaciones")
