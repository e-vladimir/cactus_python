# КАКТУС: КОНТЕЙНЕР-SQL
# 04 мая 2025

import threading
import time

from   G00_cactus_codes     import  CONNECTION_MANAGEMENT
from   G00_status_codes     import (CODES_COMPLETION,
                                    CODES_PROCESSING)

from   G10_math_linear      import  CalcBetween

from   G20_struct_result    import  T20_StructResult
from   G21_struct_result    import (T21_StructResult_Bool,
                                    T21_StructResult_Int,
                                    T21_StructResult_String,
                                    T21_StructResult_List)

from   G30_cactus_container import C30_Container


class C31_ContainerSQL(C30_Container):
	""" Кактус: Контейнер SQL """

	# Модель данных
	def Init_00(self):
		super().Init_00()

		self._connect_mode       : CONNECTION_MANAGEMENT = CONNECTION_MANAGEMENT.MANUAL
		self._disconnect_mode    : CONNECTION_MANAGEMENT = CONNECTION_MANAGEMENT.MANUAL
		self._disconnect_timeout : int = 10

	def Init_10(self):
		super().Init_10()

		self.disconnector = None

	# Механика данных: Состояния
	def StateConnected(self) -> T21_StructResult_Bool:
		""" Запрос состояния подключения """
		return T21_StructResult_Bool(code     = CODES_COMPLETION.COMPLETED,
		                             subcodes = {CODES_PROCESSING.SKIP},
		                             data     = True)

	# Механика данных: Параметры Автоподключения
	def ConnectMode_Manual(self, flag: bool = None) -> T21_StructResult_Bool | None:
		""" Режим подключения: Ручной """
		if   flag is None: return T21_StructResult_Bool(code = CODES_COMPLETION.COMPLETED,
		                                                data = self._connect_mode == CONNECTION_MANAGEMENT.MANUAL)

		elif flag        :                                     self._connect_mode  = CONNECTION_MANAGEMENT.MANUAL
		return None

	def ConnectMode_Auto(self, flag: bool = None) -> T21_StructResult_Bool | None:
		""" Режим подключения: Автоматически """
		if   flag is None: return T21_StructResult_Bool(code = CODES_COMPLETION.COMPLETED,
		                                                data = self._connect_mode == CONNECTION_MANAGEMENT.AUTO)

		elif flag        :                                     self._connect_mode  = CONNECTION_MANAGEMENT.AUTO
		return None

	# Механика данных: Параметры Автоотключения
	def DisconnectMode_Manual(self, flag: bool = None) -> T21_StructResult_Bool | None:
		""" Режим отключения: Отключено """
		if   flag is None: return T21_StructResult_Bool(code = CODES_COMPLETION.COMPLETED,
		                                                data = self._disconnect_mode == CONNECTION_MANAGEMENT.MANUAL)

		elif flag        :                                     self._disconnect_mode  = CONNECTION_MANAGEMENT.MANUAL
		return None

	def DisconnectMode_Auto(self, flag: bool = None) -> T21_StructResult_Bool | None:
		""" Режим отключения: Автоматически """
		if   flag is None: return T21_StructResult_Bool(code = CODES_COMPLETION.COMPLETED,
		                                                data = self._disconnect_mode == CONNECTION_MANAGEMENT.AUTO)

		elif flag        :                                     self._disconnect_mode  = CONNECTION_MANAGEMENT.AUTO
		return None

	def DisconnectMode_Timeout(self, flag: bool = None) -> T21_StructResult_Bool | None:
		""" Режим отключения: Ожидание """
		if   flag is None: return T21_StructResult_Bool(code = CODES_COMPLETION.COMPLETED,
		                                                data = self._disconnect_mode == CONNECTION_MANAGEMENT.TIMEOUT)

		elif flag        :                                     self._disconnect_mode  = CONNECTION_MANAGEMENT.TIMEOUT
		return None

	def DisconnectTimeout(self, value: int = None) -> T21_StructResult_Int | None:
		""" Задержка отключения """
		if value is None: return T21_StructResult_Int(code = CODES_COMPLETION.COMPLETED,
		                                              data = self._disconnect_timeout)

		self._disconnect_timeout = CalcBetween(3, value, 600)
		return None

	# Механика управления: Управление подключением
	def Connect(self) -> T20_StructResult:
		""" Подключение к контейнеру """
		return T20_StructResult(code     = CODES_COMPLETION.COMPLETED,
		                        subcodes = {CODES_PROCESSING.SKIP})

	def Disconnect(self) -> T20_StructResult:
		""" Отключение от контейнера """
		return T20_StructResult(code     = CODES_COMPLETION.COMPLETED,
		                        subcodes = {CODES_PROCESSING.SKIP})

	# Механика управления: Выполнение SQL
	def ExecSql(self, sql: str) -> T20_StructResult:
		""" Выполнение запроса с кодом """
		return T20_StructResult(code     = CODES_COMPLETION.COMPLETED,
		                        subcodes = {CODES_PROCESSING.SKIP})

	def ExecSqlSelectRowCount(self, sql: str) -> T21_StructResult_Int:
		"""Выполнение запроса с числом строк"""
		return T21_StructResult_Int(code     = CODES_COMPLETION.COMPLETED,
		                            subcodes = {CODES_PROCESSING.SKIP},
		                            data     = 0)

	def ExecSqlSelectSingle(self, sql: str) -> T21_StructResult_String:
		"""Выполнение запроса с получением значения"""
		return T21_StructResult_String(code     = CODES_COMPLETION.COMPLETED,
		                               subcodes = {CODES_PROCESSING.SKIP},
		                               data     = "")

	def ExecSqlSelectVList(self, sql: str) -> T21_StructResult_List:
		"""Выполнение запроса с получением вертикального списка значений"""
		return T21_StructResult_List(code     = CODES_COMPLETION.COMPLETED,
		                             subcodes = {CODES_PROCESSING.SKIP},
		                             data     = [])

	def ExecSqlSelectHList(self, sql: str) -> T21_StructResult_List:
		"""Выполнение запроса с получением горизонтального списка значений"""
		return T21_StructResult_List(code     = CODES_COMPLETION.COMPLETED,
		                             subcodes = {CODES_PROCESSING.SKIP},
		                             data     = [])

	def ExecSqlSelectMatrix(self, sql: str) -> T21_StructResult_List:
		"""Выполнение запроса с получением матрицы"""
		return T21_StructResult_List(code     = CODES_COMPLETION.COMPLETED,
		                             subcodes = {CODES_PROCESSING.SKIP},
		                             data     = [])

	# Логика данных: Управление подключением
	def PrepareConnect(self) -> T21_StructResult_Bool:
		""" Подготовка подключения """
		if   self.ConnectMode_Manual().data :
			pass

		elif self.ConnectMode_Auto().data:
			if not self.StateConnected().data: self.Connect()

		return self.StateConnected()

	def PrepareDisconnect(self) -> T21_StructResult_Bool:
		""" Подготовка отключения """
		if   self.DisconnectMode_Manual().data    :
			pass

		elif self.DisconnectMode_Auto().data   :
			self.Disconnect()

		elif self.DisconnectMode_Timeout().data:
			if self.disconnector is None:
				self.disconnector = C30_ContainerSqlDisconnector(self)
				self.disconnector.start()

			self.disconnector.ResetCounter()

		return self.StateConnected()

	# Логика данных: Управление регистрацией класса
	def RegisterClass(self, idc: str) -> T21_StructResult_Bool:
		""" Регистрация класса структурного объекта """
		return T21_StructResult_Bool(code     = CODES_COMPLETION.COMPLETED,
		                             subcodes = {CODES_PROCESSING.SKIP},
		                             data     = True)

	# Логика управления
	pass


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

		time.sleep(0.001)

		while self.Counter() < self.container.DisconnectTimeout().data:
			time.sleep(1)
			self.IncCounter()

		self.container.Disconnect()
