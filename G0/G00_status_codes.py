# КАТАЛОГ: КОДЫ СОСТОЯНИЯ
# 08 июн 2024

import enum


class CStatusCodesGroup(enum.Enum):
	""" Мета-структура группы кодов состояния """
	def __init__(self, code: int, description: str):
		self.code        = code
		self.description = description


# 00 - Коды завершения
class Codes_Completion(CStatusCodesGroup):
	COMPLETED   = (0, "Завершено")
	PROCESSING  = (1, "Выполняется")
	INTERRUPTED = (2, "Прервано")


# 01 - Коды выполнения
class Codes_Exec(CStatusCodesGroup):
	pass


# 02 - Коды данных
class Codes_Data(CStatusCodesGroup):
	pass
