# КАТАЛОГ: КОДЫ СОСТОЯНИЯ
# 08 июн 2024

import enum


class GROUP_CODES(enum.Enum):
	""" Мета-структура группы кодов состояния """
	def __init__(self, code: int, description: str):
		self.code        = code
		self.description = description


# 00 - Коды завершения
class CODES_COMPLETION(GROUP_CODES):
	COMPLETED   = (0, "Завершено")
