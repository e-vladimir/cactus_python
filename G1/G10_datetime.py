# ПАЛИТРА ИНСТРУМЕТОВ ДЛЯ РАБОТЫ С ДАТОЙ-ВРЕМЕНЕМ
# 11 июн 2024

import datetime
import pytz
import time


# ДАТА-ВРЕМЯ
def DTime(dy, dm, dd, hh, hm, hs, utc_shift: int | str = None):
	""" Создание datetime с указанным часовым поясом """
	if        utc_shift  is None:
		return datetime.datetime(year=dy, month=dm, day=dd, hour=hh, minute=hm, second=hs)

	elif type(utc_shift) is int :
		return datetime.datetime(year=dy, month=dm, day=dd, hour=hh, minute=hm, second=hs, tzinfo=datetime.timezone(datetime.timedelta(minutes=utc_shift)))

	elif type(utc_shift) is str :
		try   : return datetime.datetime(year=dy, month=dm, day=dd, hour=hh, minute=hm, second=hs, tzinfo=pytz.timezone(utc_shift))
		except: return datetime.datetime(year=dy, month=dm, day=dd, hour=hh, minute=hm, second=hs)


# UNIX-ВРЕМЯ
def CurrentUTime() -> int:
	""" Получение текущего времени в UNIX-формате """
	return int(time.time())


# ТЕКУЩИЕ ДАННЫЕ
def CurrentDTime(utc_shift: int | str = None):
	""" Текущее значение DTime """
	if        utc_shift  is None:
		return datetime.datetime.now()

	elif type(utc_shift) is int :
		return datetime.datetime.now(datetime.timezone(datetime.timedelta(minutes=utc_shift)))

	elif type(utc_shift) is str :
		try   : return datetime.datetime.now(pytz.timezone(utc_shift))
		except: return datetime.datetime.now()


def CurrentDayOfWeek(utc_shift: int | str = 0):
	""" Текущий день недели [1..7] """
	return CurrentDTime(utc_shift).weekday() + 1


def CurrentDy(utc_shift : int | str = None):
	""" Текущий час """
	return CurrentDTime(utc_shift).day


def CurrentDm(utc_shift : int | str = None):
	""" Текущая минута """
	return CurrentDTime(utc_shift).month


def CurrentDd(utc_shift : int | str = None):
	""" Текущая секунда """
	return CurrentDTime(utc_shift).day


def CurrentHh(utc_shift : int | str = None):
	""" Текущий час """
	return CurrentDTime(utc_shift).hour


def CurrentHm(utc_shift : int | str = None):
	""" Текущая минута """
	return CurrentDTime(utc_shift).minute


def CurrentHs(utc_shift : int | str = None):
	""" Текущая секунда """
	return CurrentDTime(utc_shift).second


# СМЕЩЕНИЕ ДАТ
def CalcDyDmByShiftDm(dy: int, dm: int, shift: int) -> tuple[int, int]:
	""" Вычисление года и месяца при смещении по месяцу """
	_year  : int = dy
	_month : int = dm - 1
	_month      += shift

	if _month < 0: _month -= 12

	_year  += (_month//abs(_month)) * (abs(_month) // 12)
	_month  = _month  % 12
	_month += 1

	return _year, _month


# ПРЕОБРАЗОВАНИЕ
def UTimeToDTime(in_utime: int, utc_shift : int | str = None):
	""" Конвертация UTime в DTime """
	if        utc_shift  is None:
		return datetime.datetime.fromtimestamp(in_utime)

	elif type(utc_shift) is int :
		return datetime.datetime.fromtimestamp(in_utime, datetime.timezone(datetime.timedelta(minutes=utc_shift)))

	elif type(utc_shift) is str :
		try   : return datetime.datetime.fromtimestamp(in_utime, pytz.timezone(utc_shift))
		except: return datetime.datetime.fromtimestamp(in_utime)


def DTimeToUTime(in_dtime: datetime.datetime):
	""" Конвертация DTime в UTime """
	return int(in_dtime.timestamp())
