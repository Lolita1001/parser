import requests
from bs4 import BeautifulSoup
import datetime
import dbPostgres
import re
import classes
import schedule
import time



if __name__ == '__main__':
    data = dbPostgres.select('weatherYandexv1')
    for i in data:
        print(i.column_names)