# КАКТУС: КОНТРОЛЛЕР КОНТЕЙНЕРОВ
# 31 окт 2024

from G00_status_codes         import (CODES_DATA,
                                      CODES_PROCESSING,
                                      CODES_COMPLETION,
                                      CODES_CACTUS)

from G20_meta_frame           import  C20_MetaFrame
from G21_struct_result        import (T21_StructResult_List,
                                      T21_StructResult_String)

from G31_cactus_container_ram import  C31_ContainerRAM
from G32_cactus_container_sql import (C32_ContainerSQLite,
                                      C32_ContainerPostgreSQL)


class C30_ControllerContainers(C20_MetaFrame):
	""" Кактус: Контроллер контейнеров """

	# Модель данных
	def Init_00(self):
		self._containers : dict[str, any] = dict()

	# Механика данных
	def ContainerNames(self) -> T21_StructResult_List:
		""" Запрос списка названий контейнеров """
		struct_result      = T21_StructResult_List()
		struct_result.code = CODES_COMPLETION.COMPLETED

		names : list[str]  = list(self._containers.keys())
		names.sort()

		match len(names):
			case 0: struct_result.subcodes.add(CODES_DATA.NO_DATA)
			case 1: struct_result.subcodes.add(CODES_DATA.SINGLE)

		struct_result.data = names[:]

		return struct_result

	def Container(self, container_name: str) -> None | C31_ContainerRAM | C32_ContainerSQLite | C32_ContainerPostgreSQL:
		""" Запрос контейнера """
		return self._containers.get(container_name, None)

	# Механика управления
	pass

	# Логика данных: Управление регистрацией контейнера
	def RegisterContainerRAM(self, container_name: str) -> None | C31_ContainerRAM:
		""" Регистрация RAM-Контейнера """
		container = self.Container(container_name)

		if container is not None:
			if container.Type_RAM(): return container

			return None

		container = C31_ContainerRAM()
		self._containers[container_name] = container

		return container

	def RegisterContainerSQLite(self, container_name: str) -> None | C32_ContainerSQLite:
		""" Регистрация SQLite-Контейнера """
		container = self.Container(container_name)

		if container is not None:
			if container.Type_RAM(): return container

			return None

		container = C32_ContainerSQLite()
		self._containers[container_name] = container

		return container

	def RegisterContainerPostgreSQL(self, container_name: str) -> None | C32_ContainerPostgreSQL:
		""" Регистрация PostgreSQL-Контейнера """
		container = self.Container(container_name)

		if container is not None:
			if container.Type_RAM(): return container

			return None

		container = C32_ContainerPostgreSQL()
		self._containers[container_name] = container

		return container

	# Логика данных: Управление отменой регистрации контейнеров
	def UnregisterContainer(self, container_name: str) -> T21_StructResult_String:
		""" Отмена регистрации контейнера """
		container     = self.Container(container_name)

		if container is None:
			return T21_StructResult_String(code     = CODES_COMPLETION.INTERRUPTED,
			                               subcodes = {CODES_CACTUS.NO_CONTAINER},
			                               data     = container_name)

		# Отключение контейнера
		if   container.Type_SQLite().data    : container.Disconnect()
		elif container.Type_PostgreSQL().data: container.Disconnect()

		struct_result = T21_StructResult_String(data=container_name)
		struct_result.code = CODES_COMPLETION.COMPLETED

		try:
			del container
			del self._containers[container_name]
		except:
			struct_result.subcodes.add(CODES_PROCESSING.SKIP)

		return struct_result

	# Логика управления
	pass


controller_containers = C30_ControllerContainers()
