from flask import Flask, render_template, request, redirect, url_for
from cargarModelo import cargar_modelo, give_results
from werkzeug.utils import secure_filename
import os

# Variable creamos un objeto con el nombre del archivo
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(__file__),'./static')

def saveImage(file):
  filename = secure_filename(file.filename)
  path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
  file.save(path)
  return path

# Definimos un metodo para poder procesar una peticion desde el navegador 
# http://localhost:5000/
@app.route('/')
def inicio():
    return f'Hola mundo desde Flask! {request.path}'

@app.route('/enviarImagen', methods=['GET', 'POST'])
def enviar_imagen():
    if request.method == 'POST':
        f = request.files['archivo']
        image_path = saveImage(f)
        print(f)
        give_results(image_path)
        return f'Imagen enviada'
    else:
        return render_template('enviarImagen.html')

@app.route('/api/prueba', methods=['POST'])
def api_prueba():
    if request.method == 'POST':
        pass

@app.route('/prueba', methods=['GET', 'POST'])
def prueba():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # generar token
        '''codigo para generar token'''
        json_test = {
            "username": username,
            "password": password,
            "token": "Ae61xvfe7fjezq1",
        } 
        return redirect(url_for('prueba_Autorizado',token=json_test["token"]))
    else:
        return render_template('prueba.html')

@app.route('/pruebaAutorizado/<token>', methods=['GET','POST'])
def prueba_Autorizado(token):
    if request.method == 'GET':
        # comprueba si tienes token
        '''codigo para que compruebe el token'''

        # aqui se devolveria el diccionario con los datos del usuario
        return render_template('pruebaAutorizado.html',token=token)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(email,password)
        json_test = {
            "email": email,
            "password": password,
            "token": "Ae61xvfe7fjezq1",
        } 
        return redirect(url_for('prueba_Autorizado',token=json_test["token"]))

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        birthday = request.form['birthday']
        weight = request.form['weight']
        height = request.form['height']
        print(name, email, password, birthday, weight, height)
        json_test = {
            "email": email,
            "password": password,
            "token": "Ae61xvfe7fjezq1",
        } 
        return redirect(url_for('prueba_Autorizado',token=json_test["token"]))

if __name__ == '__main__':
    cargar_modelo()
    app.run(host='127.0.0.1', port=5000, debug=True)
