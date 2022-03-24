# Для разработки сайта 
from flask import Flask
# Для получения и ответа на Ajax запросы в формате json
from flask import request, jsonify
# Для работы с БД
import pymysql
from pymysql.cursors import DictCursor

# Для получения тек. времени при публикации статьи
from datetime import datetime

# Основным файлом для работы с Flask будет файл app.py
# Папка static будет содержать неизменяемый JS и CSS
app = Flask(__name__, static_folder="static")

# Для конвертации времени из SQL в строку
# Настройки для соединения с БД.
conv = pymysql.converters.conversions.copy()
conv[12] = str # Конвертация формата времени получаемого из БД в строку, формат которой позволяет загрузить данные обратно в БД 

print("Просмотр кодов для настроек: \n")
print(conv)

# Установка соединения с БД
dbh = pymysql.connect(
        host='185.12.94.106',
        user='2p1s10',
        password='TOP SECRET. DO NOT HACK ME',
        db='2p1s10',
        charset='utf8mb4',
        cursorclass=DictCursor,
        autocommit=True,
        conv=conv # Добавление моих конвертеров при взаимодействии с БД
    )

# Запуск страниц сайта
@app.route('/home')
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
                    'author': author_data[0], # Сохранение всех данных о выбранном пользователе
                }
        except:
            out_data = {
                'status': 'error'
            }
    # Создание нового автора
    else:
        new_author = {
            'f': '',
            'i': '',
            'o': '',
            'id': 0
        }
        out_data = {
            'status': 'ok',
            'author': new_author,
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
                    'category': category_data[0], 
                }
        except:
            out_data = {
                'status': 'error'
            }
    # Создание новой категории
    else:
        new_category = {
            'category': '',
            'id': 0
        }
        out_data = {
            'status': 'ok',
            'category': new_category,
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
        sql = f"UPDATE blog_categories SET category='{category}' WHERE id={id}"
    else:
        sql = "INSERT INTO blog_categories (category)"
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

# Обработка запросов к странице articles #################################################

@app.route('/get_article_list')
def get_article_list():
    try:
        with dbh.cursor() as cur:
            # Получение всех данных из представления
            cur.execute('SELECT * FROM blog_articles_full')
            articles = cur.fetchall()
    except:
        articles = { 'error': 'Ошибка чтения статей' }

    return jsonify(articles)


@app.route('/get_article', methods=['POST'])
def get_article():
    out_data = {'status': 'error'}
    id = request.form.get('id') # получение id строчки категории из таблицы

    categories = ''
    # Взятие всех категорий из внешней таблицы
    try:
        with dbh.cursor() as cur:
            cur.execute('SELECT * FROM blog_categories')
            categories = cur.fetchall()
    except:
        out_data = {
            'status': 'error',
            'text': 'При загрузке всех категорий из внешней таблицы'
        }
        return jsonify(out_data)

    authors = ''
    # Взятие всех авторов из внешней таблицы
    try:
        with dbh.cursor() as cur:
            cur.execute('SELECT id, CONCAT_WS(" ", a.f, a.i, a.o) AS fio FROM blog_authors a')
            authors = cur.fetchall()
    except pymysql.Error as e: # Получение кода ошибки pymysql
        print("could not close connection error pymysql %d: %s" %(e.args[0], e.args[1]))
        out_data = {
            'status': 'error'
        }
        return jsonify(out_data)

    # Действия над существующей категорией
    if int(id) > 0:
        try:
            with dbh.cursor() as cur:
                # Получение данных о конкретной статье
                cur.execute('SELECT * FROM blog_articles_full WHERE id='+str(id))
                article_data = cur.fetchall()

                print("Полученные данные о конретной статье в виде словаря:")
                print(article_data[0])

                out_data = {
                    'status': 'ok',
                    # Передача данных о выбранной статье
                    'article': article_data[0],
                    # Передача данных о возможных категориях и авторах. Нужно для редактирования статьи
                    'categories': categories, # Возможные категории из внешней таблицы
                    'authors': authors, # Возможные авторы из внешней таблицы
                }
        except:
            out_data = {
                'status': 'error'
            }
    # Создание новой статьи
    else:
        print("Начало создание статьи с id" + str(id))
        now = datetime.now() # Получение тек. времени
        now = now.strftime('%Y-%m-%d %H:%M:%S') # Конвертация времени в формат DATETIME MySQL
        # В итоге now хранит время в формате 2021-12-26 08:41:28

        new_article = {
            'id': 0,
            'fio': '',
            'category': '',
            'title': '',
            'article': '',
            'dt': now,
        }
        out_data = {
            'status': 'ok',
            'article': new_article, # Передача данных о новой статье с значениями по умолчанию
            # Передача данных о возможных категориях и авторах. Необходимо для выбора при редактировании
            'categories': categories,
            'authors': authors
        }
    return jsonify(out_data)


@app.route('/delete_article', methods=['POST'])
def delete_article():
    out_data = {'status': 'error'}
    id = request.form.get('id')

    if int(id) > 0:
        try:
            with dbh.cursor() as cur:
                cur.execute('DELETE FROM blog_articles WHERE id = '+str(id))
                out_data = {
                    'status': 'ok',
                }
        except:
            out_data = {
                'status': 'error'
            }

    return jsonify(out_data)


@app.route('/save_article', methods=['POST'])
def save_article():
    # Получение данных data с помощью библ. request
    id = int(request.form.get('id'))
    fio = str(request.form.get('fio')) #TODO: переименовать в fio_id или author_id
    category = str(request.form.get('category')) #TODO: переименовать в category_id
    title = str(request.form.get('title'))
    article = str(request.form.get('article'))
    dt = str(request.form.get('dt'))

    print("Данные полученные с фронтенда для сохранения в БД: \n")
    print(f"{id}, {fio}, {category}, {title}, {article}, {dt}")

    # Обновление таблицы статей
    sql = ''
    if id > 0:
        sql  = f"UPDATE blog_articles SET category_id='{category}', author_id={fio}, "
        sql += f"title='{title}', article='{article}', dt='{dt}' "
        sql += f"WHERE id={id}"
    else:
        sql = "INSERT INTO blog_articles (category_id, author_id, title, article, dt)"
        sql += f" VALUE ('{fio}', '{category}', '{title}', '{article}', '{dt}')"

    # Попытка выполнить sql
    print("SQL запрос для выполнения: \n")
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
app.run(debug = True, host='db-learning.ithub.ru', port=1177)

# Запуск приложения на локальном пк
# app.run(debug=True)
