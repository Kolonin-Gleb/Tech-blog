# Для работы с БД
import pymysql
from pymysql.cursors import DictCursor

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

# Для получения тек. времени при публикации статьи
from datetime import datetime

now = datetime.now() # Получение тек. времени
id = 5
now = now.strftime('%Y-%m-%d %H:%M:%S')
print(now)
# Тест сохранениия времени в БД
try:
    with dbh.cursor() as cur:
        sql = f'INSERT INTO dt_test (id, dt) VALUES ("{id}", "{now}");'
        print(sql)
        cur.execute(sql)
    print("Данные добавлены в таблицу")
except:
    print("Ошибка добавления данных в таблицу")

# Тест получения времени из БД
# result = ''
# try:
#     with dbh.cursor() as cur:
#         sql = ('SELECT * FROM dt_test where id='+str(id))
#         print(sql)
#         cur.execute(sql)
#         result = cur.fetchall()
#         print("Данные получены из таблицы")
# except:
#     print("Ошибка получения данных из таблицы")

# # Перевод ответа в словарь
# result = result[0]
# print(result)

# # Получаю только время из ответа на запрос
# dt = result['dt']

# print(dt) # Теперь dt в формате времени библиотеки datetime

