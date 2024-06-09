# КАКТУС: КОНТЕЙНЕР-SQL
# 09 июн 2024

import threading
import time

from   G00_cactus_codes     import CONNECTION_MANAGEMENT
from   G00_status_codes     import *

from   G10_math_linear      import CalcBetween
from   G21_struct_result    import *
from   G30_cactus_container import C30_Container


# 2022-11-10
class C31_ContainerSQL(C30_Container):
	""" Кактус: Контейнер SQL """

	def Init_00(self):
		super().Init_00()

		self._connect_mode       : CONNECTION_MANAGEMENT = CONNECTION_MANAGEMENT.OFF
		self._disconnect_mode    : CONNECTION_MANAGEMENT = CONNECTION_MANAGEMENT.OFF
		self._disconnect_timeout : int = 10

	def Init_10(self):
		super().Init_10()

		self.disconnector = None

	# УПРАВЛЕНИЕ ПОДКЛЮЧЕНИЕМ
	def Connect(self) -> T21_StructResult_Bool:
		""" Подключение к контейнеру """
		return T21_StructResult_Bool(code     = CODES_COMPLETION.COMPLETED,
		                             subcodes = [CODES_PROCESSING.SKIP],
		                             data     = True)

	def Disconnect(self) -> T21_StructResult_Bool:
		""" Отключение от контейнера """
		return T21_StructResult_Bool(code     = CODES_COMPLETION.COMPLETED,
		                             subcodes = [CODES_PROCESSING.SKIP],
		                             data     = True)

	def PrepareConnect(self) -> T21_StructResult_Bool:
		""" Подготовка подключения """
		if   self.ConnectMode_Off().data :
			pass

		elif self.ConnectMode_Auto().data:
			if not self.ConnectionState().data: self.Connect()

		return self.ConnectionState()

	def PrepareDisconnect(self) -> T21_StructResult_Bool:
		""" Подготовка отключения """
		if   self.DisconnectMode_Off().data    :
			pass

		elif self.DisconnectMode_Auto().data   :
			self.Disconnect()

		elif self.DisconnectMode_Timeout().data:
			if self.disconnector is None:
				self.disconnector = C30_ContainerSqlDisconnector(self)
				self.disconnector.start()

			self.disconnector.ResetCounter()

		return self.ConnectionState()

	# ЗАПРОС СОСТОЯНИЯ ПОДКЛЮЧЕНИЯ
	def ConnectionState(self) -> T21_StructResult_Bool:
		""" Запрос состояния подключения """
		return T21_StructResult_Bool(code     = CODES_COMPLETION.COMPLETED,
		                             subcodes = [CODES_PROCESSING.SKIP],
		                             data     = True)

	# УПРАВЛЕНИЕ АВТОПОДКЛЮЧЕНИЕМ
	def ConnectMode_Off(self, flag: bool = None) -> T21_StructResult_Bool:
		""" Режим подключения: Отключено """
		if   flag is None: return T21_StructResult_Bool(code = CODES_COMPLETION.COMPLETED,
		                                                data = self._connect_mode == CONNECTION_MANAGEMENT.OFF)

		elif flag        :                                     self._connect_mode  = CONNECTION_MANAGEMENT.OFF

	def ConnectMode_Auto(self, flag: bool = None) -> T21_StructResult_Bool:
		""" Режим подключения: Автоматически """
		if   flag is None: return T21_StructResult_Bool(code = CODES_COMPLETION.COMPLETED,
		                                                data = self._connect_mode == CONNECTION_MANAGEMENT.AUTO)

		elif flag        :                                     self._connect_mode  = CONNECTION_MANAGEMENT.AUTO

	# УПРАВЛЕНИЕ АВТООТКЛЮЧЕНИЕМ
	def DisconnectMode_Off(self, flag: bool = None) -> T21_StructResult_Bool:
		""" Режим отключения: Отключено """
		if   flag is None: return T21_StructResult_Bool(code = CODES_COMPLETION.COMPLETED,
		                                                data = self._disconnect_mode == CONNECTION_MANAGEMENT.OFF)

		elif flag        :                                     self._disconnect_mode  = CONNECTION_MANAGEMENT.OFF

	def DisconnectMode_Auto(self, flag: bool = None) -> T21_StructResult_Bool:
		""" Режим отключения: Автоматически """
		if   flag is None: return T21_StructResult_Bool(code = CODES_COMPLETION.COMPLETED,
		                                                data = self._disconnect_mode == CONNECTION_MANAGEMENT.AUTO)

		elif flag        :                                     self._disconnect_mode  = CONNECTION_MANAGEMENT.AUTO

	def DisconnectMode_Timeout(self, flag: bool = None) -> T21_StructResult_Bool:
		""" Режим отключения: Ожидание """
		if   flag is None: return T21_StructResult_Bool(code = CODES_COMPLETION.COMPLETED,
		                                                data = self._disconnect_mode == CONNECTION_MANAGEMENT.TIMEOUT)

		elif flag        :                                     self._disconnect_mode  = CONNECTION_MANAGEMENT.TIMEOUT

	def DisconnectTimeout(self, value: int = None) -> int:
		""" Задержка отключения """
		if value is None: return self._disconnect_timeout
		else            :	     self._disconnect_timeout = CalcBetween(3, value, 600)

	# УПРАВЛЕНИЕ РЕГИСТРАЦИЕЙ КЛАССА
	def RegisterClass(self, oci: str) -> T21_StructResult_Bool:
		""" Регистрация класса структурного объекта """
		return T21_StructResult_Bool(code     = CODES_COMPLETION.COMPLETED,
		                             subcodes = [CODES_PROCESSING.SKIP],
		                             data     = True)

	# ВЫПОЛНЕНИЕ ЗАПРОСОВ
	def ExecSql(self, sql: str) -> T20_StructResult:
		""" Выполнение запроса с кодом """
		return T20_StructResult(code     = CODES_COMPLETION.COMPLETED,
		                        subcodes = [CODES_PROCESSING.SKIP])

	def ExecSqlSelectRowCount(self, sql: str) -> T21_StructResult_Int:
		"""Выполнение запроса с числом строк"""
		return T21_StructResult_Int(code     = CODES_COMPLETION.COMPLETED,
		                            subcodes = [CODES_PROCESSING.SKIP],
		                            data     = 0)

	def ExecSqlSelectSingle(self, sql: str) -> T21_StructResult_String:
		"""Выполнение запроса с получением значения"""
		return T21_StructResult_String(code     = CODES_COMPLETION.COMPLETED,
		                               subcodes = [CODES_PROCESSING.SKIP],
		                               data     = "")

	def ExecSqlSelectVList(self, sql: str) -> T21_StructResult_List:
		"""Выполнение запроса с получением вертикального списка значений"""
		return T21_StructResult_List(code     = CODES_COMPLETION.COMPLETED,
		                             subcodes = [CODES_PROCESSING.SKIP],
		                             data     = [])

	def ExecSqlSelectHList(self, sql: str) -> T21_StructResult_List:
		"""Выполнение запроса с получением горизонтального списка значений"""
		return T21_StructResult_List(code     = CODES_COMPLETION.COMPLETED,
		                             subcodes = [CODES_PROCESSING.SKIP],
		                             data     = [])

	def ExecSqlSelectMatrix(self, sql: str) -> T21_StructResult_List:
		"""Выполнение запроса с получением матрицы"""
		return T21_StructResult_List(code     = CODES_COMPLETION.COMPLETED,
		                             subcodes = [CODES_PROCESSING.SKIP],
		                             data     = [])


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

		while self.Counter() < self.container.DisconnectTimeout().value:
			time.sleep(1)
			self.IncCounter()

		self.container.Disconnect()
