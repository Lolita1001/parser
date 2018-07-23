import requests
from bs4 import BeautifulSoup
import datetime
import dbPostgres
import createTable
import re
import schedule
import time
import logging
import copy
import calendar


def get_html(url):
    r = requests.get(url)
    return r.text, r.ok


def get_data_calendar(html):
    data_calendar = []
    soup = BeautifulSoup(html, 'lxml')
    data = soup.find_all('tbody', class_='weather-table__body')
    for num, i in enumerate(data, start=0):
        if (datetime.date.today().day + num) // (calendar.monthrange(datetime.datetime.today().year, datetime.datetime.today().month)[1] + 1) == 1:
            date = datetime.datetime.today().replace(day=(datetime.date.today().day + num) % calendar.monthrange(datetime.datetime.today().year, datetime.datetime.today().month)[1])
            date = date.replace(month=date.date().month + 1)
        else:
            date = datetime.datetime.today().replace(day=(datetime.date.today().day + num))
        data = {'DTMeasured': date}
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
    fact = {}
    soup = BeautifulSoup(html, 'lxml')
    data_current = soup.find('div', class_='fact')
    fact = {'DTMeasured': datetime.datetime.today()}
    fact['current_temperature'] = data_current.find('div', class_='fact__temp-wrap').find_all('span', class_='temp__value')[0].text
    fact['current_condition'] = data_current.find_all('div', class_='fact__condition day-anchor i-bem')[0].text
    fact['current_temperature_feels'] = data_current.find('div', class_='fact__temp-wrap').find_all('span', class_='temp__value')[1].text
    fact['current_pressure'] = data_current.find('div', class_='fact__props').find('dl',
                                                                  class_='term term_orient_v fact__pressure').find('dd',
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
                if type(i[y]) is not datetime.datetime:
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
    site = 1 # yandex
    html = get_html(url)
    global memoryData_calendar
    if html[1]:
        data = cleaningCalandar(get_data_calendar(html[0]))
        if memoryData_calendar:
            for i, z in zip(range(data.__len__()), range(memoryData_calendar.__len__())):
                if data[i]['DTMeasured'].date() != memoryData_calendar[z]['DTMeasured'].date():
                    break
                shared_items = {k: data[i][k] for k in data[i] if k in memoryData_calendar[z] and data[i][k]
                                != memoryData_calendar[z][k]}  # what !?
                if shared_items.__len__() > 1:
                    for jj in shared_items:
                        if jj == 'DTMeasured':
                            DTMeasured = shared_items[jj]
                        else:
                            dbPostgres.insert(jj, site, DTMeasured, shared_items[jj])
                            print('yep calendar ', DTMeasured, jj, shared_items[jj])
        else:
            for i in data:
                for j in i:
                    if j == 'DTMeasured':
                        DTMeasured = i[j]
                    else:
                        dbPostgres.insert(j, site, DTMeasured, i[j])
                        print('yep first calendar ', DTMeasured, j, i[j])
        memoryData_calendar = data.copy()
    else:
        print("Error get_html")

def main_current():
    url = 'https://yandex.ru/pogoda/samara/?from=home'
    site = 1 # yandex
    html = get_html(url)
    global memoryData_current
    if html[1]:
        data = cleaningCurrent(get_data_current(html[0]))
        if memoryData_current:
            shared_items = {k: data[k] for k in data if
                                k in memoryData_current and data[k] != memoryData_current[k]}  # what !?
            if shared_items.__len__() > 1:
                for jj in shared_items:
                    if jj == 'DTMeasured':
                        DTMeasured = shared_items[jj]
                    else:
                        dbPostgres.insert(jj, site, DTMeasured, shared_items[jj])
                        print('yep current ', DTMeasured, jj, shared_items[jj])
        else:
            for jd in data:
                if jd == 'DTMeasured':
                    DTMeasured = data[jd]
                else:
                    dbPostgres.insert(jd, site, DTMeasured, data[jd])
                    print('yep first current ', DTMeasured, jd, data[jd])
        memoryData_current = data.copy()
    else:
        print("Error get_html")

if __name__ == '__main__':
    print("i\'m start")
    createTable.create_current_table()
    createTable.create_calendar_table()
    logging.basicConfig(filename="loging.log",
                        format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                        level=logging.INFO)
    schedule.every(1).minutes.do(main_calendar)
    schedule.every(1).minutes.do(main_current)
    memoryData_calendar = []
    memoryData_current = []
    while True:
        schedule.run_pending()
        time.sleep(1)