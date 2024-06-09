# КАТАЛОГ: КОДЫ СОСТОЯНИЯ
# 09 июн 2024

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
	SKIP    = (1000, "Пропуск выполнения")


# 02 - Данные
class CODES_DATA(CODES):
	NO_DATA       = (2000, "Данные отсутствуют")
	ERROR_CONVERT = (2001, "Ошибка преобразования данных")
	ERROR_CHECK   = (2002, "Ошибка проверки или валидации")
