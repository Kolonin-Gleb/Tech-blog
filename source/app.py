# Для разработки сайта 
from flask import Flask
# Для получения и ответа на Ajax запросы в формате json
from flask import request, jsonify
# Для работы с БД
import pymysql
from pymysql.cursors import DictCursor

# Для получения времени публикации статьи
# from datetime import datetime
# Для пагинации
# from flask import render_template, redirect
# from flask import url_for # Используется в других файлах

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
    
# Запуск страниц сайта
@app.route('/')
def main_page():
    html = open("index.html", "r")
    page = html.read()
    html.close()
    return page

@app.route('/authors')
def authors_page():
    html = open("authors.html", "r")
    page = html.read()
    html.close()
    return page

@app.route('/categories')
def categories_page():
    html = open("categories.html", "r")
    page = html.read()
    html.close()
    return page

@app.route('/articles')
def articles_page():
    html = open("articles.html", "r")
    page = html.read()
    html.close()
    return page

# Обработка запросов к странице authors #################################################

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
                author_data = cur.fetchall()
                out_data = {
                    'status': 'ok', # Установка статуса, что опреация выполнена успешно. # Нужно для работы JS функций
                    'user': author_data[0], # Сохранение всех данных о выбранном пользователе
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
        sql += f" VALUES('{f}','{i}','{o}')"

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

# Обработка запросов к странице categories #################################################

@app.route('/get_category_list')
def get_category_list():
    try:
        with dbh.cursor() as cur:
            cur.execute('SELECT * FROM blog_categories')
            categories = cur.fetchall()
    except:
        categories = { 'error': 'Ошибка чтения таблицы авторов' }

    return jsonify(categories)


@app.route('/get_category', methods=['POST'])
def get_category():
    out_data = {'status': 'error'}
    id = request.form.get('id') # получение id строчки категории из таблицы

    # Действия над существующей категорией
    if int(id) > 0:
        try:
            with dbh.cursor() as cur:
                # Получение данных из таблицы о категории
                cur.execute('SELECT * FROM blog_categories WHERE id='+str(id))
                category_data = cur.fetchall()
                out_data = {
                    'status': 'ok',
                    'user': category_data[0], 
                }
        except:
            out_data = {
                'status': 'error'
            }
    # Создание новой категории
    else:
        u = {
            'category': '',
            'id': 0
        }
        out_data = {
            'status': 'ok',
            'user': u,
        }
    return jsonify(out_data)


@app.route('/delete_category', methods=['POST'])
def delete_category():
    out_data = {'status': 'error'}
    id = request.form.get('id')

    if int(id) > 0:
        try:
            with dbh.cursor() as cur:
                cur.execute('DELETE FROM blog_categories WHERE id = '+str(id))
                out_data = {
                    'status': 'ok',
                }
        except:
            out_data = {
                'status': 'error'
            }

    return jsonify(out_data)


# Эта функция сохраняет данные формы
@app.route('/save_category', methods=['POST'])
def save_category():
    # Получение данных data с помощью библ. request
    id = int(request.form.get('id'))
    category = request.form.get('category')

    # Проверка получения данных
    print(f"{id}, {category}")

    sql = ''
    if id > 0:
        sql = f"UPDATE blog_categories SET name='{category}' WHERE id={id}"
    else:
        sql = "INSERT INTO blog_categories (name)"
        sql += f" VALUE ('{category}')"

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
