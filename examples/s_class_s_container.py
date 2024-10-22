# ПРИМЕР РАБОТЫ С КАКТУСОМ
# Один класс - Один контейнер

import random

from   datetime                         import datetime

from   G30_cactus_controller_containers import controller_containers
from   G30_cactus_frame                 import C30_StructFrame, C30_StructField


CONTAINER_NAME = "База SQLite"


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
	def Text(self, text: str = None) -> str:
		""" Текст сообщения """
		if text is None: return self.f_text.ToString(CONTAINER_NAME).data
		else           :        self.f_text.FromString(CONTAINER_NAME, text)

	def Date(self, date: datetime = None) -> datetime:
		""" Дата сообщения """
		if date is None: return self.f_date.ToDatetime(CONTAINER_NAME).data
		else           :        self.f_date.FromDatetime(CONTAINER_NAME, date)

	def Number(self, value: int = None) -> int:
		""" Номер сообщения """
		if value is None: return self.f_number.ToInteger(CONTAINER_NAME).data
		else            :        self.f_number.FromInteger(CONTAINER_NAME, value)

	# L7
	pass

	# L8
	pass

	# L9
	pass


container_local = controller_containers.RegisterContainerSQLite(CONTAINER_NAME)
container_local.OptionsFilename("test")
container_local.Connect()

CMsg.RegisterClass(CONTAINER_NAME)

message         = CMsg()
message.GenerateIdo()
message.RegisterObject(CONTAINER_NAME)
message.Date(datetime.now())
message.Text(f"Тестовое сообщение")
message.Number(random.randint(1, 10000))

idos : list[str] = CMsg.Idos(CONTAINER_NAME).data

print(f"Сообщений в БД: {len(idos)}")

print("")
for index_msg, ido in enumerate(idos):
	msg = CMsg(ido)

	print(f"Сообщение #{msg.Number():03d} от {msg.Date()}: {msg.Text()}")


print("")
print("Удаление сообщений с номером < 4000")
for ido in idos:
	msg = CMsg(ido)

	if msg.Number() > 4000: continue

	print(f"Удалено сообщение #{msg.Number():03d}")
	msg.DeleteObject(CONTAINER_NAME)

print("")
print(f"Сообщений в БД: {len(CMsg.Idos(CONTAINER_NAME).data)}")
