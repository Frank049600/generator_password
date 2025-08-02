from flask import Flask, request, jsonify, render_template
import secrets, string
from flask_cors import CORS


app = Flask(__name__)

CORS(app)  # Esto habilitará CORS para todas las rutas y orígenes
# Datos de ejemplo (en una aplicación real, esto vendría de una base de datos)
users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"}
]
next_id = 3 # Para asignar IDs a nuevos usuarios

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
    return render_template('index.html')

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

# Ruta para obtener todos los usuarios (GET /users)
@app.route('/users', methods=['GET'])
def get_users():
    # return render_template('index.html', mensaje=users)
    return jsonify(users)

# Ruta para obtener un usuario por ID (GET /users/<id>)
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({"error": "Usuario no encontrado"}), 404

# Ruta para agregar un nuevo usuario (POST /users)
@app.route('/users', methods=['POST'])
def add_user():
    global next_id
    if request.is_json:
        new_user_data = request.get_json()
    else:
         new_user_data = request.form


    # Validar que los datos se hayan podido obtener y contengan lo necesario
    if not new_user_data:
        return jsonify({"error": "No se recibieron datos válidos (JSON o formulario)."}), 400

    name = new_user_data.get('name')
    email = new_user_data.get('email')

    if not name or not email:
        return jsonify({"error": "Se requieren 'name' y 'email'."}), 400

    new_user = {
        "id": next_id,
        "name": name,
        "email": email
    }
    users.append(new_user)
    next_id += 1
    return jsonify(new_user), 201 # 201 Created

# Ruta para actualizar un usuario (PUT /users/<id>)
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    if not request.is_json:
        return jsonify({"error": "El contenido debe ser JSON"}), 400

    update_data = request.get_json()
    if 'name' in update_data:
        user['name'] = update_data['name']
    if 'email' in update_data:
        user['email'] = update_data['email']
    return jsonify(user)

# Ruta para eliminar un usuario (DELETE /users/<id>)
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users
    initial_len = len(users)
    users = [u for u in users if u['id'] != user_id]
    if len(users) < initial_len:
        return jsonify({"message": "Usuario eliminado"}), 204 # 204 No Content
    return jsonify({"error": "Usuario no encontrado"}), 404

# Punto de entrada para ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True) # debug=True permite recarga automática y mensajes de error detallados