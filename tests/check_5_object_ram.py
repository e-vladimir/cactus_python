# ТЕСТИРОВАНИЕ СТРУКТУРНОГО ОБЪЕКТА С КОНТЕЙНЕРОМ RAM
# 24 окт 2024

import time
import datetime

import pytest

from   G00_status_codes                 import CODES_COMPLETION

from   G30_cactus_controller_containers import controller_containers
from   G30_cactus_frame                 import C30_StructFrame, C30_StructField

CONTAINER_RAM = "RAM"


class CMessage(C30_StructFrame):
	_idc = "Сообщение"

	def Init_10(self):
		super().Init_10()

		self.f_number = C30_StructField(self, "Номер сообщения")
		self.f_text   = C30_StructField(self, "Текст сообщения")


@pytest.mark.default
@pytest.mark.ram
def test_object_ram():
	controller_containers.RegisterContainerRAM(CONTAINER_RAM)

	message = CMessage()
	message.GenerateIdo()

	time_0 = time.time()
	result = message.CheckRegisterObject(CONTAINER_RAM)
	time_1 = time.time()
	check  = result.code == CODES_COMPLETION.COMPLETED
	check &= result.data == False
	print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Проверка регистрации объекта")
	if not check: print(f"                  {result.code} {result.subcodes}\n")
	assert check

	time_0 = time.time()
	result = message.f_number.ToBoolean(CONTAINER_RAM)
	time_1 = time.time()
	check  = result.code == CODES_COMPLETION.INTERRUPTED
	print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Чтение несуществующих данных в формате Boolean")
	if not check: print(f"                  {result.code} {result.subcodes}\n")
	assert check

	time_0 = time.time()
	result = message.f_number.ToDatetime(CONTAINER_RAM)
	time_1 = time.time()
	check  = result.code == CODES_COMPLETION.INTERRUPTED
	print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Чтение несуществующих данных в формате DateTime")
	if not check: print(f"                  {result.code} {result.subcodes}\n")
	assert check

	time_0 = time.time()
	result = message.f_number.ToInteger(CONTAINER_RAM)
	time_1 = time.time()
	check  = result.code == CODES_COMPLETION.INTERRUPTED
	print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Чтение несуществующих данных в формате Integer")
	if not check: print(f"                  {result.code} {result.subcodes}\n")
	assert check

	time_0 = time.time()
	result = message.f_number.ToFloat(CONTAINER_RAM)
	time_1 = time.time()
	check  = result.code == CODES_COMPLETION.INTERRUPTED
	print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Чтение несуществующих данных в формате Float")
	if not check: print(f"                  {result.code} {result.subcodes}\n")
	assert check

	time_0 = time.time()
	result = message.f_number.ToString(CONTAINER_RAM)
	time_1 = time.time()
	check  = result.code == CODES_COMPLETION.INTERRUPTED
	print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Чтение несуществующих данных в формате String")
	if not check: print(f"                  {result.code} {result.subcodes}\n")
	assert check

	time_0 = time.time()
	result = message.f_number.ToBooleans(CONTAINER_RAM)
	time_1 = time.time()
	check  = result.code == CODES_COMPLETION.INTERRUPTED
	print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Чтение несуществующих данных в формате [Boolean]")
	if not check: print(f"                  {result.code} {result.subcodes}\n")
	assert check

	time_0 = time.time()
	result = message.f_number.ToDatetimes(CONTAINER_RAM)
	time_1 = time.time()
	check  = result.code == CODES_COMPLETION.INTERRUPTED
	print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Чтение несуществующих данных в формате [DateTime]")
	if not check: print(f"                  {result.code} {result.subcodes}\n")
	assert check

	time_0 = time.time()
	result = message.f_number.ToIntegers(CONTAINER_RAM)
	time_1 = time.time()
	check  = result.code == CODES_COMPLETION.INTERRUPTED
	print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Чтение несуществующих данных в формате [Integer]")
	if not check: print(f"                  {result.code} {result.subcodes}\n")
	assert check

	time_0 = time.time()
	result = message.f_number.ToFloats(CONTAINER_RAM)
	time_1 = time.time()
	check  = result.code == CODES_COMPLETION.INTERRUPTED
	print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Чтение несуществующих данных в формате [Float]")
	if not check: print(f"                  {result.code} {result.subcodes}\n")
	assert check

	time_0 = time.time()
	result = message.f_number.ToStrings(CONTAINER_RAM)
	time_1 = time.time()
	check  = result.code == CODES_COMPLETION.INTERRUPTED
	print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Чтение несуществующих данных в формате [String]")
	if not check: print(f"                  {result.code} {result.subcodes}\n")
	assert check

	time_0 = time.time()
	result = message.RegisterObject(CONTAINER_RAM)
	time_1 = time.time()
	check  = result.code == CODES_COMPLETION.COMPLETED
	print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Регистрация объекта")
	if not check: print(f"                  {result.code} {result.subcodes}\n")
	assert check

	time_0 = time.time()
	result = message.CheckRegisterObject(CONTAINER_RAM)
	time_1 = time.time()
	check  = result.code == CODES_COMPLETION.COMPLETED
	check &= result.data == True
	print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Проверка регистрации объекта")
	if not check: print(f"                  {result.code} {result.subcodes}\n")
	assert check

	time_0 = time.time()
	result = message.f_number.FromInteger(CONTAINER_RAM, 1)
	time_1 = time.time()
	check  = result.code == CODES_COMPLETION.COMPLETED
	print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Запись данных")
	if not check: print(f"                  {result.code} {result.subcodes}\n")
	assert check

	time_0 = time.time()
	result = message.f_number.ToBoolean(CONTAINER_RAM)
	time_1 = time.time()
	check  = result.code == CODES_COMPLETION.COMPLETED
	check &= result.data == True
	print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Чтение данных в формате Boolean")
	if not check: print(f"                  {result.code} {result.subcodes}\n")
	assert check

	time_0 = time.time()
	result = message.f_number.ToDatetime(CONTAINER_RAM)
	time_1 = time.time()
	check  = result.code == CODES_COMPLETION.COMPLETED
	check &= result.data == datetime.datetime(1970, 1, 1, 3, 0, 1)
	print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Чтение данных в формате DateTime")
	if not check: print(f"                  {result.code} {result.subcodes}\n")
	assert check

	time_0 = time.time()
	result = message.f_number.ToInteger(CONTAINER_RAM)
	time_1 = time.time()
	check  = result.code == CODES_COMPLETION.COMPLETED
	check &= result.data == 1
	print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Чтение данных в формате Integer")
	if not check: print(f"                  {result.code} {result.subcodes}\n")
	assert check

	time_0 = time.time()
	result = message.f_number.ToFloat(CONTAINER_RAM)
	time_1 = time.time()
	check  = result.code == CODES_COMPLETION.COMPLETED
	check &= result.data == 1.00
	print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Чтение данных в формате Float")
	if not check: print(f"                  {result.code} {result.subcodes}\n")
	assert check

	time_0 = time.time()
	result = message.f_number.ToString(CONTAINER_RAM)
	time_1 = time.time()
	check  = result.code == CODES_COMPLETION.COMPLETED
	check &= result.data == "1"
	print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Чтение данных в формате String")
	if not check: print(f"                  {result.code} {result.subcodes}\n")
	assert check

	time_0 = time.time()
	result = message.f_number.ToBooleans(CONTAINER_RAM)
	time_1 = time.time()
	check  = result.code == CODES_COMPLETION.COMPLETED
	check &= len(result.data) == 1
	print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Чтение данных в формате [Boolean]")
	if not check: print(f"                  {result.code} {result.subcodes}\n")
	assert check

	time_0 = time.time()
	result = message.f_number.ToDatetimes(CONTAINER_RAM)
	time_1 = time.time()
	check  = result.code == CODES_COMPLETION.COMPLETED
	check &= len(result.data) == 1
	print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Чтение данных в формате [DateTime]")
	if not check: print(f"                  {result.code} {result.subcodes}\n")
	assert check

	time_0 = time.time()
	result = message.f_number.ToIntegers(CONTAINER_RAM)
	time_1 = time.time()
	check  = result.code == CODES_COMPLETION.COMPLETED
	check &= len(result.data) == 1
	print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Чтение данных в формате [Integer]")
	if not check: print(f"                  {result.code} {result.subcodes}\n")
	assert check

	time_0 = time.time()
	result = message.f_number.ToFloats(CONTAINER_RAM)
	time_1 = time.time()
	check  = result.code == CODES_COMPLETION.COMPLETED
	check &= len(result.data) == 1
	print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Чтение данных в формате [Float]")
	if not check: print(f"                  {result.code} {result.subcodes}\n")
	assert check

	time_0 = time.time()
	result = message.f_number.ToStrings(CONTAINER_RAM)
	time_1 = time.time()
	check  = result.code == CODES_COMPLETION.COMPLETED
	check &= len(result.data) == 1
	print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Чтение данных в формате [String]")
	if not check: print(f"                  {result.code} {result.subcodes}\n")
	assert check
