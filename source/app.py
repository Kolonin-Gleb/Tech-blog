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


# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db' #Установка бд sqlite с которой будет вестись работа
# #blog.db - название БД
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)


# # Класс для манипуляции с БД
# class Article(db.Model):
#     # Создание полей БД
#     id = db.Column(db.Integer, primary_key=True) # поле id, что может хранить только целые числа
#     title = db.Column(db.String(100), nullable=False)
#     intro = db.Column(db.String(300), nullable=False)
#     text = db.Column(db.Text, nullable=False)
#     date = db.Column(db.DateTime, default=datetime.utcnow) # По умолч. время создания статьи - текущее

#     # Метод возвращающий объект и его id
#     def __repr__(self):
#         return '<Article %r>' % self.id

@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

# @app.route('/posts')
# def posts():
#     articles = Article.query.order_by(Article.date.desc()).all() # Создание списка всех данных из бд отсортированных по дате
#     return render_template("posts.html", articles=articles) # Передача шаблона и списка данных из бд

# #Переход на конкретную статью
# @app.route('/posts/<int:id>')
# def post_detail(id):
#     article = Article.query.get(id) # Получение статьи с заданным id
#     return render_template("post_detail.html", article=article) # Передача шаблона и списка данных из бд

# #Переход на удаление статьи
# @app.route('/posts/<int:id>/del')
# def post_delete(id):
#     article = Article.query.get_or_404(id) # Получение статьи с заданным id из бд

#     try:
#         db.session.delete(article)
#         db.session.commit()
#         return redirect('/posts')
#     except:
#         return "Ошибка удаления статьи"

# #Переход на редактирование статьи
# @app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
# def post_update(id):
#     article = Article.query.get_or_404(id)

#     if request.method == 'POST':  # Если идёт добавление данных
#         # Внесение изменений в объект в бд
#         article.title = request.form['title']
#         article.intro = request.form['intro']
#         article.text = request.form['text']

#         try:
#             db.session.commit()
#             return redirect('/posts')
#         except:
#             return "Ошибка редактирования статьи"
#     else:
#         return render_template("post_update.html", article=article)  # Передача шаблона и списка данных из бд


# @app.route('/create-article', methods=['POST', 'GET']) # Для обработки POST и GET запросов
# def create_article():
#     if request.method == 'POST': # Если идёт добавление данных
#         # Сохранение данных из формы в переменные
#         title = request.form['title']
#         intro = request.form['intro']
#         text = request.form['text']

#         # Создание объекта, что будет добавляться в БД
#         article = Article(title=title, intro=intro, text=text)

#         try:
#             db.session.add(article) # Нет необходимости в SQL запросе
#             db.session.commit()
#             return redirect('/posts') # Перенаправление пользователя
#         except:
#             return "Ошибка добавления статьи"
#     else: # Если идёт простое отображение данных
#         return render_template("create-article.html")

# Запуск приложения на сервере колледжа
# app.run(debug = True, host='db-learning.ithub.ru', port=1110)

# Запуск приложения на локальном пк
app.run(debug=True) # Режим debug следует включить при разработке для того, чтобы видеть ошибки
