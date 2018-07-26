import requests
from bs4 import BeautifulSoup
import datetime
import dbPostgres
import createTable
import re
import schedule
import time
import logging
import calendar


def get_html(url):
    r = requests.get(url, timeout=20)
    return r.text, r.ok


def get_data_calendar(html):
    data_calendar = []
    soup = BeautifulSoup(html, 'lxml')
    data = soup.find_all('tbody', class_='weather-table__body')
    for num, i in enumerate(data, start=0):
        if (datetime.date.today().day + num) // (
                calendar.monthrange(datetime.date.today().year, datetime.date.today().month)[1] + 1) == 1:
            date = datetime.date.today().replace(day=(datetime.date.today().day + num) %
                                                     calendar.monthrange(datetime.date.today().year,
                                                                         datetime.date.today().month)[1])
            date = date.replace(month=date.month + 1)
        else:
            date = datetime.date.today().replace(day=(datetime.date.today().day + num))
        data = {'date_calendar': date}
        dg = i.find_all('tr', class_='weather-table__row')

        lens = dg[0].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value').__len__()
        if lens == 2:
            data['calendar_T_morning_minimum'] = \
                dg[0].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[0].text
            data['calendar_T_morning_maximum'] = \
                dg[0].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[1].text
        else:
            data['calendar_T_morning_minimum'] = \
                dg[0].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[0].text
            data['calendar_T_morning_maximum'] = \
                dg[0].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[0].text
        data['calendar_morning_condition'] = \
            dg[0].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_condition')[0].text
        data['calendar_morning_pressure'] = \
            dg[0].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_air-pressure')[0].text
        data['calendar_morning_humidity'] = \
            dg[0].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_humidity')[0].text
        data['calendar_T_morning_feeling'] = \
            dg[0].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_feels-like')[0].text

        lens = dg[1].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value').__len__()
        if lens == 2:
            data['calendar_T_day_minimum'] = \
                dg[1].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[0].text
            data['calendar_T_day_maximum'] = \
                dg[1].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[1].text
        else:
            data['calendar_T_day_minimum'] = \
                dg[1].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[0].text
            data['calendar_T_day_maximum'] = \
                dg[1].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[0].text
        data['calendar_day_condition'] = \
            dg[1].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_condition')[0].text
        data['calendar_day_pressure'] = \
            dg[1].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_air-pressure')[0].text
        data['calendar_day_humidity'] = \
            dg[1].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_humidity')[0].text
        data['calendar_T_day_feeling'] = \
            dg[1].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_feels-like')[0].text

        lens = dg[2].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value').__len__()
        if lens == 2:
            data['calendar_T_evening_minimum'] = \
                dg[2].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[0].text
            data['calendar_T_evening_maximum'] = \
                dg[2].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[1].text
        else:
            data['calendar_T_evening_minimum'] = \
                dg[2].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[0].text
            data['calendar_T_evening_maximum'] = \
                dg[2].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[0].text
        data['calendar_evening_condition'] = \
            dg[2].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_condition')[0].text
        data['calendar_evening_pressure'] = \
            dg[2].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_air-pressure')[0].text
        data['calendar_evening_humidity'] = \
            dg[2].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_humidity')[0].text
        data['calendar_T_evening_feeling'] = \
            dg[2].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_feels-like')[0].text

        lens = dg[3].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value').__len__()
        if lens == 2:
            data['calendar_T_night_minimum'] = \
                dg[3].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[0].text
            data['calendar_T_night_maximum'] = \
                dg[3].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[1].text
        else:
            data['calendar_T_night_minimum'] = \
                dg[3].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[0].text
            data['calendar_T_night_maximum'] = \
                dg[3].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[0].text
        data['calendar_night_condition'] = \
            dg[3].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_condition')[0].text
        data['calendar_night_pressure'] = \
            dg[3].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_air-pressure')[0].text
        data['calendar_night_humidity'] = \
            dg[3].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_humidity')[0].text
        data['calendar_T_night_feeling'] = \
            dg[3].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_feels-like')[0].text
        data_calendar.append(data.copy())
    return data_calendar


def get_data_current(html):
    soup = BeautifulSoup(html, 'lxml')
    data_current = soup.find('div', class_='fact')
    fact = {'timestamp_measured': datetime.datetime.today().utcnow()}
    fact['current_temperature'] = \
    data_current.find('div', class_='fact__temp-wrap').find_all('span', class_='temp__value')[0].text
    fact['current_condition'] = data_current.find_all('div', class_='fact__condition day-anchor i-bem')[0].text
    fact['current_temperature_feels'] = \
    data_current.find('div', class_='fact__temp-wrap').find_all('span', class_='temp__value')[1].text
    fact['current_pressure'] = data_current.find('div', class_='fact__props').find('dl',
                                                                                   class_='term term_orient_v fact__pressure').find(
        'dd',
        class_='term__value').text
    fact['current_humidity'] = data_current.find('div', class_='fact__props').find('dl',
                                                                                   class_='term term_orient_v fact__humidity').find(
        'dd', class_='term__value').text
    return fact


def toInt(s):
    try:
        return int(s)
    except ValueError:
        return s


def cleaningCalandar(data):
    try:
        for i in data:
            for y in i:
                if type(i[y]) is not datetime.date:
                    i[y] = toInt(re.search(r'[а-яА-Я\s]+|\-\d{1,3}|\d+', i[y]).group())
        return data
    except:
        return None


def cleaningCurrent(data):
    try:
        for i in data:
            if type(data[i]) is not datetime.datetime:
                data[i] = toInt(re.search(r'[а-яА-Я\s]+|\-\d{1,3}|\d+', data[i]).group())
        return data
    except:
        return None


def main_calendar():
    url = 'https://yandex.ru/pogoda/samara/details?'
    site = 1  # yandex
    html = get_html(url)
    global test_bool1, test_bool2
    global memoryData_calendar
    global need_insert_first_calendar
    global need_insert_status_calendar
    if html[1]:
        if need_insert_status_calendar:
            dbPostgres.insert('public.sysinfo', 2)
            need_insert_status_calendar = False
        data = cleaningCalandar(get_data_calendar(html[0]))
        if test_bool1:
            test_bool1 = 0
            for z in memoryData_calendar:
                if z['date_calendar'].day > 28:
                    break
                z.update({'date_calendar': z['date_calendar'].replace(day=z['date_calendar'].day + 1)})
        if test_bool2:
            test_bool2 = 0
            for z in memoryData_calendar:
                z.update({'calendar_T_evening_minimum': 9})
        if memoryData_calendar:
            dbPostgres.update('public.sysinfo', 'site', 2, 'site=2')
            for i, z in zip(range(data.__len__()), range(memoryData_calendar.__len__())):
                if data[i]['date_calendar'] != memoryData_calendar[z]['date_calendar']:
                    break
                shared_items = {k: data[i][k] for k in data[i] if k in memoryData_calendar[z] and data[i][k]
                                != memoryData_calendar[z][k]}  # what !?
                date_calendar = data[i]['date_calendar'] if shared_items.get('date_calendar') is None else shared_items['date_calendar']
                for jj in shared_items:
                    if jj != 'date_calendar':
                        dbPostgres.insert(jj, site, date_calendar, shared_items[jj])
                        print('yep calendar ', date_calendar, jj, shared_items[jj])
        elif need_insert_first_calendar:
            need_insert_first_calendar = False
            for i in data:
                for j in i:
                    date_calendar = i['date_calendar']
                    if j != 'date_calendar':
                        dbPostgres.insert(j, site, date_calendar, i[j])
                        dbPostgres.update('public.sysinfo', 'site', 2, 'site=2')
                        print('yep first calendar ', date_calendar, j, i[j])
        memoryData_calendar = data.copy()
    else:
        print("Error get_html")


def main_current():
    url = 'https://yandex.ru/pogoda/samara/?from=home'
    site = 1  # yandex
    html = get_html(url)
    global memoryData_current
    global need_insert_first_current
    global need_insert_status_current
    if html[1]:
        if need_insert_status_current:
            dbPostgres.insert('public.sysinfo', 1)
            need_insert_status_current = False
        data = cleaningCurrent(get_data_current(html[0]))
        if memoryData_current:
            dbPostgres.update('public.sysinfo', 'site', 1, 'site=1')
            shared_items = {k: data[k] for k in data if
                            k in memoryData_current and data[k] != memoryData_current[k]}  # what !?
            timestamp_measured = data['timestamp_measured']
            for jj in shared_items:
                if jj != 'timestamp_measured':
                    dbPostgres.insert(jj, site, timestamp_measured, shared_items[jj])
                    print('yep current ', timestamp_measured, jj, shared_items[jj])
        elif need_insert_first_current:
            need_insert_first_current = False
            timestamp_measured = data['timestamp_measured']
            for jd in data:
                if jd != 'timestamp_measured':
                    dbPostgres.insert(jd, site, timestamp_measured, data[jd])
                    dbPostgres.update('public.sysinfo', 'site', 1, 'site=1')
                    print('yep first current ', timestamp_measured, jd, data[jd])
        memoryData_current = data.copy()
    else:
        print("Error get_html")


if __name__ == '__main__':
    try:
        print("i\'m start")
        logging.basicConfig(filename="loging.log",
                            format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                            level=logging.WARNING)
        createTable.create_current_table()
        createTable.create_calendar_table()
        createTable.create_system_table()
        select_data1 = dbPostgres.select('public.sysinfo', 'timestamp_record', condition='WHERE site=1')
        select_data2 = dbPostgres.select('public.sysinfo', 'timestamp_record', condition='WHERE site=2')
        textForLoging = "now - " + str(datetime.datetime.now().utcnow()) + ", select_time1 - " + str(select_data1) + ", result = " + str((datetime.datetime.now().utcnow() - select_data1).seconds)
        print(textForLoging)
        logging.warning(textForLoging)
        textForLoging = "now - " + str(datetime.datetime.now().utcnow()) + ", select_time2 - " + str(select_data2) + ", result = " + str((datetime.datetime.now().utcnow() - select_data2).seconds)
        print(textForLoging)
        logging.warning(textForLoging)
        if select_data1 is not None:
            need_insert_first_current = True if (datetime.datetime.now().utcnow() - select_data1).seconds >= 180 else False
            need_insert_status_current = False
        else:
            need_insert_first_current = True
            need_insert_status_current = True
        if select_data2 is not None:
            need_insert_first_calendar = True if (datetime.datetime.now().utcnow() - select_data2).seconds >= 180 else False
            need_insert_status_calendar = False
        else:
            need_insert_first_calendar = True
            need_insert_status_calendar = True
        textForLoging = "\n need_insert_first_current - " + str(need_insert_first_current)
        textForLoging += "\n need_insert_status_current - " + str(need_insert_status_current)
        textForLoging += "\n need_insert_first_calendar - " + str(need_insert_first_calendar)
        textForLoging += "\n need_insert_status_calendar - " + str(need_insert_status_calendar)
        print(textForLoging)
        logging.warning(textForLoging)
        memoryData_calendar = []
        memoryData_current = []
        test_bool1 = 0
        test_bool2 = 0
        schedule.every(2).minutes.do(main_calendar)
        schedule.every(1).minutes.do(main_current)
        while True:
            schedule.run_pending()
            time.sleep(1)
    except Exception as ex:
        print('EXCEPTION ' + str(datetime.datetime.now().utcnow()))
        print(ex)  # for the repr
        # the first one is usually the message.
        logging.exception('exception')