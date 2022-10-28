from dataclasses import replace
from flask import flash
from datetime import datetime
from multiprocessing.dummy import connection
import sqlite3
import enviaremail

DB_NAME='dblibreria.s3db'

def conexion():
    conn=sqlite3.connect(DB_NAME)
    return conn

def add_registro(nombre,apellido,usuario,pass1):
    ## genera códigi unico
    cod_ver=str(datetime.now())
    cod_ver=cod_ver.replace("-","")
    cod_ver=cod_ver.replace(" ","")
    cod_ver=cod_ver.replace(":","")
    cod_ver=cod_ver.replace(".","")
    ##flash(cod_ver)
    ### para que no salga erorroes de base de datos en las vistas
    
    try:
        db=conexion()
        cursor=db.cursor()

        sql='INSERT INTO usuarios(nombre,apellido,usuario,passw,cod_v,verifi,id_rol) VALUES(?,?,?,?,?,?,?)'

        cursor.execute(sql,[nombre,apellido,usuario,pass1,cod_ver,0,1])
        db.commit()
        ##envío codigo de verificación al correo
                
        enviaremail.enviar_email(usuario,cod_ver)
        return True
    except:
        return False

def validacion_login(usu):
    try:
        db=conexion()
        cursor=db.cursor()
        sql='SELECT * FROM usuarios WHERE usuario=?'
        cursor.execute(sql,[usu])
        ## me retorna uncampo
        resul=cursor.fetchone()
        datos=[
            {
                'id':resul[0],
                'nombre':resul[1],
                'apellido':resul[2],
                'usuario':resul[3],
                'passw':resul[4],
                'cod_v':resul[5],
                'verifi':resul[6],
                'id_rol':resul[7]

            }
        ]
        return datos
    except:
        return False

def activar_cuenta(usu,cod_v):
    try:
        db=conexion()       
        cursor=db.cursor()
        sql='UPDATE usuarios SET verifi=1 WHERE usuario=? AND cod_v=?'
        cursor.execute(sql,[usu,cod_v])
        db.commit()
        return True
    except:
        return False

def listar_mensajes(tipo,username):

    listmensajeria=[]
    
    
    try:
        db=conexion()
        cursor=db.cursor()
        sql='SELECT * FROM mensajeria ORDER BY fecha DESC'
        if tipo == 1:
            cursor.execute(sql)
        else:
            sql='SELECT * FROM mensajeria WHERE remitente=? OR destinatario=? ORDER BY fecha DESC'
            cursor.execute(sql,[username,username])

        resul=cursor.fetchall()
        listmensajeria=[]
        for m in resul:
            tipo=''
            if m[1]==username:
                tipo='Mensaje Enviado'
            else:
                tipo='Mensaje Recibido'

            registro={
                    
                    'id':m[0],
                    'remitente':m[1],
                    'destinatario':m[2],
                    'asunto':m[3],                   
                    'mensaje':m[4],
                    'fecha':m[5],
                    'tipo':tipo
                }
            listmensajeria.append(registro)

    except:
        registro={'Resultado':'No existe Mensaje'

        }
        listmensajeria.append(registro)
    
    return listmensajeria

def listar_g_usuarios():
    
    listusu=[]
    try:
        db=conexion()
        cursor=db.cursor()
        sql='SELECT * FROM usuarios'
        cursor.execute(sql)
        resul=cursor.fetchall()
        listusu=[]
        for u in resul:
            registro={
                    
                    'id':u[0],
                    'nombre':u[1],
                    'apellido':u[2],
                    'usuario':u[3],
                    'id_rol':u[7]
                }
            listusu.append(registro)

    except:
        registro={'Resultado':'No existe Mensaje'

        }
        listusu.append(registro)
    
    return listusu

def listar_usuario(usu):
    try:
        db=conexion()
        cursor=db.cursor()
        sql='SELECT * FROM usuarios WHERE usuario<>?'
        cursor.execute(sql,[usu])
        ## me retorna una lista
        resul=cursor.fetchall()
        usuarios=[]
        for u in resul:
            registro={
                    'id':u[0],
                    'nombre':u[1],
                    'apellido':u[2],
                    'usuario':u[3],                   
                    'id_rol':u[7]
                }
            usuarios.append(registro)

        return usuarios
    except:
        return False


def adicionar_mensaje(rem,dest,asunto,cuerpo):
    
    try:
        db=conexion()
        cursor=db.cursor()

        sql='INSERT INTO mensajeria(remitente,destinatario,asunto,mensaje) VALUES(?,?,?,?)'

        cursor.execute(sql,[rem,dest,asunto,cuerpo])
        db.commit()
               
        return True
    except:
        return False

def listar_mensaje():
    try:
        db=conexion()
        cursor=db.cursor()
        sql='SELECT * FROM mensajeria'
        cursor.execute(sql)
        ## me retorna una lista
        resul=cursor.fetchall()
        usuarios=[]
        for u in resul:
            registro={
                    'id':u[0],
                    'remitente':u[1],
                    'destinatario':u[2],
                    'asunto':u[3],                   
                    'mensaje':u[4],
                    'fecha':u[5]
                }
            usuarios.append(registro)

        return usuarios
    except:
        return False


def recupera_cuenta(usu):
    
    try:
        db=conexion()
        cursor=db.cursor()
        sql='SELECT *FROM usuarios WHERE usuario=?'
        cursor.execute(sql,[usu])
        db.commit()
        resul=cursor.fetchone()
        if resul!=None:
            enviaremail.recuperar_email(usu)
            return 'SI'
        else:
            return 'NO'
    except:
        return False


def restablecer_cuenta(usu,p1):
    
    try:
        db=conexion()
        cursor=db.cursor()
        sql='UPDATE usuarios SET passw=? WHERE usuario=?'
        cursor.execute(sql,[p1,usu])
        db.commit()
        
        return True
    except:
        return False
