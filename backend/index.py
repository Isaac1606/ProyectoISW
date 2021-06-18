from flask import Flask, render_template, request, redirect, url_for
from cargarModelo import cargar_modelo, give_results
from werkzeug.utils import secure_filename
import db
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

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        token = db.checkCredentials(email,password)
        if token is None :
            return render_template('login.html')

        return redirect(url_for('perfil',token=token))

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        bloods = db.getBloods()
        skins = db.getSkins()
        return render_template('register.html', bloods = bloods , skins = skins)

    elif request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        birthday = request.form['birthday']
        sex = request.form['sex']
        weight = request.form['weight']
        height = request.form['height']
        blood = request.form['blood']
        skin = request.form['skin']

        userRequest = {
            "email" : email,
            "password" : password,
            "name" : name,
            "birthday" : birthday,
            "sex" : sex,
            "weight" : weight,
            "height" : height,
            "blood" : blood,
            "skin" : skin
        }

        token = db.createUser(userRequest)
        if token is None :
            return render_template('register.html')

        return redirect(url_for('perfil',token=token))

@app.route('/<token>/perfil',methods=['GET','POST'])
def perfil(token):
    if request.method == 'GET':

        usertoken = db.validateToken(token)
        if usertoken is None :
            return render_template('login.html')

        user = db.getUser(usertoken[1])
        if user is None :
            return render_template('login.html')

        informacion_general = {
            "name": user['name'],
            "email": user['email'],
            "fecha_nacimiento": user['birthday'],
            "sexo": user['sex']
        }
        
        informacion_clinica = {
            "estatura": user['height'],
            "peso": user['weight'],
            "skin" : user['skin'],
            "blood" : user['blood']
        }
        
        bloods = db.getBloods()
        skins = db.getSkins()
        if bloods is None or skins is None :
            return render_template('login.html')

        return render_template('perfil.html', token=token, ig= informacion_general, ic= informacion_clinica, bloods = bloods, skins = skins)

    if request.method == 'POST':

        name = request.form['name']
        birthday = request.form['birthday']
        sex = request.form['sex']
        weight = request.form['weight']
        height = request.form['height']
        blood = request.form['blood']
        skin = request.form['skin']

        userRequest = {
            "token" : token,
            "name" : name,
            "birthday" : birthday,
            "sex" : sex,
            "weight" : weight,
            "height" : height,
            "blood" : blood,
            "skin" : skin
        }
        db.updateUser(userRequest)

        return redirect(url_for('perfil',token=token))

@app.route('/<token>/prediagnosticos', methods=['GET'])
def prediagnosticos(token):
    if request.method == 'GET':
        pass

@app.route('/<token>/alergias', methods=['GET', 'POST'])
def alergias(token):
    if request.method == 'GET':

        usertoken = db.validateToken(token)
        if usertoken is None :
            return render_template('login.html')

        userAllergies = db.getUserAllergies(usertoken[1])

        return render_template('alergias.html', token=token, allergies = userAllergies)

    if request.method == 'POST':

        allergy = request.form['descripcionAlergia']
        date = request.form['fechaAlergia']

        userRequest = {
            "token" : token,
            "date" : date,
            "allergy" : allergy
        }
        db.insertUserAllergy(userRequest)

        return redirect(url_for('alergias',token=token))


@app.route('/resetPassword', methods=['GET', 'POST'])
def resetPassword():
    return render_template('recuperarPassword.html')
if __name__ == '__main__':
    cargar_modelo()
    app.run(host='127.0.0.1', port=5000, debug=True)
