from flask import Flask, render_template, request
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

if __name__ == '__main__':
    cargar_modelo()
    app.run(host='127.0.0.1', port=5000, debug=True)
