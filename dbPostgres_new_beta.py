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


class Table:
    def __init__(self, db_cursor, table_name: str):
        self._db_cursor = db_cursor
        self._table_name = table_name
        self._get_structure_of_table()
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
                  f"'{self._table_name}'"
        results = self.select(user_request=request, multi_result=True)
        self._is_created = results is not None
        self._structure = results

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
        spec = '*' if specific is None else specific
        cond = '' if condition is None else f' WHERE {condition}'
        _request = f"SELECT {spec} FROM public.{self._table_name}{cond}" if user_request is None else user_request
        rows: tuple = self._executor(request=_request)
        return self._rows_pars(rows=rows, multi_result=multi_result)

    @staticmethod
    def _rows_pars(rows, multi_result):
        """Статическая функция для парсинга полученных данных из DB

        Аргументы:

        - rows -- данные;
        - multi_result = False -- определяет вид возвращаемого значения, одно значение(по умолчанию);
        - multi_result = True -- определяет вид возвращаемого значения, множественный вывод.

        """
        if rows:
            if not multi_result:
                for row in rows:
                    for i in row:
                        return i  # вывод первого вхождения из кортежа и списка
            else:  # если множественный вывод
                if len(rows) == 1:  # если кортеж из одного элемента
                    return rows[0]  # избавляемся от кортежа и выводим список
                else:  # если кортеж из нескольких элементов
                    return rows  # выводим весь кортеж
        else:
            return None  # если данных не получили, выводим None

    def create(self, *name_columns, user_request: str=None):
        """Метод для создания таблицы. Таблица может быть создана только в случае если она не была создана ранее

        Аргументы:

        - *name_columns -- названия и тип данных колонок;
        - user_request -- определяет пользовательский запрос, шаблон не используется.

        Шаблон по умолчанию:

        CREATE TABLE IF NOT EXISTS public.{self._table_name} (*name_columns)

        """
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
        """Метод для внесения изменений в существующую таблицу

        Аргументы:

        - action -- изменение в таблице;
        - user_request -- определяет пользовательский запрос, шаблон не используется.

        Шаблон по умолчанию:

        ALTER TABLE {self._table_name} {action}"

        """

        request = f"ALTER TABLE {self._table_name} {action}" if user_request is None else user_request
        self._executor(request=request, read=False)
