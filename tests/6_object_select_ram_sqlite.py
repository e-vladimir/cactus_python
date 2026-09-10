# ТЕСТИРОВАНИЕ ВЫБОРКИ ДАННЫХ
# 08 сен 2026

import os
import time

from   pprint                           import pprint

from   G30_cactus_controller_containers import ControllerContainers
from   G30_cactus_datafilters           import C30_FilterLinear1D
from   G30_cactus_frames                import C30_StructField, C30_StructFrame


CONTAINER_RAM    = "RAM"
CONTAINER_SQLITE = "SQLITE"


print("Тест Выборки данных")
print("")


class CObj(C30_StructFrame):
	_idc = "Сообщение"

	def Init_10(self):
		super().Init_10()

		self.f_field_1 = C30_StructField(self, "Поле-1")
		self.f_field_2 = C30_StructField(self, "Поле-2")


try: os.remove("./data.sqlite")
except: pass

container_ram = ControllerContainers.RegisterContainerRAM(CONTAINER_RAM)
container_sql = ControllerContainers.RegisterContainerRAM(CONTAINER_SQLITE)

CObj.RegisterClass(CONTAINER_SQLITE)

message = CObj()

for idx in range(10):
	message.Ido(f"{idx:03d}")
	message.RegisterObject(CONTAINER_RAM)

	message.f_field_1.FromString(CONTAINER_RAM, "Белый объект" if idx < 5 else "Красный объект")

	if idx < 5: message.f_field_2.FromInteger(CONTAINER_RAM, idx)

	message.CopyToContainer(CONTAINER_RAM, CONTAINER_SQLITE)


print("Проверка выборки из контейнера RAM")

time_0 = time.time()

filter_messages = C30_FilterLinear1D(message.Idc().data)
filter_messages.FilterIdpVlpByEqual(message.f_field_2.Idp().data, "2")

result          = filter_messages.Capture(CONTAINER_RAM)
idos            = sorted(filter_messages.Idos().data)

pprint(container_ram._s_cells)

print(result)
print(idos)

# time_1 = time.time()
# check  = result.code == CODES_COMPLETION.COMPLETED
# check &= CODES_DATA.NO_DATA in result.subcodes
# check &= result.data == 0
# print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Проверка ситуации Данных нет без установки значения по-умолчанию")
# if not check: print(f"                  {result.code} {result.subcodes}\n")
