# КАТАЛОГ: ФИЛЬТРЫ
# 08 июн 2024

import enum


class FILTERS(enum.Enum):
	EQUAL            =  (0, "Равенство")

	MORE             = (10, "Больше")
	MORE_OR_EQUAL    = (11, "Больше или равно")

	LESS             = (20, "Меньше")
	LESS_OR_EQUAL    = (21, "Меньше или равно")

	INCLUDE          = (30, "Включает в себя")

	IN               = (40, "Входит в список")

	BETWEEN          = (50, "В пределах")
	BETWEEN_OR_EQUAL = (51, "В пределах или равно")

	def __init__(self, code: int, description: str):
		self.code         = code
		self.descriptions = description
