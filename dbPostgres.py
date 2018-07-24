import os
import psycopg2
import datetime

on_heroku = False
if 'HEROKU_RUN' in os.environ:
  on_heroku = True

conn = psycopg2.connect(database='dahhjum5mbqggk', user='mpczhjgpnwsbrc', password='a3d54f288147f39ff9fe809a20018bf6ca984043934768581f3964f0299f7b47', host='ec2-54-163-234-99.compute-1.amazonaws.com', port='5432', sslmode='require') if on_heroku else psycopg2.connect(database='test', user='pyParser', password='pyParser', host='localhost', port='5432')
#conn = psycopg2.connect(database='test', user='pyParser', password='pyParser', host='localhost', port='5432')
#conn = psycopg2.connect(database='dahhjum5mbqggk', user='mpczhjgpnwsbrc', password='a3d54f288147f39ff9fe809a20018bf6ca984043934768581f3964f0299f7b47', host='ec2-54-163-234-99.compute-1.amazonaws.com', port='5432', sslmode='require')
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

def create(table, *args):
    text = "CREATE TABLE IF NOT EXISTS %s (" % (table)
    for num, i in enumerate(args, start=1):
        text += '%s' % i
        if num != args.__len__():
            text += ', '
    text += ")"
    # Make the changes to the database persistent
    db.execute(text)
    conn.commit()


def select(table: str, specific: str=None, condition: str=None):
    if specific is None:
        spec = '*'
    else:
        spec = specific
    #if condition is None:
    #    cond = ''
    #else:
    #    cond = ' WHERE %s' % condition
    db.execute("SELECT %s FROM %s %s" % (spec, table, condition))
    rows = db.fetchall()
    return rows

    #conn.commit()


'''
def create():
    text = "CREATE TABLE IF NOT EXISTS public.calendarSamara\
(\
    datetimemeasure timestamp without time zone,\
    mor_min integer,\
    mor_max integer,\
    mor_cond_cloud character varying COLLATE pg_catalog.\"default\",\
    mor_presure integer,\
    mor_humidity integer,\
    mor_feeling integer,\
    day_min integer,\
    day_max integer,\
    day_cond_cloud character varying COLLATE pg_catalog.\"default\",\
    day_presure integer,\
    day_humidity integer,\
    day_feeling integer,\
    eve_min integer,\
    eve_max integer,\
    eve_cond_cloud character varying COLLATE pg_catalog.\"default\",\
    eve_presure integer,\
    eve_humidity integer,\
    eve_feeling integer,\
    ngh_min integer,\
    ngh_max integer,\
    ngh_cond_cloud character varying COLLATE pg_catalog.\"default\",\
    ngh_presure integer,\
    ngh_humidity integer,\
    ngh_feeling integer,\
    datetimerecord timestamp with time zone DEFAULT now() \
    )"
    #ps = db.prepare(text)
    #ps()
    db.execute(text)
    text = "CREATE TABLE IF NOT EXISTS public.currentSamara\
    (\
        temperature integer,\
        cond_cloud character varying COLLATE pg_catalog.\"default\",\
        feels integer,\
        presure integer,\
        humidity integer,\
        datetimerecord timestamp with time zone DEFAULT now() \
        )"
    # Make the changes to the database persistent
    db.execute(text)

    conn.commit()

    # Close communication with the database
    #db.close()
    #conn.close()


def update(table, nameColum:str, value, condition=None):
    if type(value) is str:
        str_pole = "%s" % nameColum + " = \'%s\'" % value
    else:
        str_pole = "%s" % nameColum + " = %s" % value
    if condition is None:
        request = "UPDATE %s" % table + " SET " + str_pole
    else:
        request = "UPDATE %s" % table + " SET " + str_pole + " WHERE " + condition
    ps = db.prepare(request)
    ps()





def select_max(table: str, specific: str):
    if specific is None:
        spec = '*'
    else:
        spec = specific
    ps = db.query("SELECT MAX (%s) FROM %s" % (spec, table))
    return ps
'''