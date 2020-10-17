from flask import Flask, render_template, request, json, url_for, session, redirect, send_from_directory
from flaskext.mysql import MySQL
import bcrypt
import os
import Modelo as Modelo
from PyPDF2 import PdfFileReader
from pathlib import Path
import smtplib
import time
import re
import email
from reportlab.pdfbase import pdfmetrics
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'matangalachanga'

app.config['UPLOAD_PATH'] = 'ArchivosPDF'
app.config['UPLOAD_EXTENSIONS'] = ['.pdf']

@app.route("/")
def hola():
    return render_template("login.html")

@app.route("/inicio")
def select():
    try:
        consulta = Modelo.SelectAll()
        return render_template("jennito.html", eventos=consulta)
    except Exception as e:
        print(str(e))
        return json.dumps({'errooooooror':str(e)})  


@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'GET':
            return render_template("Login.html")
        else:
            _e = request.form.get('Email')
            _p = request.form.get('Password').encode('utf-8')
            
            if _e and _p:
                Modelo.validarUsuario( _e, _p)
                return render_template("jennito.html")
                #return redirect(url_for('inicio'))
            else:
                return "Error correo y contra"
    except Exception as e:
        print(str(e))
        return json.dumps({'errooooooror':str(e)})  


@app.route('/register', methods=['GET', 'POST'])
def Register():
    try:
        if request.method == 'GET':
            return render_template("Register.html")
        else:
            _n = request.form.get('Name')
            _l = request.form.get('Lastname')
            _e = request.form.get('Email')
            _p = request.form.get('Password').encode('utf-8')
            hash_p = bcrypt.hashpw(_p, bcrypt.gensalt())
            if _n and _l and _e and hash_p:
                Modelo.insertarUsuario(_n, _l, _e, hash_p)
                #return render_template("Login.html", session=consulta)
                return redirect(url_for('login'))
            else:                
                return json.dumps({'html':'<span>No se pudo hacer login</span>'})
        
    except Exception as e:
        print(str(e))
        return json.dumps({'eeeeeeerror':str(e)})

@app.route('/Aspirante', methods=['GET', 'POST'])
def Aspirante():
    try:
        if request.method == 'GET':
            return render_template("Aspirante.html")
        else:
            _no = request.form.get('Nombre')
            _ap = request.form.get('Apellidop')
            _am = request.form.get('Apellidom')
            _ed = request.form.get('Edad')
            _po = request.form.get('Puesto')
            _aa = request.form.get('Area')
            _fa = request.form.get('Fecha')
            if _no and _ap and _am and _ed and _po and _aa and _fa:
                Modelo.insertarAspirante(_no, _ap, _am, _ed, _po, _aa, _fa)
                return redirect(url_for('login'))
            else:                
                return json.dumps({'html':'<span>No se ingresaron los los datos</span>'})
        
    except Exception as e:
        print(str(e))
        return json.dumps({'eeeeeeerror':str(e)})

@app.route("/firmar")
def FirmarPDF():
    try:
        consulta = Modelo.Firmar()
        return render_template("jennito.html", eventos=consulta)
    except Exception as e:
        print(str(e))
        return json.dumps({'errooooooror':str(e)})  


@app.route('/EnviarPDF',  methods=['GET', 'POST'])
def EnviarPDF():
    try:
        if request.method == 'GET':
            return render_template("EnviarPDF.html")
        else:
            _e = request.form.get('Email')
            if _e:
                Modelo.EnviarPDF(_e)
                return redirect(url_for('inicio'))
            else:     
                return render_template("jennitoU.html")     
   
    except Exception as e:
        print(str(e))
        return json.dumps({'eeeeeeerror':str(e)})



app.route('/Contrato',methods=["POST","GET"])
def Contrato():
    try:
        if request.method == 'GET':
            return render_template("Layout.html")
        else:
            _no = request.form.get('Nombre')
            _ap = request.form.get('Apellidop')
            _am = request.form.get('Apellidom')
            _ed = request.form.get('Edad')
            _po = request.form.get('Puesto')
            _aa = request.form.get('Area')
            _fa = request.form.get('Fecha')
            if _no and _ap and _am and _ed and _po and _aa and _fa:
                Modelo.CrearPDF(_no, _ap, _am, _ed, _po, _aa, _fa)
                return redirect(url_for('inicio'))
            else:                
                return json.dumps({'html':'<span>No se ingresaron los los datos</span>'})
        
    except Exception as e:
        print(str(e))
        return json.dumps({'eeeeeeerror':str(e)})

if __name__ == "__main__":
    app.run(debug=True)


