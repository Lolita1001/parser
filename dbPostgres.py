import postgresql
#import classes
import datetime

db = postgresql.open('pq://pyParser:pyParser@localhost:5432/test')

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
                if num1 != i.__len__():
                    request = request + ', '
        else:
            if type(i) is int:
                request = request + '%s' % i
            elif type(i) is str:
                request = request + "\'%s\'" % i
            elif type(i) is bool:
                request = request + '%s' % i
            if num != args.__len__():
                request = request + ', '
    if nameCol is None:
        ps = db.prepare("INSERT INTO %s VALUES (%s)" % (table, request))
    else:
        ps = db.prepare("INSERT INTO %s (%s) VALUES (%s)" % (table, nameCol, request))
    ps()


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
    ps = db.prepare(text)
    ps()
    text = "CREATE TABLE IF NOT EXISTS public.currentSamara\
    (\
        temperature integer,\
        cond_cloud character varying COLLATE pg_catalog.\"default\",\
        feels integer,\
        presure integer,\
        humidity integer,\
        datetimerecord timestamp with time zone DEFAULT now() \
        )"
    ps = db.prepare(text)
    ps()
    text = "CREATE TABLE IF NOT EXISTS public.calendarSamara_last\
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


def select(table: str, specific: str=None, condition: str=None):
    if specific is None:
        spec = '*'
    else:
        spec = specific
    if condition is None:
        cond = ''
    else:
        cond = ' WHERE %s' % condition
    ps = db.query("SELECT %s FROM %s %s" % (spec, table, cond))
    return ps


def select_max(table: str, specific: str):
    if specific is None:
        spec = '*'
    else:
        spec = specific
    ps = db.query("SELECT MAX (%s) FROM %s" % (spec, table))
    return ps
