#!/usr/bin/python2
# vim: set fileencoding=utf-8 :
import urllib
import os
import MySQLdb
import csv

def download_rename(address, name):
	urllib.urlretrieve(address, name)

# Скачать станции метрополитена
download_rename('http://data.mos.ru/datasets/download/624', 'metro.csv')

# Скачать перехватывающие парковки
download_rename('http://data.mos.ru/datasets/download/622', 'swap_parking.csv')

# Скачать платные парковки
download_rename('http://data.mos.ru/datasets/download/623', 'pay_parking.csv')

# Распарсить csv
# with open('swap_parking.csv', 'rb') as csvfile:
# 	parkreader = csv.reader(csvfile, delimiter=';')
# 	flag = 0
# 	for row in parkreader:
# 		if flag == 0: # не обрабатывать первую строчку
# 			flag = 1
# 			continue

# 		if flag > 5: # just for tests
# 			break

# 		fields = [x.decode('cp1251').encode('utf-8') for x in row]

# 		uid     = fields[1]
# 		address = fields[4]
# 		x_pos   = fields[5]
# 		y_pos   = fields[6]
# 		metro   = fields[12]
# 		size    = fields[13]

# 		print ', '.join([uid, address, x_pos, y_pos, size])
# 		flag += 1

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