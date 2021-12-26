# Для получения тек. времени при публикации статьи
# from datetime import datetime, time

# now = datetime.utcnow()
# print(now)
# now = f"{now.year} {now.month} {now.day} {now.hour} {now.minute}"
# print(now)
# print(type(now))

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
id = 2
now = now.strftime('%Y-%m-%d %H:%M:%S')
print(now)

try:
    with dbh.cursor() as cur:
        sql = f'INSERT INTO dt_test (id, dt) VALUES ("{id}", "{now}");'
        print(sql)
        cur.execute(sql)
    print("Данные добавлены в таблицу")
except:
    print("Ошибка добавления данных в таблицу")

