# ОБРАБОТКА SQL-ЗАПРОСОВ
# 10 сен 2026


def FormatStringForSqlite(text: str) -> str:
	""" Подготовка текстовой строки в совместимый формат для SQLite """
	return text.replace("'", "''")

def FormatStringForPostgreSql(text: str) -> str:
	""" Подготовка текстовой строки в совместимый формат для PostgreSQL """
	return text.replace("'", "''")
