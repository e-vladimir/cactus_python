# КАКТУС: КОНТРОЛЛЕР КОНТЕЙНЕРОВ
# 25 июн 2024

from G00_status_codes         import (CODES_DATA,
                                      CODES_PROCESSING)

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

		names : list[str]  = list(self._containers.keys())
		names.sort()
		if not names: struct_result.subcodes.add(CODES_DATA.NO_DATA)

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
		struct_result = T21_StructResult_String(data=container_name)

		container     = self.Container(container_name)

		if container is None:
			struct_result.subcodes.add(CODES_DATA.NO_DATA)
			return struct_result

		# Отключение контейнера
		if   container.Type_SQLite().data    : container.Disconnect()
		elif container.Type_PostgreSQL().data: container.Disconnect()

		try:
			del container
			del self._containers[container_name]
		except:
			struct_result.subcodes.add(CODES_PROCESSING.SKIP)

		return struct_result

	# Логика управления
	pass


controller_containers = C30_ControllerContainers()
