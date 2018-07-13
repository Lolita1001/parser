import postgresql
import classes

db = postgresql.open('pq://pyParser:pyParser@localhost:5432/test')


def insert(table, *args, nameCol=None):
    request = ''
    q = 0
    for num, i in enumerate(args, start=1):
        if type(i) is list:
            for num1, y in enumerate(i, start=1):
                if type(y) is int:
                    request = request + '%s' % y
                elif type(y) is str:
                    request = request + "\'%s\'" % y
                elif type(y) is bool:
                    request = request + '%s' % y
                elif type(y) is classes.TimeStamp:
                    request = request + '%s' % y.time
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


def update(table, nameColum:str, value, condition=None):
    str_pole = ''
    request = ''
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


def max(table: str, specific: str):
    if specific is None:
        spec = '*'
    else:
        spec = specific
    ps = db.query("SELECT MAX (%s) FROM %s" % (spec, table))
    return ps