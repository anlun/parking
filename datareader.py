#!/usr/bin/python2
# vim: set fileencoding=utf-8 :
import urllib
import os
import MySQLdb
import csv

def download_rename(address, name):
	urllib.urlretrieve(address, name)

# Скачать станции метрополитена
# download_rename('http://data.mos.ru/datasets/download/624', 'metro.csv')

# Скачать перехватывающие парковки
# download_rename('http://data.mos.ru/datasets/download/622', 'swap_parking.csv')

# Скачать платные парковки
# download_rename('http://data.mos.ru/datasets/download/623', 'pay_parking.csv')

def parse_csv(filename, positions):
	with open(filename, 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=';')
		flag = 0

		for row in reader:
			if flag == 0: # не обрабатывать первую строчку
				flag = 1
				continue

			if flag > 5: # just for tests
				break

			fields = [row[i] for i in positions]

			print ', '.join(fields)
			flag += 1

# id, address, x_pos, y_pos, size | 7 - metro
# 1 ,       4,     5,     6,    8
# parse_csv('swap_parking.csv', [1, 4, 5, 6, 8])

# id, address, x_pos, y_pos, size
# 1 ,       4,     5,     6,    7
# parse_csv('pay_parking.csv', [1, 4, 5, 6, 7])

# 0_uidnftn;1_Наименование;0_label;0_address;0_x;0_y;
# 0_bui_no_bti;0_cad_no;0_street_bti;0_house_bti;0_hadd_bti;
# 1_Линия;1_Статус;Вестибюль;1_Выход из вестибюля;1_Время отправления первого и последнего поездов по четным дням;
# 1_Время отправления первого и последнего поездов в нечетные дни;1_Количество БПА;1_Эскалаторы. Плановая дата замены/ремонта;
# 1_Эскалаторы. Тип до и после ремонта;1_Эскалаторы. Высота подъема;1_Эскалаторы. Количество до и после замены;0_moddate;0_moduser;1_Тип БПА

# name, x_pos, y_pos, line
# 1   ,     4,     5,   11
parse_csv('metro.csv', [1, 4, 5, 11])

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