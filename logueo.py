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


##########################################
################## LOGUEO ################
##########################################

@app.route('/login')
def logueo():

    return render_template("/admin/login.html")

@app.route('/admin/login', methods = ['POST'] )
def admin_login_post():

    logs.logs1('Logueo')

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("""select count(*) from periodos_activos 
                   where activo = 1 and tipo_licencia = 'Vacaciones'""")
    lic_vac=cursor.fetchall()
    conexion.commit
    licencia_vacaciones = int(lic_vac[0][0])

    session["licencia_vacaciones"]= licencia_vacaciones

    _usuario = request.form['txtUsuario']
    _password = request.form['txtPassword']

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("""Select count(*) from `usuario` 
                   where nombre_usuario = %s and clave_usuario = %s""", (_usuario, _password))
    libros=cursor.fetchall()
    conexion.commit
    verificacion = int(libros[0][0])

    if  verificacion == 1:
        cursor=conexion.cursor()
        cursor.execute("""Select count(*) from usuario 
                       where nombre_usuario = %s and clave_usuario = 'Clave123'""", (_usuario))
        clave=cursor.fetchall()
        conexion.commit
        cambiar_clave = int(clave[0][0])

        cursor=conexion.cursor()
        cursor.execute("Select count(*) from saludos where id_recibe = %s and visto = 0", (_usuario))
        saludos=cursor.fetchall()
        conexion.commit
        nuevos_saludos = int(saludos[0][0])

        if cambiar_clave > 0:
            return render_template("/admin/login.html", mensaje = "A2", usuario = _usuario)
        else:
                cursor=conexion.cursor()
                cursor.execute("""Select count(*), sexo,
                                (select nivel from niveles where niveles.orden = funcion) as nivel,
                                nombre, 
                                (select id_aprobacion from aprobaciones where id_aprobacion = aprobacion) as aprobacion
                                from usuario 
                                where nombre_usuario = %s and clave_usuario = %s 
                                group by sexo, nombre, nivel, aprobacion""", (_usuario, _password))
                libros=cursor.fetchall()
                conexion.commit
                sexo = str(libros[0][1])
                funcion = str(libros[0][2])
                nombre = str(libros[0][3])
                aprobacion = int(libros[0][4])
                
                if funcion == 'Admin':
                    session["login"]=True
                    session["usuario"]=_usuario
                    session["sexo"]= sexo
                    session["nombre_usr"]= nombre
                    session["aprobacion"]= aprobacion
                    session["funcion"]= funcion
                    session["nuevos_saludos"]= nuevos_saludos
                    return redirect("/administrador")
                    if sexo == "M":
                        mensaje2 = "Bienvenido"
                    else:
                        mensaje2 = "Bienvenida"
                    return render_template("/index.html", mensaje = mensaje2)
                else:    
                    session["login"]=True
                    session["usuario"]=_usuario
                    session["sexo"]= sexo
                    session["aprobacion"]= aprobacion
                    session["nombre_usr"]= nombre
                    session["funcion"]= funcion
                    session["nuevos_saludos"]= nuevos_saludos                    
                    return redirect("/inicio")
                    if sexo == "M":
                        mensaje2 = "Bienvenido"
                    else:
                        mensaje2 = "Bienvenida"
                    return render_template("/admin/login.html", mensaje = mensaje2)
    else:
            return render_template("/admin/login.html", mensaje = "Acceso Denegado")



@app.route('/admin/cambio_clave', methods=['POST'])
def cambio_clave():

    logs.logs1('Cambio Clave Admin')


    _nuevaclave = request.form['txtNuevaclave']
    _usuario = request.form['usuario']

    sql = "insert into logueo (fecha, sitio, usuario) values (now(), 'Cambio Clave',%s );"
    datos= (_usuario)
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()

    sql = "update `usuario` set clave_usuario = %s where nombre_usuario = %s;"
    datos= ( _nuevaclave, _usuario)
    conexion= mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()
    
    return redirect("/")

@app.route('/cambio_clave')
def cambio_clave2():
    
    logs.logs1('Cambio Clave Usuario')


    return render_template("/sitio/cambio_clave.html")











@app.route('/cumple/login2', methods = ['POST'] )
def admin_login2_post():

    _usuario = request.form['txtUsuario']
    _password = request.form['txtPassword']

    if (_usuario == 'gfasanella') & (_password == 'entrada'):
        return render_template("/cumple/primera.html")
    else:
        return render_template("/cumple/login.html")

@app.route('/cumple/login3', methods = ['POST'] )
def admin_login3_post():

    _santi = request.form['opcion_santi']
    _sofi = request.form['opcion_sofi']
    _diego = request.form['opcion_diego']

    if (_santi == 'PlayStation') & (_sofi == 'Pilates') & (_diego == 'Basket'):
        return render_template("/cumple/tercera.html")
    else:
        return render_template("/cumple/primera.html")


@app.route('/cumple/login4', methods = ['POST'] )
def admin_login4_post():

    _dulce = request.form['preferido_santi']
    
    if (_dulce == 'jugador'):
        return render_template("/cumple/cuarta.html")
    else:
        return render_template("/cumple/tercera.html")


@app.route('/cumple/login5', methods = ['POST'] )
def admin_login5_post():

    _dulce = request.form['codigo_dulce']
    
    if (_dulce == 'chocolate'):
        return render_template("/cumple/quinta.html")
    else:
        return render_template("/cumple/cuarta.html")


@app.route('/cumple/login6', methods = ['POST'] )
def admin_login6_post():

    _dulce = request.form['codigo_electrico']
    
    if (_dulce == 'perfume'):
        return render_template("/cumple/sexta.html")
    else:
        return render_template("/cumple/quinta.html")


@app.route('/cumple/login7', methods = ['POST'] )
def admin_login7_post():

    _dulce = request.form['codigo_u2']
    
    if (_dulce == 'mate_yerba'):
        return render_template("/cumple/septima.html")
    else:
        return render_template("/cumple/sexta.html")



