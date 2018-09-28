import os
import psycopg2
import datetime
import timeit

on_heroku = False
if 'HEROKU_RUN' in os.environ:
    on_heroku = True

conn = psycopg2.connect(database='dahhjum5mbqggk', user='mpczhjgpnwsbrc',
                        password='a3d54f288147f39ff9fe809a20018bf6ca984043934768581f3964f0299f7b47',
                        host='ec2-54-163-234-99.compute-1.amazonaws.com', port='5432', sslmode='require') if on_heroku \
    else psycopg2.connect(database='test', user='pyParser', password='pyParser', host='localhost', port='5432')
db = conn.cursor()


'''
Host - ec2-54-163-234-99.compute-1.amazonaws.com
Database - dahhjum5mbqggk
User - mpczhjgpnwsbrc
Port - 5432
Password - a3d54f288147f39ff9fe809a20018bf6ca984043934768581f3964f0299f7b47
URI - postgres://mpczhjgpnwsbrc:a3d54f288147f39ff9fe809a20018bf6ca984043934768581f3964f0299f7b47@ec2-54-163-234-99.compute-1.amazonaws.com:5432/dahhjum5mbqggk
Heroku CLI - heroku pg:psql postgresql-rectangular-42119 --app lolitaapp
'''


def insert(table, *args, nameCol=None):
    request = ''
    for num, i in enumerate(args, start=1):
        if type(i) is list:
            for num1, y in enumerate(i, start=1):
                if type(y) is int:
                    request = request + '%s' % y
                elif type(y) is str:
                    request = request + "\'%s\'" % y
                elif type(y) is bool:
                    request = request + '%s' % y
                elif type(y) is datetime.datetime:
                    request = request + '%s' % y.strftime("TIMESTAMP\'%Y-%m-%d %H:%M:%S\'")
                elif type(y) is datetime.date:
                    request = request + '%s' % y.strftime("DATE\'%Y-%m-%d\'")
                if num1 != i.__len__():
                    request = request + ', '
        else:
            if type(i) is int:
                request = request + '%s' % i
            elif type(i) is str:
                request = request + "\'%s\'" % i
            elif type(i) is bool:
                request = request + '%s' % i
            elif type(i) is datetime.datetime:
                request = request + '%s' % i.strftime("TIMESTAMP\'%Y-%m-%d %H:%M:%S\'")
            elif type(i) is datetime.date:
                request = request + '%s' % i.strftime("DATE\'%Y-%m-%d\'")
            if num != args.__len__():
                request = request + ', '
    if nameCol is None:
        db.execute("INSERT INTO %s VALUES (%s)" % (table, request))
    else:
        db.execute("INSERT INTO %s (%s) VALUES (%s)" % (table, nameCol, request))
    conn.commit()


class Table:
    def __init__(self, db_cursor, table_name: str):
        self._db_cursor = db_cursor  # Передаем курсор для проведение операций с базой данных.
        self._table_name = table_name  # Имя таблицы в базе данных.
        self._get_structure_of_table()  # Запуск метода получения/обновления структуры таблицы базы данных.
        #
        # Structure of record -- dict:
        # {temp: (2, 5), condition: 'sun', pressure: 79, wind: (6.9, 'west'), feeling_temp: 6}
        #
        self.last_day_mor = None
        self.last_day_day = None
        self.last_day_evn = None
        self.last_day_ngh = None

    def get_count_of_records(self):
        """Метод получения колличества записей в таблице"""
        return self.select(specific='COUNT(*)')

    def _get_structure_of_table(self):
        """Метод получения структуры таблицы"""

        request = f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = " \
                  f"'{self._table_name}'"  # Формируется пользовательский запрос на получения структуры таблицы.
        results = self.select(user_request=request, multi_result=True)  # Метод Select с пользовательским запросом.
        self._is_created = results is not None  # Если структура пустая, то считаем таблицу не существующей.
        self._structure = results  # Сохраняем/обновляем структуру таблицы.

    def _executor(self, request, read: bool=True):
        """Метод для выполнения запросов на чтение и запись.

        Аргументы:

        - read = True -- определяет запрос на чтение (по умолчанию);
        - read = False -- определяет запрос на запись.

        """
        self._db_cursor.execute(request)
        if read:
            return self._db_cursor.fetchall()
        else:
            self._db_cursor.connection.commit()
            return True

    def select(self, specific: str=None, condition: str=None, user_request: str=None, multi_result: bool=False):
        """Метод запроса "Select" из базы данных.

        Аргументы:

        - user_request -- определяет пользовательский запрос, шаблон не используется;
        - specific -- определяет столбцы для запроса;
        - condition -- дополнительное условие;
        - multi_result = False -- определяет вид возвращаемого значения, одно значение(по умолчанию);
        - multi_result = True -- определяет вид возвращаемого значения, множественный вывод.

        По умолчанию выполняет запрос шаблонного вида:

        SELECT {spec} FROM public.{self._table_name}{cond}

        """
        spec = '*' if specific is None else specific  # если столбцы не определенны, формирует запрос всех (*)
        cond = '' if condition is None else f' WHERE {condition}'  # если условие не определенно, условие не формируется
        _request = f"SELECT {spec} FROM public.{self._table_name}{cond}" if user_request is None else user_request
        rows: tuple = self._executor(request=_request)
        if rows:  # если данные есть
            if not multi_result:  # если одиночный вывод
                for row in rows:
                    for i in row:
                        results = i  # вывод первого вхождения из кортежа и списка
                        break
                    break
                return results
            else:  # если множественный вывод
                if len(rows) == 1:  # если кортеж из одного элемента
                    results = rows[0]  # избавляемся от кортежа и выводим список
                else:  # если кортеж из нескольких элементов
                    results = rows  # выводим весь кортеж
                return results
        else:
            return None  # если данных не получили, выводим None

    def create(self, *name_columns, user_request: str=None):
        """Метод для создания таблицы. Таблица может быть создана только в случае если она не была создана ранее"""

        if not self._is_created:
            request = f"CREATE TABLE IF NOT EXISTS public.{self._table_name} ("
            for num, i in enumerate(name_columns, start=1):
                request += f'{i}'
                if num != name_columns.__len__():
                    request += ', '
            request += ")"
            request = request if user_request is None else user_request
            results = self._executor(request=request, read=False)
            self._get_structure_of_table()
            return results
        else:
            return False

    def alter(self, action: str, user_request: str=None):
        request = f"ALTER TABLE {self._table_name} {action}" if user_request is None else user_request
        self._executor(request=request, read=False)


def update(table, nameColum: str, value, condition=None):
    if type(value) is str:
        str_pole = "%s" % nameColum + " = \'%s\'" % value
    else:
        str_pole = "%s" % nameColum + " = %s" % value
    if condition is None:
        request = "UPDATE %s" % table + " SET " + str_pole
    else:
        request = "UPDATE %s" % table + " SET " + str_pole + ", timestamp_record=now() WHERE " + condition
    db.execute(request)
    conn.commit()


def alter(table, nameAndTypeColum: str, properties: str = None):
    if properties is None:
        text = "ALTER TABLE %s ADD COLUMN IF NOT EXISTS %s" % (table, nameAndTypeColum)
    else:
        text = "ALTER TABLE %s ADD COLUMN IF NOT EXISTS %s %s" % (table, nameAndTypeColum, properties)
    try:
        db.execute(text)
        conn.commit()
    except:
        conn.commit()
