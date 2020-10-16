from flask import Flask, render_template, request, json, url_for, session, redirect, send_from_directory
from flaskext.mysql import MySQL
import bcrypt
import email
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config["DEBUG"] = True
app.config['MYSQL_DATABASE_USER'] = 'sepherot_jennifer'
app.config['MYSQL_DATABASE_PASSWORD'] = 'AW4ur5mHBR'
app.config['MYSQL_DATABASE_DB'] = 'sepherot_jenniferBD'
app.config['MYSQL_DATABASE_HOST'] = 'nemonico.com.mx'
mysql = MySQL(app)


def insertarUsuario(_name, _lastname, _email, _password):
    try:
        if _name and _lastname and _email and _password:
            conn = mysql.connect()
            cursor = conn.cursor()
            _TABLA="USERS"
            sqlDropProcedure="DROP PROCEDURE IF EXISTS InsertarUsuario;"
            cursor.execute(sqlDropProcedure)

            sqlCreateSP="CREATE PROCEDURE InsertarUsuario(IN PName VARCHAR(100), IN PLastname VARCHAR(100), IN PEmail VARCHAR(100), IN PPassword VARCHAR(100)) INSERT INTO "+_TABLA+"(name, last_name, email, password) VALUES (PName, PLastname, PEmail, PPassword)"
            cursor.execute(sqlCreateSP)
            
            cursor.execute("CREATE TABLE IF NOT EXISTS `sepherot_jenniferBD`.`"+_TABLA+"` ( `id_user` INT(11) NOT NULL AUTO_INCREMENT , `name` VARCHAR(100) NULL , `last_name` VARCHAR(100) NULL ,`email` VARCHAR(100) NULL ,`password` VARCHAR(100) NULL, PRIMARY KEY (`id_user`)) ENGINE = InnoDB;")
            cursor.callproc('InsertarUsuario',(_name, _lastname, _email, _password))
            data = cursor.fetchall()

            if len(data)==0:
                conn.commit()             
                ##notificacion de que se creo
            else:
                return json.dumps({'errorrrr':str(data[0])})
        else:
            return json.dumps({'html':'<span>Datos faltantes</span>'})

    except Exception as e:
        return json.dumps({'erroor':str(e)})
    finally:
       cursor.close() 
       conn.close()      

def validarUsuario( _email, _password):
    try:
        if  _email and _password:
            conn = mysql.connect()
            cursor = conn.cursor()
            _TABLA="USERS"
            sqlDropProcedure="DROP PROCEDURE IF EXISTS BuscarUsuario;"
            cursor.execute(sqlDropProcedure)

            sqlCreateSP="CREATE PROCEDURE BuscarUsuario(IN PEmail VARCHAR(100)) SELECT * FROM "+_TABLA+" WHERE (email) = (PEmail)"
            cursor.execute(sqlCreateSP)
            cursor.callproc('BUSCAR USUARIO',(_email))
            data = cursor.fetchone()
            cursor.close() 

            if len(data) == 1:
                if bcrypt.hashpw(_password, data[('password')].encode('utf-8')) == data[('assword')].encode('utf-8'):
                    session['name'] = data[('name')]
                    session['email'] = data[('email')]
                    
                    
                else:
                    return "Error correo y contra"
            else:
                return "Error correo y contra"
        else:
            return json.dumps({'html':'<span>Datos faltantes</span>'})

    except Exception as e:
        return json.dumps({'errOoooor':str(e)})
    finally:
       conn.close() 


def insertarAspirante(_nombre, _apellidop, _apellidom, _edad, _puesto, _area, _fecha):
    try:
        if _nombre and _apellidop and _apellidom and _edad and _puesto and _area and _fecha:
            conn = mysql.connect()
            cursor = conn.cursor()
            _TABLA="ASPIRANTE"
            sqlDropProcedure="DROP PROCEDURE IF EXISTS InsertarAspirante;"
            cursor.execute(sqlDropProcedure)

            sqlCreateSP="CREATE PROCEDURE InsertarAspirante(IN PNombre VARCHAR(60), IN PApellido_paterno VARCHAR(60), IN PApellido_materno VARCHAR(60), IN PEdad INT(11), IN PPuesto VARCHAR(60), IN PArea VARCHAR(60),IN PFecha VARCHAR(60)) INSERT INTO "+_TABLA+" (nombre, apellido_paterno, apellido_materno, edad, puesto, area, fecha) VALUES (PNombre, PApellido_paterno, PApellido_materno, PEdad, PPuesto, PArea, PFecha)"
            cursor.execute(sqlCreateSP)
            
            cursor.execute("CREATE TABLE IF NOT EXISTS  `sepherot_jenniferBD`.`"+_TABLA+"`  ( `ID` INT(11) NOT NULL AUTO_INCREMENT , `nombre` VARCHAR(60) NOT NULL , `apellido_paterno` VARCHAR(60) NOT NULL , `apellido_materno` VARCHAR(60) NOT NULL ,`edad` INT(11) NOT NULL, `puesto` VARCHAR(60) NOT NULL, `area` VARCHAR(60) NOT NULL ,`fecha` VARCHAR(60) NOT NULL ,  PRIMARY KEY (`ID`)) ENGINE = InnoDB;")
            cursor.callproc('InsertarAspirante',(_nombre, _apellidop, _apellidom, _edad, _puesto, _area, _fecha))
            data = cursor.fetchall()
            
            if len(data) == 0:
                conn.commit()
                return data
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Datos faltantes</span>'})
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
       cursor.close() 
       conn.close()





def SelectAll():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        _TABLA = "ASPIRANTE"
        sqlSelectAllProcedure = "SELECT * FROM " + _TABLA
        cursor.execute(sqlSelectAllProcedure)
        data = cursor.fetchall()
        return data
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()

def drawMyRuler(pdf):
    pdf.drawString(100,810, 'x100')
    pdf.drawString(200,810, 'x200')
    pdf.drawString(300,810, 'x300')
    pdf.drawString(400,810, 'x400')
    pdf.drawString(500,810, 'x500')

    pdf.drawString(10,100, 'y100')
    pdf.drawString(10,200, 'y200')
    pdf.drawString(10,300, 'y300')
    pdf.drawString(10,400, 'y400')
    pdf.drawString(10,500, 'y500')
    pdf.drawString(10,600, 'y600')
    pdf.drawString(10,700, 'y700')
    pdf.drawString(10,800, 'y800') 


def CrearPDF(_nombre, _apellidop, _apellidom, _edad, _puesto, _area, _fecha):
    try:
        #os.remove(".\Contrato_Aspirante.pdf")
        if _nombre and _apellidop and _apellidom and _edad and _puesto and _area and _fecha:
            conn = mysql.connect()
            cursor = conn.cursor()
            
            _Nombre= _nombre
            _NombreArchivo="Contrato_Aspirante.pdf" 
            _TituloDocumento="Contrato Aspirante"
            _ln= _apellidom
            _lnp= _apellidop
            _ed= _edad
            _pu= _puesto
            _ar= _area
            _fh= _fecha
            c=canvas.Canvas(_NombreArchivo)
            c.setTitle(_TituloDocumento)
            c.setLineWidth(.3)
            c.setFont('Helvetica',36)

            textLines = [
                'Contrato del aspirante: ', _Nombre ,'Con apellido paterno: ', _ln ,
                'Y apellido materno: ', _lnp ,'Con edad de; ', _ed ,
                'Entrara al puesto de: ', _pu,'Al área:', _ar,'El día:', _fh ,
                'El “aspirante" se compromete a asistir de 9:00-5:00 a',
                'de cada semana al domicilio de la empresa que le sea',
                'asignada por parte de la empresa, para realizar',
                'su trabajo laboral y, de esta manera, aprender',
                'las funciones de integración. La empresa se compromete a ',
                'otorgar al "aspirante",a partir de la fecha de celebración',
                'del presente convenio, un salario, con la finalidad de',
                'que pueda sostener parte de sus necesitas y que al',
                'realizar su trabajo laboral  dentro de la',
                'empresa asignada, se le enseñe al "aspirante"' ,
                'la actividad señalada en la cláusula anterior.'
                ]
           
            c.drawCentredString(300,760,_TituloDocumento)
            c.setFont('Helvetica',20)
            text = c.beginText(100,680)
            text.setFont("Helvetica", 18)
            for line in textLines:
                text.textLine(line)
                
                
            c.drawText(text)
            c.drawCentredString(300,80,_Nombre)
            c.line(200,100,400,100)
            
            c.save()
            data = cursor.fetchall()
        else:
            print("error")
            return json.dumps({'html':'<span>Datos faltantes</span>'})
    except Exception as e:
        print("error 2")
        print(json.dumps({'error':str(e)}))
        return json.dumps({'error':str(e)})
    finally:
        
        print("cierre")
        conn.close()




def Firmar():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        _TABLA = "ASPIRANTE"
        sqlSelectAllProcedure = "SELECT * FROM " + _TABLA
        cursor.execute(sqlSelectAllProcedure)
        data = cursor.fetchall()
        return data
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()


def EnviarPDF(_e):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        sql= "DELETE * FROM  `USERS`  WHERE email = %s"
        cursor.execute(sql,(_e))
        data = cursor.fetchone()
        return data

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()
