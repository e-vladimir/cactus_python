# КАКТУС: КОНТЕЙНЕР-SQL
# 2022-12-01

import threading
import time

from   G00_result_codes     import RESULT_OK,                     \
								   RESULT_WARNING_NOT_IMPLEMENTED
from   G10_math_linear      import CalcBetween
from   G30_cactus_container import C30_Container
from   G30_cactus_struct    import T30_ResultCode
from   G31_cactus_struct    import T31_ResultBool,   \
								   T31_ResultInt,    \
								   T31_ResultString, \
								   T31_ResultList


# КАТАЛОГИ: АВТОПОДКЛЮЧЕНИЕ
MODE_CONNECT_OFF    : int = 0
MODE_CONNECT_AUTO   : int = 1
MODE_CONNECT_TIMEOUT: int = 2


# 2022-11-10
class C31_ContainerSQL(C30_Container):
	""" Кактус: Контейнер SQL """

	def Init_00(self):
		super().Init_00()

		self._autoconnect_mode            : int = MODE_CONNECT_OFF
		self._autodisconnect_mode         : int = MODE_CONNECT_OFF
		self._autodisconnect_timeout_value: int = 10

	def Init_10(self):
		super().Init_10()

		self.disconnector = None

	# УПРАВЛЕНИЕ ПОДКЛЮЧЕНИЕМ
	def Connect(self) -> T31_ResultBool:
		""" Подключение к контейнеру """
		return T31_ResultBool(RESULT_WARNING_NOT_IMPLEMENTED)

	def Disconnect(self) -> T31_ResultBool:
		""" Отключение от контейнера """
		return T31_ResultBool(RESULT_WARNING_NOT_IMPLEMENTED)

	def PrepareConnect(self) -> T31_ResultBool:
		""" Подготовка подключения """
		if   self.AutoconnectIsOff().flag : pass
		elif self.AutoconnectIsAuto().flag:
			if not self.ConnectionState().flag: self.Connect()

		return self.ConnectionState()

	def PrepareDisconnect(self) -> T31_ResultBool:
		""" Подготовка отключения """
		if   self.AutodisconnectIsOff().flag    : pass
		elif self.AutodisconnectIsAuto().flag   : self.Disconnect()
		elif self.AutodisconnectIsTimeout().flag:
			if self.disconnector is None:
				self.disconnector = C30_ContainerSqlDisconnector(self)
				self.disconnector.start()

			self.disconnector.ResetCounter()

		return self.ConnectionState()

	# ЗАПРОС СОСТОЯНИЯ ПОДКЛЮЧЕНИЯ
	def ConnectionState(self) -> T31_ResultBool:
		""" Запрос состояния подключения """
		return T31_ResultBool(RESULT_WARNING_NOT_IMPLEMENTED)

	# УПРАВЛЕНИЕ АВТОПОДКЛЮЧЕНИЕМ
	def AutoconnectIsOff(self, flag: bool = None) -> T31_ResultBool:
		""" Проверка/Установка режима автоподключения: Отключено """
		if   flag is None: return T31_ResultBool(RESULT_OK, self._autoconnect_mode == MODE_CONNECT_OFF)
		elif flag        :                                  self._autoconnect_mode  = MODE_CONNECT_OFF

	def AutoconnectIsAuto(self, flag: bool = None) -> T31_ResultBool:
		""" Проверка/Установка режима автоподключения: Автоматически """
		if   flag is None: return T31_ResultBool(RESULT_OK, self._autoconnect_mode == MODE_CONNECT_AUTO)
		elif flag        :                                  self._autoconnect_mode  = MODE_CONNECT_AUTO

	# УПРАВЛЕНИЕ АВТООТКЛЮЧЕНИЕМ
	def AutodisconnectIsOff(self, flag: bool = None) -> T31_ResultBool:
		""" Проверка/Установка режима автоотключения: Отключено """
		if   flag is None: return T31_ResultBool(RESULT_OK, self._autodisconnect_mode == MODE_CONNECT_OFF)
		elif flag        :                                  self._autodisconnect_mode  = MODE_CONNECT_OFF

	def AutodisconnectIsAuto(self, flag: bool = None) -> T31_ResultBool:
		""" Проверка/Установка режима автоотключения: Автоматически """
		if   flag is None: return T31_ResultBool(RESULT_OK, self._autodisconnect_mode == MODE_CONNECT_AUTO)
		elif flag        :                                  self._autodisconnect_mode  = MODE_CONNECT_AUTO

	def AutodisconnectIsTimeout(self, flag: bool = None) -> T31_ResultBool:
		""" Проверка/Установка режима автоотключения: Ожидание """
		if   flag is None: return T31_ResultBool(RESULT_OK, self._autodisconnect_mode == MODE_CONNECT_TIMEOUT)
		elif flag        :                                  self._autodisconnect_mode  = MODE_CONNECT_TIMEOUT

	# TODO: Переименовать метод
	def AutodisconnectTimeoutValue(self, value: int = None) -> T31_ResultInt:
		""" Проверка/Установка значения ожидания """
		if value is None: return T31_ResultInt(RESULT_OK, self._autodisconnect_timeout_value)

		self._autodisconnect_timeout_value = CalcBetween(3, value, 600)

	# УПРАВЛЕНИЕ РЕГИСТРАЦИЕЙ КЛАССА
	def RegisterClass(self, oci: str) -> T31_ResultBool:
		""" Регистрация класса структурного объекта """
		return T31_ResultBool(RESULT_WARNING_NOT_IMPLEMENTED)

	# ВЫПОЛНЕНИЕ ЗАПРОСОВ
	def ExecSql(self, sql: str) -> T30_ResultCode:
		""" Выполнение запроса с кодом """
		return T30_ResultCode(RESULT_WARNING_NOT_IMPLEMENTED)

	def ExecSqlSelectRowCount(self, sql: str) -> T31_ResultInt:
		"""Выполнение запроса с числом строк"""
		return T31_ResultInt(RESULT_WARNING_NOT_IMPLEMENTED)

	def ExecSqlSelectSingle(self, sql: str) -> T31_ResultString:
		"""Выполнение запроса с получением значения"""
		return T31_ResultString(RESULT_WARNING_NOT_IMPLEMENTED)

	def ExecSqlSelectVList(self, sql: str) -> T31_ResultList:
		"""Выполнение запроса с получением вертикального списка значений"""
		return T31_ResultList(RESULT_WARNING_NOT_IMPLEMENTED)

	def ExecSqlSelectHList(self, sql: str) -> T31_ResultList:
		"""Выполнение запроса с получением горизонтального списка значений"""
		return T31_ResultList(RESULT_WARNING_NOT_IMPLEMENTED)

	def ExecSqlSelectMatrix(self, sql: str) -> T31_ResultList:
		"""Выполнение запроса с получением матрицы"""
		return T31_ResultList(RESULT_WARNING_NOT_IMPLEMENTED)


# 2022-11-10
class C30_ContainerSqlDisconnector(threading.Thread):
	""" Обработчик автоотключения """

	def __init__(self, container_sql):
		threading.Thread.__init__(self)

		self._counter : int              = 0

		self.container                   = container_sql
		self.daemon   : bool             = True

	def Counter(self, value: int = None) -> int:
		""" Чтение/Запись счетчика тактов """
		if value is not None: self._counter = value

		return self._counter

	def IncCounter(self) -> int:
		""" +1 к счётчику """
		return self.Counter(self.Counter() + 1)

	def ResetCounter(self):
		""" Сброс счётчика """
		self.Counter(0)

	def run(self) -> None:
		""" Основной обработчик потока """
		if self.container is None: return

		while self.Counter() < self.container.AutodisconnectTimeoutValue().value:
			time.sleep(1)
			self.IncCounter()

		self.container.Disconnect()
