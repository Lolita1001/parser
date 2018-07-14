import requests
from bs4 import BeautifulSoup
import datetime
import dbPostgres
import re
import classes
import schedule
import time

def get_html(url):
    r = requests.get(url)
    return r.text

def get_data_calendar(html):
    calendar = []
    soup = BeautifulSoup(html, 'lxml')
    datas = soup.find_all('tbody', class_='weather-table__body')
    for num,i in enumerate(datas, start=0):
        date = classes.TimeStamp()
        date.time = datetime.datetime.today().replace(day=datetime.date.today().day + num).strftime("TIMESTAMP\'%Y-%m-%d %H:%M:%S\'")
        data = {'dateTimeMeasure': date}
        dg = i.find_all('tr', class_='weather-table__row')

        lens = dg[0].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value').__len__()
        if lens == 2:
            data['mor_min'] = dg[0].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[0].text
            data['mor_max'] = dg[0].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[1].text
        else:
            data['mor_min'] = dg[0].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[0].text
            data['mor_max'] = dg[0].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[0].text
        data['mor_cond_cloud'] = dg[0].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_condition')[0].text
        data['mor_presure'] = dg[0].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_air-pressure')[0].text
        data['mor_humidity'] = dg[0].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_humidity')[0].text
        data['mor_feeling'] = dg[0].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_feels-like')[0].text

        lens = dg[1].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value').__len__()
        if lens == 2:
            data['day_min'] = dg[1].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[0].text
            data['day_max'] = dg[1].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[1].text
        else:
            data['day_min'] = dg[1].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[0].text
            data['day_max'] = dg[1].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[0].text
        data['day_cond_cloud'] = dg[1].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_condition')[0].text
        data['day_presure'] = dg[1].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_air-pressure')[0].text
        data['day_humidity'] = dg[1].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_humidity')[0].text
        data['day_feeling'] = dg[1].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_feels-like')[0].text

        lens = dg[2].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value').__len__()
        if lens == 2:
            data['eve_min'] = dg[2].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[0].text
            data['eve_max'] = dg[2].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[1].text
        else:
            data['eve_min'] = dg[2].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[0].text
            data['eve_max'] = dg[2].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[0].text
        data['eve_cond_cloud'] = dg[2].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_condition')[0].text
        data['eve_presure'] = dg[2].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_air-pressure')[0].text
        data['eve_humidity'] = dg[2].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_humidity')[0].text
        data['eve_feeling'] = dg[2].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_feels-like')[0].text

        lens = dg[3].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value').__len__()
        if lens == 2:
            data['ngh_min'] = dg[3].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[0].text
            data['ngh_max'] = dg[3].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[1].text
        else:
            data['ngh_min'] = dg[3].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[0].text
            data['ngh_max'] = dg[3].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[0].text
        data['ngh_cond_cloud'] = dg[3].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_condition')[0].text
        data['ngh_presure'] = dg[3].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_air-pressure')[0].text
        data['ngh_humidity'] = dg[3].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_humidity')[0].text
        data['ngh_feeling'] = dg[3].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_feels-like')[0].text
        '''
        data['mor_min'] = dg[0].find_all('div', class_='temp')[0].text
        data['mor_max'] = dg[0].find_all('div', class_='temp')[1].text
        data['mor_cond_cloud'] = dg[0].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_condition')[0].text
        data['mor_presure'] = dg[0].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_air-pressure')[0].text
        data['mor_humidity'] = dg[0].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_humidity')[0].text
        data['mor_feeling'] = dg[0].find_all('div', class_='temp')[2].text
        data['day_min'] = dg[1].find_all('div', class_='temp')[0].text
        data['day_max'] = dg[1].find_all('div', class_='temp')[1].text
        data['day_cond_cloud'] = dg[1].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_condition')[0].text
        data['day_presure'] = dg[1].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_air-pressure')[0].text
        data['day_humidity'] = dg[1].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_humidity')[0].text
        data['day_feeling'] = dg[1].find_all('div', class_='temp')[2].text
        data['eve_min'] = dg[2].find_all('div', class_='temp')[0].text
        data['eve_max'] = dg[2].find_all('div', class_='temp')[1].text
        data['eve_cond_cloud'] = dg[2].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_condition')[0].text
        data['eve_presure'] = dg[2].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_air-pressure')[0].text
        data['eve_humidity'] = dg[2].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_humidity')[0].text
        data['eve_feeling'] = dg[2].find_all('div', class_='temp')[2].text
        data['ngh_min'] = dg[3].find_all('div', class_='temp')[0].text
        data['ngh_max'] = dg[3].find_all('div', class_='temp')[1].text
        data['ngh_cond_cloud'] = dg[3].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_condition')[0].text
        data['ngh_presure'] = dg[3].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_air-pressure')[0].text
        data['ngh_humidity'] = dg[3].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_humidity')[0].text
        data['ngh_feeling'] = dg[3].find_all('div', class_='temp')[2].text
        '''
        calendar.append(data.copy())
    return calendar

def get_data_fact(html):
    fact = {}
    soup = BeautifulSoup(html, 'lxml')
    data = soup.find('div', class_='fact')
    fact['temp'] = data.find('div', class_='fact__temp-wrap').find_all('span', class_='temp__value')[0].text
    fact['cond_cloud'] = data.find_all('div', class_='fact__condition day-anchor i-bem')[0].text
    fact['feels'] = data.find('div', class_='fact__temp-wrap').find_all('span', class_='temp__value')[1].text
    fact['presure'] = data.find('div', class_='fact__props').find('dl', class_='term term_orient_v fact__pressure').find('dd', class_='term__value').text
    fact['humidity'] = data.find('div', class_='fact__props').find('dl', class_='term term_orient_v fact__humidity').find('dd', class_='term__value').text
    return fact

def toInt(s):
    try:
        return int(s)
    except ValueError:
        return s

def cleaning(data):
    try:
        for i in data:
            for y in i:
                if type(i[y]) is not classes.TimeStamp:
                    i[y] = toInt(re.search(r'[а-яА-Я\s]+|\-\d{1,3}|\d+', i[y]).group())
        return data
    except:
        return None


def main():
    url = 'https://yandex.ru/pogoda/samara/details?'
    url1 = 'https://yandex.ru/pogoda/samara/?from=home'
    #selectData = dbPostgres.select('weatheryandex1')
    data = cleaning(get_data_calendar(get_html(url)))
    data_1 = get_data_fact(get_html(url1))
    for i in data:
        req = []
        for y in i:
            req.append(i[y])
        dbPostgres.insert('weatheryandexv1', req)
    print('yep')

    #ffffff = '\'TIMESTAMP\'2000-01-01 00:00:00\'\', \'TIMESTAMP\'2000-01-01 00:00:00\'\', 18, 25, 25, 26, 20, 26, 17, 19, '
    #ffffff = 'TIMESTAMP\'2000-01-01 00:00:00\', TIMESTAMP\'2000-01-01 00:00:00\', 22, 27, 24, 27, 18, 23, 17, 18'
    #ps = db.prepare("INSERT INTO %s VALUES (%s)" % ('weatherYandex', ffffff))
    #ps()

schedule.every(5).seconds.do(main)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)
