# КАКТУС: КОНВЕРТОРЫ ДАННЫХ
# 08 июн 2024


# КОНВЕРТОР ИДЕНТИФИКАТОРОВ
def UnificationOci(oci: str) -> str:
	""" Конвертация OCI в унифицированный вид """
	oci = oci.replace(' ', '_', -1)
	oci = oci.replace('-', '_', -1)
	oci = oci.lower()

	return oci


def OidFromSid(sid: str) -> str:
	""" Извлечение OID из SID """
	try   : return sid.split('.')[0]
	except: return ""


def PidFromSid(sid: str) -> str:
	""" Извлечение PID из SID """
	try   : return sid.split('.')[1]
	except: return ""
