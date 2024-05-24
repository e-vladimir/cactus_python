# КАКТУС: КОНТРОЛЛЕР КОНТЕЙНЕРОВ
# 2022-12-01

from G00_result_codes         import *
from G20_meta_frame           import C20_MetaFrame
from G30_cactus_struct        import T30_ResultCode
from G31_cactus_struct        import T31_ResultList
from G31_cactus_container_ram import C31_ContainerRAM
from G32_cactus_container_sql import C32_ContainerSQLite, C32_ContainerPostgreSQL


class C30_ControllerContainers(C20_MetaFrame):
	""" Кактус: Контроллер контейнеров """

	def Init_00(self):
		self._containers : dict[str, any] = dict()

	# УПРАВЛЕНИЕ РЕГИСТРАЦИЕЙ КОНТЕЙНЕРА
	def RegisterContainerRAM(self, container_name: str) -> None | C31_ContainerRAM:
		""" Регистрация RAM-Контейнера """
		container = self.GetContainer(container_name)

		if container is not None:
			if container.TypeIsRAM(): return container

			return None

		container = C31_ContainerRAM()
		self._containers[container_name] = container

		return container

	def RegisterContainerSQLite(self, container_name: str) -> None | C32_ContainerSQLite:
		""" Регистрация SQLite-Контейнера """
		container = self.GetContainer(container_name)

		if container is not None:
			if container.TypeIsRAM(): return container

			return None

		container = C32_ContainerSQLite()
		self._containers[container_name] = container

		return container

	def RegisterContainerPostgreSQL(self, container_name: str) -> None | C32_ContainerPostgreSQL:
		""" Регистрация PostgreSQL-Контейнера """
		container = self.GetContainer(container_name)

		if container is not None:
			if container.TypeIsRAM(): return container

			return None

		container = C32_ContainerPostgreSQL()
		self._containers[container_name] = container

		return container

	def UnregisterContainer(self, container_name: str) -> T30_ResultCode:
		""" Отмена регистрации контейнера """
		container = self.GetContainer(container_name)

		if container is None: return T30_ResultCode(RESULT_WARNING_NO_DATA)

		# Отключение контейнера
		if   container.TypeIsSQLite().flag    : container.Disconnect()
		elif container.TypeIsPostgreSQL().flag: container.Disconnect()

		del container

		del self._containers[container_name]

		return T30_ResultCode(RESULT_OK)

	# УПРАВЛЕНИЕ КОНТЕЙНЕРОМ
	def GetContainer(self, container_name: str) -> None | C31_ContainerRAM | C32_ContainerSQLite | C32_ContainerPostgreSQL:
		""" Запрос контейнера """
		return self._containers.get(container_name, None)

	# ЗАПРОСЫ КОНТЕЙНЕРОВ
	def ContainerNames(self) -> T31_ResultList:
		""" Запрос списка названий контейнеров """
		names : list[str] = list(self._containers.keys())
		names.sort()

		if not names: return T31_ResultList(RESULT_WARNING_NO_DATA)

		return T31_ResultList(RESULT_OK, names)


controller_containers = C30_ControllerContainers()
