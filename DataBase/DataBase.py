from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
import bcrypt
import sqlite3

app = Flask(__name__)

# Конфигурация JWT
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
jwt = JWTManager(app)

# Функция для подключения к базе данных
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Регистрация пользователя
# Регистрация пользователя
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    first_name = data.get('first_name')
    last_name = data.get('last_name')
    patronymic = data.get('patronymic', None)  # Отчество может быть NULL
    login = data.get('login')
    password = data.get('password')
    email = data.get('email')

    if not first_name or not last_name or not login or not password or not email:
        return jsonify({"error": "All fields (first_name, last_name, login, password, email) are required"}), 400

    # Хеширование пароля
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    conn = get_db_connection()
    cursor = conn.cursor()

    # Проверка на уникальность логина и email
    cursor.execute("SELECT * FROM users WHERE login = ? OR email = ?", (login, email))
    user = cursor.fetchone()

    if user:
        return jsonify({"error": "User with this login or email already exists"}), 400

    # Добавление нового пользователя в базу данных
    cursor.execute('''INSERT INTO users 
                      (first_name, last_name, patronymic, login, password, role, points, email, isDelete)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                   (first_name, last_name, patronymic, login, hashed_password, 'Пользователь', 0, email, 0))

    conn.commit()
    conn.close()

    return jsonify({"message": "User registered successfully"}), 201

# Логин пользователя
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    login = data.get('login')
    password = data.get('password')

    if not login or not password:
        return jsonify({"error": "Login and password are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Поиск пользователя по логину
    cursor.execute("SELECT * FROM users WHERE login = ?", (login,))
    user = cursor.fetchone()

    conn.close()

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        # Создание JWT токенов с ролью пользователя
        access_token = create_access_token(identity=user['login'], additional_claims={"role": user['role']})
        refresh_token = create_refresh_token(identity=user['login'], additional_claims={"role": user['role']})

        return jsonify({
            "access_token": access_token,
            "refresh_token": refresh_token
        })

    return jsonify({"error": "Invalid login or password"}), 401

# Пример защищённого маршрута с проверкой роли
@app.route('/admin', methods=['GET'])
@jwt_required()
def admin_route():
    # Извлекаем данные о текущем пользователе
    current_user = get_jwt_identity()
    role = get_jwt_identity().get("role", "")

    # Проверка роли пользователя
    if role != 'admin':
        return jsonify({"error": "Access forbidden: you are not an admin"}), 403

    return jsonify({"message": f"Hello {current_user}, you have admin access!"}), 200

@app.route('/add_category', methods=['POST'])
@jwt_required()  # Проверка наличия валидного JWT
def add_category():
    # Получаем данные из запроса
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    # Проверка, что все поля заполнены
    if not name or not description:
        return jsonify({"error": "Name and description are required"}), 400

    # Подключаемся к базе данных
    conn = get_db_connection()
    cursor = conn.cursor()

    # Проверка на уникальность названия категории
    cursor.execute("SELECT * FROM categories WHERE name = ?", (name,))
    existing_category = cursor.fetchone()
    if existing_category:
        conn.close()
        return jsonify({"error": "Category with this name already exists"}), 400

    # Получаем роль пользователя из токена
    current_user = get_jwt_identity()
    role = get_jwt_identity().get("role", "")

    # Проверка, что роль пользователя 'admin'
    if role != 'Администратор':
        conn.close()
        return jsonify({"error": "Access forbidden: you are not an admin"}), 403

    # Запись новой категории в базу данных
    cursor.execute('''INSERT INTO categories (name, description, isDelete) 
                      VALUES (?, ?, ?)''', (name, description, 0))
    
    # Сохраняем изменения
    conn.commit()
    conn.close()

    return jsonify({"message": "Category added successfully"}), 201


from flask_jwt_extended import get_jwt_identity

@app.route('/user_info', methods=['GET'])
@jwt_required()
def user_info():
    # Извлекаем данные пользователя из токена
    current_user = get_jwt_identity()
    role = get_jwt_identity().get("role", "user")  # Если роль не указана, по умолчанию будет 'user'

    return jsonify({
        "user": current_user,
        "role": role
    })

# Основная точка входа
if __name__ == '__main__':
    app.run(debug=True)
