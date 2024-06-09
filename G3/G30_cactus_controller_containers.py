# КАКТУС: КОНТРОЛЛЕР КОНТЕЙНЕРОВ
# 09 июн 2024

from G00_status_codes         import (CODES_COMPLETION,
                                      CODES_DATA)

from G20_meta_frame           import  C20_MetaFrame
from G21_struct_result        import (T21_StructResult_String,
                                      T21_StructResult_List)
from G31_cactus_container_ram import  C31_ContainerRAM
from G32_cactus_container_sql import (C32_ContainerSQLite,
                                      C32_ContainerPostgreSQL)


class C30_ControllerContainers(C20_MetaFrame):
	""" Кактус: Контроллер контейнеров """

	def Init_00(self):
		self._containers : dict[str, any] = dict()

	# УПРАВЛЕНИЕ РЕГИСТРАЦИЕЙ КОНТЕЙНЕРА
	def RegisterContainerRAM(self, container_name: str) -> None | C31_ContainerRAM:
		""" Регистрация RAM-Контейнера """
		container = self.GetContainer(container_name)

		if container is not None:
			if container.Type_RAM(): return container

			return None

		container = C31_ContainerRAM()
		self._containers[container_name] = container

		return container

	def RegisterContainerSQLite(self, container_name: str) -> None | C32_ContainerSQLite:
		""" Регистрация SQLite-Контейнера """
		container = self.GetContainer(container_name)

		if container is not None:
			if container.Type_RAM(): return container

			return None

		container = C32_ContainerSQLite()
		self._containers[container_name] = container

		return container

	def RegisterContainerPostgreSQL(self, container_name: str) -> None | C32_ContainerPostgreSQL:
		""" Регистрация PostgreSQL-Контейнера """
		container = self.GetContainer(container_name)

		if container is not None:
			if container.Type_RAM(): return container

			return None

		container = C32_ContainerPostgreSQL()
		self._containers[container_name] = container

		return container

	def UnregisterContainer(self, container_name: str) -> T21_StructResult_String:
		""" Отмена регистрации контейнера """
		container = self.GetContainer(container_name)

		if container is None: return T21_StructResult_String(code     = CODES_COMPLETION.COMPLETED,
		                                                     subcodes = [CODES_DATA.NO_DATA],
		                                                     data     = container_name)

		# Отключение контейнера
		if   container.Type_SQLite().data    : container.Disconnect()
		elif container.Type_PostgreSQL().data: container.Disconnect()

		del container

		del self._containers[container_name]

		return T21_StructResult_String(code     = CODES_COMPLETION.COMPLETED,
		                               subcodes = [],
		                               data     = container_name)

	# УПРАВЛЕНИЕ КОНТЕЙНЕРОМ
	def GetContainer(self, container_name: str) -> None | C31_ContainerRAM | C32_ContainerSQLite | C32_ContainerPostgreSQL:
		""" Запрос контейнера """
		return self._containers.get(container_name, None)

	# ЗАПРОСЫ КОНТЕЙНЕРОВ
	def ContainerNames(self) -> T21_StructResult_List:
		""" Запрос списка названий контейнеров """
		names : list[str] = list(self._containers.keys())
		names.sort()

		if not names: return T21_StructResult_List(code     = CODES_COMPLETION.COMPLETED,
		                                           subcodes = [CODES_DATA.NO_DATA],
		                                           data     = [])

		return T21_StructResult_List(code     = CODES_COMPLETION.COMPLETED,
									 subcodes = [],
									 data     = names)


controller_containers = C30_ControllerContainers()
