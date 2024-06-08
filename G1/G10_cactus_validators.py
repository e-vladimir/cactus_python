# КАКТУС: ВАЛИДАТОРЫ ДАННЫХ
# 2022-11-19

def ValidateOci(oci: str) -> bool:
	""" Валидация OCI """
	if      not oci: return False
	elif ' ' in oci: return False
	elif '.' in oci: return False
	elif '-' in oci: return False

	return True


def ValidateOid(oid: str) -> bool:
	""" Валидация OID """
	if      not oid: return False
	elif '.' in oid: return False

	return True


def ValidatePid(oid: str) -> bool:
	""" Валидация PID """
	if      not oid: return False
	elif '.' in oid: return False

	return True
