# КАКТУС: КОНВЕРТОРЫ ДАННЫХ
# 31 июл 2024


# КОНВЕРТОР ИДЕНТИФИКАТОРОВ
def UnificationIdc(idc: str) -> str:
	""" Конвертация IDC в унифицированный вид """
	idc = idc.replace(' ', '_', -1)
	idc = idc.replace('-', '_', -1)
	idc = idc.replace(':', '_', -1)
	idc = idc.replace('.', '_', -1)
	idc = idc.lower()

	return idc


def IdoFromIds(ids: str) -> str:
	""" Извлечение IDO из IDS """
	try   : return ids.split('.')[0]
	except: return ""


def IdpFromIds(ids: str) -> str:
	""" Извлечение IDP из IDS """
	try   : return ids.split('.')[1]
	except: return ""
