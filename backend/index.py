from flask import Flask, render_template, request
from cargarModelo import cargar_modelo
# Variable creamos un objeto con el nombre del archivo
app = Flask(__name__)

# Definimos un metodo para poder procesar una peticion desde el navegador 
# http://localhost:5000/
@app.route('/')
def inicio():
    return f'Hola mundo desde Flask! {request.path}'


if __name__ == '__main__':
    cargar_modelo()
    app.run(host='127.0.0.1', port=5000, debug=True)
