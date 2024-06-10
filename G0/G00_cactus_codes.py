# КАТАЛОГ: КАКТУС
# 10 июн 2024

import enum


# ВИДЫ КОНТЕЙНЕРОВ
class CONTAINERS(enum.Enum):
	CONTAINER_NONE       = ( 0, "Нет контейнера")
	CONTAINER_RAM        = ( 1, "RAM-Контейнер")
	CONTAINER_SQL        = (10, "SQL-Контейнер")
	CONTAINER_SQLITE     = (11, "SQL.SQLite-Контейнер")
	CONTAINER_POSTGRESQL = (12, "SQL.Postgresql-Контейнер")

	def __init__(self, code: int, description: str):
		self.code         = code
		self.descriptions = description


# ИДЕНТИФИКАТОРЫ СТРУКТУРЫ ДАННЫХ
class CACTUS_STRUCT_DATA(enum.Enum):
	OCI = (0, "oci", "_oci")
	OID = (1, "oid", "_oid")
	PID = (2, "pid", "_pid")
	SID = (3, "sid", "_sid")
	CID = (4, "cid", "_cid")
	CVL = (5, "cvl", "_cvl")
	CUT = (6, "cut", "_cut")

	def __init__(self, code: int, name_base: str, name_sql: str):
		self.code      = code
		self.name_base = name_base
		self.name_sql  = name_sql


# ТИП ПОДКЛЮЧЕНИЯ
class CONNECTION_MANAGEMENT(enum.Enum):
	OFF     = (0, "Управление подключением отключено")
	AUTO    = (1, "Автоматическое управление подключением")
	TIMEOUT = (2, "Управление по timeout")

	def __init__(self, code: int, name_sql: str):
		self.code     = code
		self.name_sql = name_sql


# РАСШИРЕНИЕ СТРУКТУРНЫХ ПАРАМЕТРОВ
CS_POSTFIX  = "cs"
RS_POSTFIX  = "cs"
SRC_POSTFIX = "src"
DST_POSTFIX = "dst"
