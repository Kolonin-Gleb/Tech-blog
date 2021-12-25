# Для разработки сайта и пагинации
from flask import Flask, render_template, redirect
# Для получения и ответа на Ajax запросы в формате json
from flask import request, jsonify
# Для работы с БД
import pymysql
from pymysql.cursors import DictCursor

# from flask import url_for # Используется в других файлах
# from datetime import datetime

# Основным файлом для работы с Flask будет файл app.py
# Папка static будет содержать неизменяемый JS и CSS
app = Flask(__name__, static_folder="static")

# Установка соединения с БД
dbh = pymysql.connect(
        host='185.12.94.106',
        user='2p1s10',
        password='404-086-366',
        db='2p1s10',
        charset='utf8mb4',
        cursorclass=DictCursor,
        autocommit=True
    )

@app.route('/')
def index():
    index = open("index.html", "r")
    page = index.read()
    index.close()
    return page


@app.route('/get_author_list')
def get_author_list():
    try:
        with dbh.cursor() as cur:
            cur.execute('SELECT * FROM blog_authors')
            authors = cur.fetchall()
    except:
        authors = { 'error': 'Ошибка чтения таблицы авторов' }

    return jsonify(authors)


@app.route('/get_author', methods=['POST'])
def get_author():
    out_data = {'status': 'error'}
    id = request.form.get('id') # получение id строчки контакта из таблицы

    # Действия над существующим автором
    if int(id) > 0:
        try:
            with dbh.cursor() as cur:
                # Получение данных из таблицы об авторе
                cur.execute('SELECT * FROM blog_authors WHERE id='+str(id))
                contact_data = cur.fetchall()
                out_data = {
                    'status': 'ok', # Установка статуса, что опреация выполнена успешно. # Нужно для работы JS функций
                    'user': contact_data[0], # Сохранение всех данных о выбранном пользователе
                }
        except:
            out_data = {
                'status': 'error'
            }
    # Создание нового автора
    else:
        u = {
            'f': '',
            'i': '',
            'o': '',
            'id': 0
        }
        out_data = {
            'status': 'ok',
            'user': u,
        }
    return jsonify(out_data)


@app.route('/delete_author', methods=['POST'])
def delete_author():
    out_data = {'status': 'error'}
    id = request.form.get('id')

    if int(id) > 0:
        try:
            with dbh.cursor() as cur:
                cur.execute('DELETE FROM blog_authors WHERE id = '+str(id))
                out_data = {
                    'status': 'ok',
                }
        except:
            out_data = {
                'status': 'error'
            }

    return jsonify(out_data)


# Эта функция сохраняет данные формы
@app.route('/save_author', methods=['POST'])
def save_author():
    # Получение данных data с помощью библ. request
    id = int(request.form.get('id'))
    f = request.form.get('f')
    i = request.form.get('i')
    o = request.form.get('o')

    # Проверка получения данных
    print(f"{id}, {f}, {i}, {o}")

    sql = ''
    if id > 0:
        sql = f"UPDATE blog_authors SET f='{f}', i='{i}', o='{o}' WHERE id={id}"
    else:
        sql = "INSERT INTO blog_authors (f, i, o)"

    # Попытка выполнить sql
    print(sql)
    try:
        with dbh.cursor() as cur:
            cur.execute(sql)
            out_data = {
                'status': 'ok'
            }
    except:
        out_data = {
            'status': 'error'
        }

    return jsonify(out_data)

# Запуск приложения на сервере колледжа
app.run(debug = True, host='db-learning.ithub.ru', port=1110)

# Запуск приложения на локальном пк
# app.run(debug=True)
