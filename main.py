import requests
from bs4 import BeautifulSoup
import datetime
import dbPostgres
import re
import schedule
import time
import logging
import copy


def get_html(url):
    #print('start get_html ' + url) # temp
    r = requests.get(url)
    #print('finish get_html ' + str(r.ok)) # temp
    return r.text, r.ok


def get_data_calendar(html):
    #print('start get_data_calendar')  # temp
    calendar = []
    soup = BeautifulSoup(html, 'lxml')
    data = soup.find_all('tbody', class_='weather-table__body')
    for num, i in enumerate(data, start=0):
        date = datetime.datetime.today().replace(day=datetime.date.today().day + num)
        data = {'dateTimeMeasure': date}
        dg = i.find_all('tr', class_='weather-table__row')

        lens = dg[0].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value').__len__()
        if lens == 2:
            data['mor_min'] = \
                dg[0].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[0].text
            data['mor_max'] = \
                dg[0].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[1].text
        else:
            data['mor_min'] = \
                dg[0].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[0].text
            data['mor_max'] = \
                dg[0].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[0].text
        data['mor_cond_cloud'] = \
            dg[0].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_condition')[0].text
        data['mor_presure'] = \
            dg[0].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_air-pressure')[0].text
        data['mor_humidity'] = \
            dg[0].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_humidity')[0].text
        data['mor_feeling'] = \
            dg[0].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_feels-like')[0].text

        lens = dg[1].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value').__len__()
        if lens == 2:
            data['day_min'] = \
                dg[1].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[0].text
            data['day_max'] = \
                dg[1].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[1].text
        else:
            data['day_min'] = \
                dg[1].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[0].text
            data['day_max'] = \
                dg[1].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[0].text
        data['day_cond_cloud'] = \
            dg[1].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_condition')[0].text
        data['day_presure'] = \
            dg[1].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_air-pressure')[0].text
        data['day_humidity'] = \
            dg[1].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_humidity')[0].text
        data['day_feeling'] = \
            dg[1].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_feels-like')[0].text

        lens = dg[2].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value').__len__()
        if lens == 2:
            data['eve_min'] = \
                dg[2].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[0].text
            data['eve_max'] = \
                dg[2].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[1].text
        else:
            data['eve_min'] = \
                dg[2].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[0].text
            data['eve_max'] = \
                dg[2].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[0].text
        data['eve_cond_cloud'] = \
            dg[2].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_condition')[0].text
        data['eve_presure'] = \
            dg[2].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_air-pressure')[0].text
        data['eve_humidity'] = \
            dg[2].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_humidity')[0].text
        data['eve_feeling'] = \
            dg[2].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_feels-like')[0].text

        lens = dg[3].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value').__len__()
        if lens == 2:
            data['ngh_min'] = \
                dg[3].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[0].text
            data['ngh_max'] = \
                dg[3].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[1].text
        else:
            data['ngh_min'] = \
                dg[3].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[0].text
            data['ngh_max'] = \
                dg[3].find_all('div', class_='weather-table__temp')[0].find_all('span', class_='temp__value')[0].text
        data['ngh_cond_cloud'] = \
            dg[3].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_condition')[0].text
        data['ngh_presure'] = \
            dg[3].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_air-pressure')[0].text
        data['ngh_humidity'] = \
            dg[3].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_humidity')[0].text
        data['ngh_feeling'] = \
            dg[3].find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_feels-like')[0].text
        calendar.append(data.copy())
    #print('finish get_data_calendar')  # temp
    return calendar


def get_data_current(html):
    #print('start get_data_current')  # temp
    fact = {}
    soup = BeautifulSoup(html, 'lxml')
    data = soup.find('div', class_='fact')
    fact['temperature'] = data.find('div', class_='fact__temp-wrap').find_all('span', class_='temp__value')[0].text
    fact['cond_cloud'] = data.find_all('div', class_='fact__condition day-anchor i-bem')[0].text
    fact['feels'] = data.find('div', class_='fact__temp-wrap').find_all('span', class_='temp__value')[1].text
    fact['presure'] = data.find('div', class_='fact__props').find('dl',
                                                                  class_='term term_orient_v fact__pressure').find('dd',
                                                                                                                   class_='term__value').text
    fact['humidity'] = data.find('div', class_='fact__props').find('dl',
                                                                   class_='term term_orient_v fact__humidity').find(
        'dd', class_='term__value').text
    #print('finish get_data_current')  # temp
    return fact


def toInt(s):
    #print('start toInt')  # temp
    try:
        #print('finish toInt try')  # temp
        return int(s)
    except ValueError:
        #print('finish toInt except')  # temp
        return s


def cleaningCalandar(data):
    #print('start cleaningCalandar')  # temp
    try:
        for i in data:
            for y in i:
                if type(i[y]) is not datetime.datetime:
                    i[y] = toInt(re.search(r'[а-яА-Я\s]+|\-\d{1,3}|\d+', i[y]).group())
        #print('finish cleaningCalandar try')  # temp
        return data
    except:
        #print('finish cleaningCalandar except')  # temp
        return None


def cleaningCurrent(data):
    #print('start cleaningCurrent')  # temp
    try:
        for i in data:
            data[i] = toInt(re.search(r'[а-яА-Я\s]+|\-\d{1,3}|\d+', data[i]).group())
        #print('finish cleaningCurrent try')  # temp
        return data
    except:
        #print('finish cleaningCurrent except')  # temp
        return None


def main_calendar():
    #print('start main_calendar')  # temp
    url = 'https://yandex.ru/pogoda/samara/details?'
    html = get_html(url)
    global memoryData
    if html[1]:
        data = cleaningCalandar(get_data_calendar(html[0]))
        for i in data:
            req = []
            for y in i:
                req.append(i[y])
            dbPostgres.insert('calendarSamara', req)
        print('yep calendar\n\n\n')

        req = []
        if memoryData:
            temp_data = copy.deepcopy(data)
            temp_memoryData = copy.deepcopy(memoryData)
            for i,z in zip(range(temp_data.__len__()), range(temp_memoryData.__len__())):
                temp_data[i]['dateTimeMeasure'] = temp_data[i]['dateTimeMeasure'].date()
                temp_memoryData[z]['dateTimeMeasure'] = temp_memoryData[z]['dateTimeMeasure'].date()
                if temp_data[i]['dateTimeMeasure'] != temp_memoryData[z]['dateTimeMeasure']:
                    break
                shared_items = {k: temp_data[i][k] for k in temp_data[i] if k in temp_memoryData[z] and temp_data[i][k] != temp_memoryData[z][k]}  # what !?
                if len(shared_items) != 0:
                    for y in data[i]:
                        req.append(data[i][y])
                        logging.error(req)
            '''
            for num1, num2 in zip(range(temp_data.__len__()), range(memoryData.__len__())):
                for (k, v), (k2, v2) in zip(temp_data[num1].items(), temp_memoryData[num2].items()):
                #for num, i in enumerate(data):
                    if type(v) is datetime.datetime:
                        if v.date() == v2.date():
                            num2 +=1
                            req.append(temp_data[temp_data.__len__() - 1])
                            temp_data.pop()
                            continue
                    else:
                        print()
                    date_mem = temp_memoryData['dateTimeMeasure'].date()
                    #data[num].update({'dateTimeMeasure':data[num]['dateTimeMeasure'].replace(day=17)})  # временная
                    date_curr = temp_data[num]['dateTimeMeasure'].date()
                    while date_mem != date_curr:
                        temp_memoryData.pop(0)
                        #del memoryData[num]['dateTimeMeasure']
                        #del data[num]['dateTimeMeasure']
                        #if memoryData[num] == data[num]:
                        #    print('different date')
                        date_mem = temp_memoryData[num]['dateTimeMeasure'].date()
                        date_curr = temp_data[num]['dateTimeMeasure'].date()
                    del temp_memoryData[num]['dateTimeMeasure']
                    del temp_data[num]['dateTimeMeasure']
                    if temp_memoryData[num] != temp_data[num]:
                        for y in i:
                            req.append(i[y])
                            print('different temp')
                            print(req)
    '''
        memoryData = data.copy()


def main_current():
    #print('start main_current')  # temp
    url = 'https://yandex.ru/pogoda/samara/?from=home'
    html = get_html(url)
    if html[1]:
        data = cleaningCurrent(get_data_current(html[0]))
        req = []
        for j in data:
            req.append(data[j])
        dbPostgres.insert('currentSamara', req)
        print('yep current\n\n\n')
    else:
        print("Error get_html")
        logging.error("Error get_html")

if __name__ == '__main__':
    schedule.every(2).minutes.do(main_calendar)
    schedule.every(1).minutes.do(main_current)
    logging.basicConfig(filename="loging.log",
                        format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                        level=logging.INFO)
    try:
        memoryData = []
        dbPostgres.create()
        while True:
            #print('start while 1 sec ' + time.strftime('%X'))  # temp
            schedule.run_pending()
            #print('finish schedule '  + time.strftime('%X'))  # temp
            time.sleep(1)
            #print('finish while 1 sec + ' + time.strftime('%X'))  # temp
    except:
        logging.exception()
