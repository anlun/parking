#!/usr/bin/python2
# vim: set fileencoding=utf-8 :
import urllib
import os
import MySQLdb
import csv

metro_filename        = 'metro.csv'
metro_url             = 'http://data.mos.ru/datasets/download/624'

swap_parking_filename = 'swap_parking.csv'
swap_parking_url      = 'http://data.mos.ru/datasets/download/622'

pay_parking_filename  = 'pay_parking.csv'
pay_parking_url       = 'http://data.mos.ru/datasets/download/623'

# Скачать нужные OpenData
# urllib.urlretrieve(metro_url, metro_filename)
# urllib.urlretrieve(swap_parking_url, swap_parking_filename)
# urllib.urlretrieve(pay_parking_url, pay_parking_filename)

def parse_csv(filename, positions):
	result = []
	with open(filename, 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=';')
		flag = 0

		for row in reader:
			if flag == 0: # не обрабатывать первую строчку
				flag = 1
				continue

			# if flag > 5: # just for tests
			# 	break

			fields = [row[i].strip() for i in positions]
			result.append(fields)

			# print ', '.join(fields)
			flag += 1
	return result

# id, address, lng, lat, size | 7 - metro
# 1 ,       4,   5,   6,    8
parse_csv(swap_parking_filename, [1, 4, 5, 6, 8])

# id, address, lng, lat, size
# 1 ,       4,   5,   6,    7
parse_csv(pay_parking_filename, [1, 4, 5, 6, 7])

# 0_uidnftn;1_Наименование;0_label;0_address;0_x;0_y;
# 0_bui_no_bti;0_cad_no;0_street_bti;0_house_bti;0_hadd_bti;
# 1_Линия;1_Статус;Вестибюль;1_Выход из вестибюля;1_Время отправления первого и последнего поездов по четным дням;
# 1_Время отправления первого и последнего поездов в нечетные дни;1_Количество БПА;1_Эскалаторы. Плановая дата замены/ремонта;
# 1_Эскалаторы. Тип до и после ремонта;1_Эскалаторы. Высота подъема;1_Эскалаторы. Количество до и после замены;0_moddate;0_moduser;1_Тип БПА

# name, lng, lat, line
# 1   ,   4,   5,   11
def update_metro_info(connect, cursor):
	try:
		cursor.execute("""DELETE FROM metro""")

		metro_result = parse_csv(metro_filename, [1, 4, 5, 11])
		for metro in metro_result:
			sql = """INSERT IGNORE INTO metro (header, lat, lng) VALUES (\"%s\", (%s), (%s))""" % (metro[0], metro[2].replace(',', '.'), metro[1].replace(',', '.'))
			cursor.execute(sql)
		connect.commit()
	except:
		print "Error in metro insert work!"
		connect.rollback()

def update_parking_info(connect, cursor):
	try:
		cursor.execute("""DELETE FROM parking""")

		swap_parking = parse_csv(swap_parking_filename, [1, 4, 5, 6, 8])
		pay_parking  = parse_csv(pay_parking_filename , [1, 4, 5, 6, 7])
		# parkings = pay_parking + swap_parking

		for parking in swap_parking:
			# TODO: убрать Magic Number в parking_type_id
			sql = """INSERT INTO parking (parking_type_id, header, address, lat, lng, total_space) VALUES (1, \"%s\", \"%s\", %s, %s, %s)""" % (parking[1], parking[1], parking[3].replace(',', '.'), parking[2].replace(',', '.'), parking[4])
			cursor.execute(sql)

		for parking in pay_parking:
			# TODO: убрать Magic Number в parking_type_id и в is_free
			sql = """INSERT INTO parking (parking_type_id, is_free, header, address, lat, lng, total_space) VALUES (1, 0, \"%s\", \"%s\", %s, %s, %s)""" % (parking[1], parking[1], parking[3].replace(',', '.'), parking[2].replace(',', '.'), parking[4])
			cursor.execute(sql)

		connect.commit()
	except:
		print "Error in parking insert work!"
		connect.rollback()

# Записать в БД
db = MySQLdb.connect(host='178.130.32.141', user='vova', passwd='pass', db='parking')
# cursor = db.cursor()

# update_metro_info  (db, db.cursor())
update_parking_info(db, db.cursor())

db.close()