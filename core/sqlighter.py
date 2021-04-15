import sqlite3


#from database_src import db_src
#db_url = db_src()

class SQLighter:

	def __init__(self, start_id=2640):
		"""Подключаемся к БД и сохраняем курсор соединения"""
		self.connection = sqlite3.connect(r'/storage/usbdisk1/mikopbx/astlogs/asterisk/cdr.db')
		self.cursor = self.connection.cursor()

	def get_data(self):
		latest_calls = []
		try:
			with self.connection:
				result = self.cursor.execute(f'SELECT * FROM `cdr_general`;').fetchall()
				print("Всего строк:  ", len(result))
				number_group = 0
				for row in result:
					latest_calls_dict = {}
					latest_calls_dict['номер группы'] = number_group
					latest_calls_dict['id'] = row[0]
					latest_calls_dict['время поступления звонка'] = row[1]
					latest_calls_dict['исходящий номер'] = row[5]
					latest_calls_dict['входящий номер'] = row[7]
					latest_calls_dict['код сессии'] = row[9]
					latest_calls_dict['статус звонка'] = row[11]
					latest_calls_dict['путь к файлу'] = row[12]
					latest_calls.append(latest_calls_dict)
				return latest_calls
		except:
			print('ошибка')
		return latest_calls