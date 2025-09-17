from flask import Flask, request, jsonify, render_template
import secrets, string, os
from flask_cors import CORS


app = Flask(__name__)

CORS(app)  # Esto habilitará CORS para todas las rutas y orígenes
# Datos de ejemplo (en una aplicación real, esto vendría de una base de datos)
users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"}
]
next_id = 3 # Para asignar IDs a nuevos usuarios

name_server = os.environ.get('server_name', 'default_value')

# Function to validate the password
def password_check(passwd, pwd_length, use_num, use_caracterE):
    SpecialSym =['$', '@', '#', '%']
    val = True
    # Valida tamañao
    if len(passwd) < int(pwd_length) or len(passwd) > int(pwd_length):
        val = False

    # Valida que tenga mayusculas
    if not any(char.isupper() for char in passwd):
        val = False

    # Valida que tenga minusculas
    if not any(char.islower() for char in passwd):
        val = False

    # Valida que tenga números
    if use_num == 'si':
        if not any(char.isdigit() for char in passwd):
            val = False

    # Valida que tenga caracteres especiales
    if use_caracterE == 'si':
        if not any(char in SpecialSym for char in passwd):
            val = False
    if val:
        return val

# Renderiza la página principal
@app.route('/')
def home():
    return render_template('index.html', name_server=name_server)

# Ruta para generar contraseñas seguras
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

        # valida contraseñas
        if password_check("".join(pwd), pwd_length, use_num, use_caracterE):
            # Unir la lista de caracteres en una sola cadena al final
            pwds.append("".join(pwd))
        else:
            continue
        cont+=1

    return jsonify(pwds)

# Punto de entrada para ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True) # debug=True permite recarga automática y mensajes de error detallados