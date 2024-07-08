# КАКТУС: ВАЛИДАТОРЫ ДАННЫХ
# 08 июл 2024

def ValidateIdc(idc: str) -> bool:
	""" Валидация IDC """
	if      not idc: return False
	elif ' ' in idc: return False
	elif '.' in idc: return False
	elif '-' in idc: return False

	return True


def ValidateIdo(ido: str) -> bool:
	""" Валидация IDO """
	if      not ido: return False
	elif '.' in ido: return False

	return True


def ValidateIdp(ido: str) -> bool:
	""" Валидация IDP """
	if      not ido: return False
	elif '.' in ido: return False

	return True
