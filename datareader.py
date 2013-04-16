#!/usr/bin/python2
# vim: set fileencoding=utf-8 :
import urllib
import os

# 497 - номер opendata c перехватывающими парковками
data_number     = "497"
archive_address = "http://gis-lab.info/data/mos.ru/%s.7z" % data_number
archive_name    = "data.7z"

# Скачать архив
urllib.urlretrieve (archive_address, archive_name)

# Разархивировать
os.system("7z x %s " % archive_name)
os.system("mv %s.csv data.csv" % data_number)

# Распарсить csv

# Записать в БД