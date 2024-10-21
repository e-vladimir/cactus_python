# КАТАЛОГ: КАКТУС
# 21 окт 2024

import enum


# ВИДЫ КОНТЕЙНЕРОВ
class CONTAINERS(enum.Enum):
	NONE       = ( 0, "Нет контейнера")
	RAM        = ( 1, "RAM-Контейнер")
	SQL        = (10, "SQL-Контейнер")
	SQLITE     = (11, "SQL.SQLite-Контейнер")
	POSTGRESQL = (12, "SQL.Postgresql-Контейнер")

	def __init__(self, code: int, description: str):
		self.code         = code
		self.descriptions = description


# ИДЕНТИФИКАТОРЫ СТРУКТУРЫ ДАННЫХ
class CACTUS_STRUCT_DATA(enum.Enum):
	IDC = (0, "idc", "_idc")  # Идентификатор класса объектов
	IDO = (1, "ido", "_ido")  # Идентификатор объекта
	IDP = (2, "idp", "_idp")  # Идентификатор параметра объекта
	VLP = (5, "vlp", "_vlp")  # Значение параметра объекта
	VLT = (6, "vlt", "_vlt")  # Отметка времени актуальности

	IDF = (4, "idf", "_idf")  # Идентификатор ячейки (полный)
	IDS = (3, "ids", "_ids")  # Идентификатор ячейки (сокращённый)

	def __init__(self, code: int, name_base: str, name_sql: str):
		self.code      = code
		self.name_base = name_base
		self.name_sql  = name_sql


# ТИП ПОДКЛЮЧЕНИЯ
class CONNECTION_MANAGEMENT(enum.Enum):
	MANUAL  = (0, "Ручное управление подключением")
	AUTO    = (1, "Автоматическое управление подключением")
	TIMEOUT = (2, "Управление по timeout")

	def __init__(self, code: int, name_sql: str):
		self.code     = code
		self.name_sql = name_sql


# РАСШИРЕНИЕ СТРУКТУРНЫХ ПАРАМЕТРОВ
class POSTFIX(enum.Enum):
	CS  = (0,  "cs")
	RS  = (1,  "cs")
	SRC = (2, "src")
	DST = (3, "dst")

	def __init__(self, code: int, name: str):
		self.code = code
		self.name = name
