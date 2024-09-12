# ПАЛИТРА ИНСТРУМЕТОВ ДЛЯ РАБОТЫ С ДАТОЙ-ВРЕМЕНЕМ
# 20 авг 2024

import datetime
import pytz
import time


# ДАТА-ВРЕМЯ
def DTime(dy, dm, dd, th, tm, ts, utc_shift: int | str = None):
	""" Создание datetime с указанным часовым поясом """
	if        utc_shift  is None:
		return datetime.datetime(year=dy, month=dm, day=dd, hour=th, minute=tm, second=ts)

	elif type(utc_shift) is int :
		return datetime.datetime(year=dy, month=dm, day=dd, hour=th, minute=tm, second=ts, tzinfo=datetime.timezone(datetime.timedelta(minutes=utc_shift)))

	elif type(utc_shift) is str :
		try   : return datetime.datetime(year=dy, month=dm, day=dd, hour=th, minute=tm, second=ts, tzinfo=pytz.timezone(utc_shift))
		except: return datetime.datetime(year=dy, month=dm, day=dd, hour=th, minute=tm, second=ts)


def CurrentDTime(utc_shift: int | str = None):
	""" Текущее значение DTime """
	if        utc_shift  is None:
		return datetime.datetime.now()

	elif type(utc_shift) is int :
		return datetime.datetime.now(datetime.timezone(datetime.timedelta(minutes=utc_shift)))

	elif type(utc_shift) is str :
		try   : return datetime.datetime.now(pytz.timezone(utc_shift))
		except: return datetime.datetime.now()


# UNIX-ВРЕМЯ
def CurrentUTime() -> int:
	""" Получение текущего времени в UNIX-формате """
	return int(time.time())


# ТЕКУЩИЕ ДАННЫЕ
def CurrentDayOfWeek(utc_shift: int | str = 0):
	""" Текущий день недели [1..7] """
	return CurrentDTime(utc_shift).weekday() + 1


def CurrentDy(utc_shift : int | str = None):
	""" Текущий час """
	return CurrentDTime(utc_shift).year


def CurrentDm(utc_shift : int | str = None):
	""" Текущая минута """
	return CurrentDTime(utc_shift).month


def CurrentDd(utc_shift : int | str = None):
	""" Текущая секунда """
	return CurrentDTime(utc_shift).day


def CurrentTh(utc_shift : int | str = None):
	""" Текущий час """
	return CurrentDTime(utc_shift).hour


def CurrentTm(utc_shift : int | str = None):
	""" Текущая минута """
	return CurrentDTime(utc_shift).minute


def CurrentTs(utc_shift : int | str = None):
	""" Текущая секунда """
	return CurrentDTime(utc_shift).second


# СМЕЩЕНИЕ ДАТ
def CalcDyDmByShiftDm(dy: int, dm: int, shift: int) -> tuple[int, int]:
	""" Вычисление года и месяца (1..12) при смещении по месяцу """
	_year  : int = dy
	_month : int = dm
	_month      -= 1
	_month      += shift

	if _month < 1: _month -= 12

	_year  += (_month//abs(_month)) * (abs(_month) // (13 if shift < 0 else 12))
	_month  = _month  % 12
	_month += 1

	return _year, _month
