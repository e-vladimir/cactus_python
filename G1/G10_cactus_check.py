# КАКТУС: ПРОВЕРКА ДАННЫХ
# 09 июл 2024

def CheckIdc(idc: str) -> bool:
	""" Проверка IDC """
	if      not idc: return False
	elif ' ' in idc: return False
	elif '.' in idc: return False
	elif '-' in idc: return False

	return True


def CheckIdo(ido: str) -> bool:
	""" Проверка IDO """
	if      not ido: return False
	elif '.' in ido: return False

	return True


def CheckIdp(ido: str) -> bool:
	""" Проверка IDP """
	if      not ido: return False
	elif '.' in ido: return False

	return True
