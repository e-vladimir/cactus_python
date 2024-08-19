# КОНВЕРТОР: ФОРМАТЫ
# 18 авг 2024

import datetime
import pytz

from   typing   import Optional


def BooleanToString(flag: bool) -> str:
	""" Преобразование логических значений в строку """
	return '1' if flag else '0'


def StringToBoolean(text: str) -> bool:
	""" Преобразование строки в логическое значение """
	if   text == '1'   : return True
	elif text == '+'   : return True
	elif text == "True": return True
	elif text == "Yes" : return True

	return False


def DatetimeToString(dtime: datetime.datetime) -> str:
	""" Преобразование Datetime в UNIX-формат строки """
	return f"{int(dtime.timestamp())}"


def StringToDateTime(text: str) -> Optional[datetime.datetime]:
	""" Преобразование строки в Datetime по нескольким шаблонам """
	# Подбор преобразования из UNIX формата
	try   : return datetime.datetime.fromtimestamp(int(text))
	except: pass

	# Подбор преобразования из формата YYYY-MM-DD HH:MM:SS
	try   : return datetime.datetime.strptime(text.replace('/', '-'), "%Y-%m-%d, %H:%M:%S")
	except: pass

	return None


def StringToInteger(text: str) -> int:
	""" Преобразование строки в целое число """
	return int(float(text.replace(',', '.').replace(' ', '')))


def StringToFloat(text: str) -> float:
	""" Преобразование строки в дробное число """
	return float(text.replace(',', '.'))


def StringsToIntegers(texts: [str]) -> list[int]:
	""" Преобразование строк в целые числа """
	return list(map(StringToInteger, texts))


def StringsToFloats(texts: [str]) -> list[float]:
	""" Преобразование строк в дробные числа """
	return list(map(StringToFloat, texts))


def StringsToBooleans(texts: [str]) -> list[float]:
	""" Преобразование строк в логические значения """
	return list(map(StringToBoolean, texts))


def StringsToDatetimes(texts: [str]) -> list[datetime.datetime]:
	""" Преобразование строк в формат даты/времени """
	return list(map(StringToDateTime, texts))


def FloatToString(value: float) -> str:
	""" Число с плавающей точкой в текст с точностью 0.00000 """
	return f"{value:0.5f}"


def AnyToString(value: str | int | float | bool) -> str:
	""" Преобразование любого типа данных в строковый тип с заданных форматом """
	if type(value) is str  : return value
	if type(value) is int  : return f"{value}"
	if type(value) is float: return FloatToString(value)
	if type(value) is bool : return '1' if value else '0'

	return ""


def AnyToStrings(values: list[str] | list[int] | list[float] | list[bool]) -> list[str]:
	""" Преобразование списка любых типов данных в список строк """
	return list(map(AnyToString, values))


def StringToIntegerOrNone(text: str) -> int | None:
	"""  Расширенная конвертация строки в число """
	try   : return int(text)
	except: pass

	return None


def UTimeToDTime(in_utime: int, utc_shift : int | str = None) -> datetime.datetime:
	""" Конвертация UTime в DTime """
	if        utc_shift  is None:
		return datetime.datetime.fromtimestamp(in_utime)

	elif type(utc_shift) is int :
		return datetime.datetime.fromtimestamp(in_utime, datetime.timezone(datetime.timedelta(minutes=utc_shift)))

	elif type(utc_shift) is str :
		try   : return datetime.datetime.fromtimestamp(in_utime, pytz.timezone(utc_shift))
		except: return datetime.datetime.fromtimestamp(in_utime)


def DTimeToUTime(in_dtime: datetime.datetime) -> int:
	""" Конвертация DTime в UTime """
	return int(in_dtime.timestamp())
