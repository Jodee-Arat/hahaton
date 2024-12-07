import sqlite3
import bcrypt

# Функция для подключения к базе данных
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Создание базы данных и таблиц
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Создание таблицы пользователей
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    patronymic TEXT,
                    login TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL,
                    points INTEGER DEFAULT 0,
                    email TEXT UNIQUE NOT NULL,
                    isDelete INTEGER DEFAULT 0)''')

# Создание таблицы категорий
cursor.execute('''CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT NOT NULL,
                    isDelete INTEGER DEFAULT 0)''')

# Создание таблицы избранных категорий
cursor.execute('''CREATE TABLE IF NOT EXISTS favorite_categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    category_id INTEGER NOT NULL,
                    isDelete INTEGER DEFAULT 0,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (category_id) REFERENCES categories(id))''')

# Создание таблицы мероприятий
cursor.execute('''CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    status INTEGER NOT NULL,
                    description TEXT NOT NULL,
                    start_date TEXT NOT NULL,
                    end_date TEXT NOT NULL,
                    coordinates TEXT NOT NULL,
                    max_participants INTEGER NOT NULL,
                    isDelete INTEGER DEFAULT 0,
                    FOREIGN KEY (category_id) REFERENCES categories(id))''')

# Создание таблицы новостей
cursor.execute('''CREATE TABLE IF NOT EXISTS news (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    category_id INTEGER NOT NULL,
                    text BLOB NOT NULL,
                    release_date TEXT NOT NULL,
                    isDelete INTEGER DEFAULT 0,
                    FOREIGN KEY (event_id) REFERENCES events(id),
                    FOREIGN KEY (category_id) REFERENCES categories(id))''')

# Создание таблицы участника мероприятия
cursor.execute('''CREATE TABLE IF NOT EXISTS event_participants (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    event_id INTEGER NOT NULL,
                    role TEXT NOT NULL,
                    attended INTEGER,
                    isDelete INTEGER DEFAULT 0,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (event_id) REFERENCES events(id))''')

# Создание таблицы изображений
cursor.execute('''CREATE TABLE IF NOT EXISTS images (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    news_id INTEGER,
                    product_id INTEGER,
                    image_path TEXT NOT NULL,
                    order_number INTEGER NOT NULL,
                    isDelete INTEGER DEFAULT 0,
                    FOREIGN KEY (news_id) REFERENCES news(id),
                    FOREIGN KEY (product_id) REFERENCES products(id))''')

# Создание таблицы товаров
cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT NOT NULL,
                    price INTEGER NOT NULL,
                    acquisition_method TEXT,
                    isDelete INTEGER DEFAULT 0)''')

# Создание таблицы истории покупок
cursor.execute('''CREATE TABLE IF NOT EXISTS purchase_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    isDelete INTEGER DEFAULT 0,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (product_id) REFERENCES products(id))''')

# Создание таблицы комментариев
cursor.execute('''CREATE TABLE IF NOT EXISTS comments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    text TEXT NOT NULL,
                    write_date TEXT NOT NULL,
                    isDelete INTEGER DEFAULT 0,
                    FOREIGN KEY (user_id) REFERENCES users(id))''')

# Создание таблицы отзывов
cursor.execute('''CREATE TABLE IF NOT EXISTS reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    rating INTEGER NOT NULL,
                    text TEXT NOT NULL,
                    write_date TEXT NOT NULL,
                    isDelete INTEGER DEFAULT 0,
                    FOREIGN KEY (user_id) REFERENCES users(id))''')

# Создание таблицы опросов
cursor.execute('''CREATE TABLE IF NOT EXISTS surveys (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    manager_id INTEGER NOT NULL,
                    rating INTEGER NOT NULL,
                    text TEXT NOT NULL,
                    start_date TEXT NOT NULL,
                    end_date TEXT NOT NULL,
                    isDelete INTEGER DEFAULT 0,
                    FOREIGN KEY (manager_id) REFERENCES users(id))''')

# Создание таблицы вариантов ответов
cursor.execute('''CREATE TABLE IF NOT EXISTS survey_answers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    survey_id INTEGER NOT NULL,
                    answer_option TEXT NOT NULL,
                    vote_count INTEGER NOT NULL,
                    isDelete INTEGER DEFAULT 0,
                    FOREIGN KEY (survey_id) REFERENCES surveys(id))''')

conn.commit()

# Функция для добавления администратора
def add_admin():
    # Данные администратора
    admin_login = "admin"
    admin_password = "1"  # Используйте более безопасный пароль
    admin_email = "admin@mail.ru"

    # Хеширование пароля администратора
    hashed_password = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt())

    # Подключаемся к базе данных
    conn = get_db_connection()
    cursor = conn.cursor()

    # Проверка на наличие администратора
    cursor.execute("SELECT * FROM users WHERE login = ?", (admin_login,))
    user = cursor.fetchone()

    if user:
        print("Администратор уже существует!")
    else:
        # Добавление администратора в базу данных
        cursor.execute('''INSERT INTO users 
                          (first_name, last_name, patronymic, login, password, role, points, email, isDelete)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                       ("Администратор", "Админов", None, admin_login, hashed_password, 'Администратор', 0, admin_email, 0))

        conn.commit()
        print("Администратор успешно добавлен!")

    conn.close()

# Запускаем функцию для добавления администратора
add_admin()

# Закрываем соединение с базой данных
conn.close()
