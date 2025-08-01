from flask import Flask, request, jsonify
import secrets, string
from flask_cors import CORS # Importa CORS

app = Flask(__name__)
CORS(app)  # Habilita CORS para toda la aplicación
# CORS(app, origins=["http://dominio-seguro.com", "http://otro-dominio.com"])

# Genera contraseña segura
@app.route('/pwd', methods=['POST'])
def get_pwd():
    if request.is_json:
        new_user_data = request.get_json()
    else:
         new_user_data = request.form


    # Validar que los datos se hayan podido obtener y contengan lo necesario
    if not new_user_data:
        return jsonify({"error": "No se recibieron datos válidos (JSON o formulario)."}), 400

    cantidad = new_user_data.get('cantidad')
    pwd_length = new_user_data.get('pwd_length')
    use_num = new_user_data.get('use_num')
    use_caracterE = new_user_data.get('use_caracterE')

    if not cantidad or not pwd_length:
        return jsonify({"error": "Se requieren 'cantidad' y 'tamaño' de la contraseña."}), 400

    pwds = []
    cont = 0
    while True:
        if cont >= int(cantidad):
            break

        letras = string.ascii_letters
        if use_num == 'si':
            digitos = string.digits
        else:
            digitos = ''
        if use_caracterE == 'si':
            caracteres_especial = string.punctuation
        else:
            caracteres_especial = ''
        alfabeto = letras + digitos + caracteres_especial

        pwd = []
        for i in range(int(pwd_length)):
            pwd.append(secrets.choice(alfabeto))

        # Unir la lista de caracteres en una sola cadena al final
        pwds.append("".join(pwd))
        cont+=1

    return jsonify(pwds)

# Punto de entrada para ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True) # debug=True permite recarga automática y mensajes de error detallados