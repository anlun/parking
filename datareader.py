#!/usr/bin/python2
# vim: set fileencoding=utf-8 :
import urllib
import os
import MySQLdb
import csv

# 497 - номер opendata c перехватывающими парковками
data_number     = '497'
archive_address = 'http://gis-lab.info/data/mos.ru/%s.7z' % data_number
archive_name    = 'data.7z'

# Скачать архив
urllib.urlretrieve (archive_address, archive_name)

# Разархивировать
os.system('7z x %s ' % archive_name)
os.system('mv %s.csv data.csv' % data_number)

# Распарсить csv
with open('data.csv', 'rb') as csvfile:
	parkreader = csv.reader(csvfile, delimiter=';')
	flag = 0
	for row in parkreader:
		if flag == 0: # не обрабатывать первую строчку
			flag = 1
			continue

		if flag > 5: # just for tests
			break

		fields = [x.decode('cp1251').encode('utf-8') for x in row]

		uid     = fields[1]
		address = fields[4]
		x_pos   = fields[5]
		y_pos   = fields[6]
		size    = fields[13]

		print ', '.join([uid, address, x_pos, y_pos, size])
		flag += 1

# Записать в БД
db = MySQLdb.connect(host='178.130.32.141', user='vova', passwd='pass', db='olimpis')
cursor = db.cursor()

sql = """ SELECT country_name FROM country """
cursor.execute(sql)
data = cursor.fetchall()

for rec in data:
	name, = rec
	print name

db.close()