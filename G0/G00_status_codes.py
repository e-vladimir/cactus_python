# КАТАЛОГ: КОДЫ СОСТОЯНИЯ
# 10 июн 2024

import enum


class CODES(enum.Enum):
	""" Мета-структура группы кодов состояния """
	def __init__(self, code: int, description: str):
		self.code        = code
		self.description = description


# 00 - Завершение
class CODES_COMPLETION(CODES):
	COMPLETED   = (0, "Завершено")
	INTERRUPTED = (0, "Прервано")


# 01 - Выполнение
class CODES_PROCESSING(CODES):
	SKIP = (1000, "Пропуск выполнения")


# 02 - Данные
class CODES_DATA(CODES):
	NO_DATA       = (2000, "Данные отсутствуют")
	ERROR_CONVERT = (2001, "Ошибка преобразования данных")
	ERROR_CHECK   = (2002, "Ошибка проверки или валидации")
	SINGLE        = (2003, "Данные в единичном экземпляре")
	NOT_ENOUGH    = (2004, "Данных недостаточно")
	ERROR_TYPE    = (2005, "Ошибка типа данных")


# 03 - СУБД/SQL
class CODES_DB(CODES):
	ERROR_CONNECTION = (3000, "Ошибка подключения")
	NO_CONNECTION    = (3001, "Подключение отсутствует")
	ERROR_DB         = (3002, "Ошибка БД")
	ERROR_SQL        = (3003, "Ошибка SQL")
