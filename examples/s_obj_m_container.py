# ПРИМЕР РАБОТЫ С КАКТУСОМ
# Один объект - Несколько контейнеров

import random

from   datetime                         import datetime

from   G30_cactus_controller_containers import ControllerContainers
from   G30_cactus_frames                 import C30_StructFrame, C30_StructField


CONTAINER_NAME_1 = "db_1"
CONTAINER_NAME_2 = "db_2"


class CMsg(C30_StructFrame):
	_idc = "message"

	# L4
	def Init_10(self):
		super().Init_10()

		self.f_text   = C30_StructField(self, "Текст сообщения")
		self.f_date   = C30_StructField(self, "Дата сообщения")
		self.f_number = C30_StructField(self, "Номер сообщения")

	# L5
	pass

	# L6
	def Text(self, text: str = None, container_2: bool = False) -> str:
		""" Текст сообщения """
		if text is None: return self.f_text.ToString(CONTAINER_NAME_1 if not container_2 else CONTAINER_NAME_2).data
		else           :        self.f_text.FromString(CONTAINER_NAME_1 if not container_2 else CONTAINER_NAME_2, text)

	def Date(self, date: datetime = None) -> datetime:
		""" Дата сообщения """
		if date is None: return self.f_date.ToDatetime(CONTAINER_NAME_2).data
		else           :        self.f_date.FromDatetime(CONTAINER_NAME_2, date)

	def Number(self, value: int = None) -> int:
		""" Номер сообщения """
		if value is None: return self.f_number.ToInteger(CONTAINER_NAME_1).data
		else            :        self.f_number.FromInteger(CONTAINER_NAME_1, value)

	# L7
	pass

	# L8
	pass

	# L9
	pass


container_1 = ControllerContainers.RegisterContainerSQLite(CONTAINER_NAME_1)
container_1.OptionsFilename("db1")
container_1.Connect()

container_2 = ControllerContainers.RegisterContainerSQLite(CONTAINER_NAME_2)
container_2.OptionsFilename("db2")
container_2.Connect()

CMsg.RegisterClass(CONTAINER_NAME_1)
CMsg.RegisterClass(CONTAINER_NAME_2)

message         = CMsg()
message.GenerateIdo()
message.RegisterObject(CONTAINER_NAME_1)
message.RegisterObject(CONTAINER_NAME_2)
message.Date(datetime.now())
message.Text(f"Тестовое сообщение в контейнере 1", False)
message.Text(f"jgiuSDGbj2r9g", True)
message.Number(random.randint(1, 10000))

print(f"Сообщение #{message.Number():05d}")
print(f"Дата: {message.Date()}")
print(f"Текст в контейнере 1: {message.Text(container_2=False)}")
print(f"Текст в контейнере 2: {message.Text(container_2=True)}")
