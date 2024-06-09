# КАТАЛОГ: КАКТУС
# 09 июн 2024

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
class CACTUS_STRUCT_ID(enum.Enum):
	OCI = ("oci", "_oci")
	OID = ("oid", "_oid")
	PID = ("pid", "_pid")
	SID = ("sid", "_sid")
	CID = ("cid", "_cid")
	CVL = ("cvl", "_cvl")
	CUT = ("cut", "_cut")

	def __init__(self, name: str, name_sql: str):
		self.name     = name
		self.name_sql = name_sql


# ТИП ПОДКЛЮЧЕНИЯ
class CONNECTION_MANAGEMENT(enum.Enum):
	OFF     = (0, "Управление подключением отключено")
	AUTO    = (1, "Автоматическое управление подключением")
	TIMEOUT = (2, "Управление по timeout")

	def __init__(self, name: str, name_sql: str):
		self.name     = name
		self.name_sql = name_sql
