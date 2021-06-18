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
        allergies = db.getAllergies()

        return render_template('alergias.html', token=token, allergies = userAllergies, all_catalog = allergies)

    elif request.method == 'POST':

        allergy = request.form['descripcionAlergia']
        date = request.form['fechaAlergia']

        userRequest = {
            "token" : token,
            "date" : date,
            "allergy" : allergy
        }
        db.insertUserAllergy(userRequest)

        return redirect(url_for('alergias',token=token))

@app.route('/<token>/borrarAlergia/<alergia>', methods=['POST'])
def borrarAlergia(token,alergia):
    if request.method == 'POST':

        userRequest = {
            "token" : token,
            "allergy" : alergia
        }

        db.deleteUserAllergy(userRequest)

        return redirect(url_for('alergias',token=token))

@app.route('/<token>/consultas', methods=['GET','POST'])
def consultas(token):
    if request.method == 'GET' :
        
        usertoken = db.validateToken(token)
        if usertoken is None :
            return render_template('login.html')
        
        userConsults = db.getUserConsults(usertoken[1])
        return render_template('consultas.html', token = token, consultas = userConsults)

    elif request.method == 'POST' :

        consult_date = request.form['fechaConsulta']
        consult_desc = request.form['descripcionConsulta']

        userRequest = {
            "token" : token,
            "date" : consult_date,
            "desc" : consult_desc
        }

        db.insertUserConsult(userRequest)

        return redirect(url_for('consultas',token=token))

@app.route('/<token>/borrarConsulta/<id_consulta>', methods=['POST'])
def borrarConsulta(token,id_consulta):
    if request.method == 'POST':

        userRequest = {
            "token" : token,
            "id_consulta" : id_consulta
        }

        db.deleteUserConsult(userRequest)

        return redirect(url_for('consultas',token=token))

@app.route('/<token>/logout', methods=['POST'])
def logout(token):
    if request.method == 'POST':

        db.deleteUserToken(token)

        return redirect(url_for('login'))

@app.route('/password', methods=['POST'])
def passwordRecovery():
    if request.method == 'GET' :

        return render_template('recuperarPassword.html')
    
    elif request.method == 'POST' :

        email = request.form['email']
        
        valid = db.sendMail(email)
        if valid is None :
            return redirect(url_for('passwordRecovery'))    

        return redirect(url_for('insertToken'))

@app.route('/newpassword', methods=['POST'])
def insertToken():
    if request.method == 'GET' :

        return render_template('ingresaCodigo.html')
    
    elif request.method == 'POST' :

        codigo = request.form['codigo']
        password = request.form['contrasena']
        r_password = request.form['r_contrasena']
        if password != r_password :
            return redirect(url_for('insertToken'))
        
        db.changePassword(codigo,password)
        
        return redirect(url_for('login'))

if __name__ == '__main__':
    cargar_modelo()
    app.run(host='127.0.0.1', port=5000, debug=True)
