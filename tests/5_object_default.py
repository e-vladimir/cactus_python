# ТЕСТИРОВАНИЕ СТРУКТУРНОГО ОБЪЕКТА СО ЗНАЧЕНИЕМ ПО УМОЛЧАНИЮ
# 08 сен 2026

import time

from   G00_status_codes  import (CODES_COMPLETION,
                                 CODES_DATA)
from   G30_cactus_frames import (C30_StructFrame,
                                 C30_StructField)


CONTAINER_RAM = "RAM"


print("Тест Структурного объекта: Значение по-умолчанию")
print("")


class CObj(C30_StructFrame):
	_idc = "Сообщение"

	def Init_10(self):
		super().Init_10()

		self.f_number = C30_StructField(self, "Число", 2)
		self.f_text   = C30_StructField(self, "Текст", "2w")
		self.f_list   = C30_StructField(self, "Список", [1, 2, 3])
		self.f_empty  = C30_StructField(self, "Пусто")
		self.f_empty_10 = C30_StructField(self, "Пусто", 10)

	def NumberOrDefault(self, real_default = None) -> any:
		result_read = self.f_number.ToString(CONTAINER_RAM)

		if CODES_DATA.NO_DATA in result_read.subcodes: return real_default
		else                                         : return result_read.data


message = CObj()
message.GenerateIdo()

print("Базовая проверка")

time_0 = time.time()
result = message.f_empty.ToInteger(CONTAINER_RAM)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
check &= result.data == 0
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Проверка ситуации Данных нет без установки значения по-умолчанию")
if not check: print(f"                  {result.code} {result.subcodes}\n")

time_0 = time.time()
result = message.f_empty_10.ToInteger(CONTAINER_RAM)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
check &= result.data == 10
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Проверка установки значения по-умолчанию равным 10")
if not check: print(f"                  {result.code} {result.subcodes}\n")

print("")
print("Расширенная проверка")

time_0 = time.time()
result = message.f_number.ToBoolean(CONTAINER_RAM)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
check &= result.data == False
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Проверка 1 значения по-умолчанию для типа Boolean")
if not check: print(f"                  {result.code} {result.subcodes}\n")

time_0 = time.time()
result = message.f_number.ToDatetime(CONTAINER_RAM)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
check &= CODES_DATA.NO_DATA in result.subcodes
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Проверка 1 значения по-умолчанию для типа DateTime")
if not check: print(f"                  {result.code} {result.subcodes}\n")

time_0 = time.time()
result = message.f_number.ToInteger(CONTAINER_RAM)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
check &= result.data == 2
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Проверка 1 значения по-умолчанию для типа Integer")
if not check: print(f"                  {result.code} {result.subcodes}\n")

time_0 = time.time()
result = message.f_number.ToFloat(CONTAINER_RAM)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
check &= result.data == 2.00
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Проверка 1 значения по-умолчанию для типа Float")
if not check: print(f"                  {result.code} {result.subcodes}\n")

time_0 = time.time()
result = message.f_number.ToBooleans(CONTAINER_RAM)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
check &= result.data == [False]
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Проверка 1 значения по-умолчанию для типа [Boolean]")
if not check: print(f"                  {result.code} {result.subcodes}\n")

time_0 = time.time()
result = message.f_number.ToDatetimes(CONTAINER_RAM)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
check &= result.data != []
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Проверка 1 значения по-умолчанию для типа [Datetime]")
if not check: print(f"                  {result.code} {result.subcodes}\n")

time_0 = time.time()
result = message.f_number.ToIntegers(CONTAINER_RAM)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
check &= result.data == [2]
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Проверка 1 значения по-умолчанию для типа [Integer]")
if not check: print(f"                  {result.code} {result.subcodes}\n")

time_0 = time.time()
result = message.f_number.ToFloats(CONTAINER_RAM)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
check &= result.data == [2.00]
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Проверка 1 значения по-умолчанию для типа [Floats]")
if not check: print(f"                  {result.code} {result.subcodes}\n")

time_0 = time.time()
result = message.f_number.ToStrings(CONTAINER_RAM)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
check &= result.data == ["2"]
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Проверка 1 значения по-умолчанию для типа [String]")
if not check: print(f"                  {result.code} {result.subcodes}\n")

print("---")

time_0 = time.time()
result = message.f_text.ToBoolean(CONTAINER_RAM)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
check &= result.data == False
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Проверка 2 значения по-умолчанию для типа Boolean")
if not check: print(f"                  {result.code} {result.subcodes}\n")

time_0 = time.time()
result = message.f_text.ToDatetime(CONTAINER_RAM)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.INTERRUPTED
check &= CODES_DATA.NO_DATA in result.subcodes
check &= CODES_DATA.NO_DATA in result.subcodes
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Проверка 2 значения по-умолчанию для типа DateTime")
if not check: print(f"                  {result.code} {result.subcodes}\n")

time_0 = time.time()
result = message.f_text.ToInteger(CONTAINER_RAM)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.INTERRUPTED
check &= CODES_DATA.NO_DATA in result.subcodes
check &= CODES_DATA.ERROR_CONVERT in result.subcodes
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Проверка 2 значения по-умолчанию для типа Integer")
if not check: print(f"                  {result.code} {result.subcodes}\n")

time_0 = time.time()
result = message.f_text.ToFloat(CONTAINER_RAM)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.INTERRUPTED
check &= CODES_DATA.NO_DATA in result.subcodes
check &= CODES_DATA.ERROR_CONVERT in result.subcodes
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Проверка 2 значения по-умолчанию для типа Float")
if not check: print(f"                  {result.code} {result.subcodes}\n")

time_0 = time.time()
result = message.f_text.ToBooleans(CONTAINER_RAM)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
check &= result.data == [False]
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Проверка 2 значения по-умолчанию для типа [Boolean]")
if not check: print(f"                  {result.code} {result.subcodes}\n")

time_0 = time.time()
result = message.f_text.ToDatetimes(CONTAINER_RAM)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
check &= result.data == []
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Проверка 2 значения по-умолчанию для типа [Datetime]")
if not check: print(f"                  {result.code} {result.subcodes}\n")

time_0 = time.time()
result = message.f_text.ToIntegers(CONTAINER_RAM)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
check &= result.data == []
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Проверка 2 значения по-умолчанию для типа [Integer]")
if not check: print(f"                  {result.code} {result.subcodes}\n")

time_0 = time.time()
result = message.f_text.ToFloats(CONTAINER_RAM)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
check &= result.data == []
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Проверка 2 значения по-умолчанию для типа [Floats]")
if not check: print(f"                  {result.code} {result.subcodes}\n")

time_0 = time.time()
result = message.f_text.ToStrings(CONTAINER_RAM)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
check &= result.data == ["2w"]
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Проверка 2 значения по-умолчанию для типа [String]")
if not check: print(f"                  {result.code} {result.subcodes}\n")

print("---")

time_0 = time.time()
result = message.f_list.ToBoolean(CONTAINER_RAM)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
check &= result.data == False
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Проверка 3 значения по-умолчанию для типа Boolean")
if not check: print(f"                  {result.code} {result.subcodes}\n")

time_0 = time.time()
result = message.f_list.ToDatetime(CONTAINER_RAM)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.INTERRUPTED
check &= CODES_DATA.NO_DATA in result.subcodes
check &= CODES_DATA.NO_DATA in result.subcodes
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Проверка 3 значения по-умолчанию для типа DateTime")
if not check: print(f"                  {result.code} {result.subcodes}\n")

time_0 = time.time()
result = message.f_list.ToInteger(CONTAINER_RAM)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.INTERRUPTED
check &= CODES_DATA.NO_DATA in result.subcodes
check &= CODES_DATA.ERROR_CONVERT in result.subcodes
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Проверка 3 значения по-умолчанию для типа Integer")
if not check: print(f"                  {result.code} {result.subcodes}\n")

time_0 = time.time()
result = message.f_list.ToFloat(CONTAINER_RAM)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.INTERRUPTED
check &= CODES_DATA.NO_DATA in result.subcodes
check &= CODES_DATA.ERROR_CONVERT in result.subcodes
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Проверка 3 значения по-умолчанию для типа Float")
if not check: print(f"                  {result.code} {result.subcodes}\n")

time_0 = time.time()
result = message.f_list.ToBooleans(CONTAINER_RAM)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
check &= result.data == [True, False, False]
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Проверка 3 значения по-умолчанию для типа [Boolean]")
if not check: print(f"                  {result.code} {result.subcodes}\n")

time_0 = time.time()
result = message.f_list.ToDatetimes(CONTAINER_RAM)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
check &= result.data != []
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Проверка 3 значения по-умолчанию для типа [Datetime]")
if not check: print(f"                  {result.code} {result.subcodes}\n")

time_0 = time.time()
result = message.f_list.ToIntegers(CONTAINER_RAM)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
check &= result.data == [1, 2, 3]
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Проверка 3 значения по-умолчанию для типа [Integer]")
if not check: print(f"                  {result.code} {result.subcodes}\n")

time_0 = time.time()
result = message.f_list.ToFloats(CONTAINER_RAM)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
check &= result.data == [1.00, 2.00, 3.00]
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Проверка 3 значения по-умолчанию для типа [Floats]")
if not check: print(f"                  {result.code} {result.subcodes}\n")

time_0 = time.time()
result = message.f_list.ToStrings(CONTAINER_RAM)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
check &= result.data == ["1", "2", "3"]
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Проверка 3 значения по-умолчанию для типа [String]")
if not check: print(f"                  {result.code} {result.subcodes}\n")

print("---")

time_0 = time.time()
result = message.f_empty.ToBoolean(CONTAINER_RAM)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
check &= result.data == False
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Проверка 4 значения по-умолчанию для типа Boolean")
if not check: print(f"                  {result.code} {result.subcodes}\n")

time_0 = time.time()
result = message.f_empty.ToDatetime(CONTAINER_RAM)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
check &= CODES_DATA.NO_DATA in result.subcodes
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Проверка 4 значения по-умолчанию для типа DateTime")
if not check: print(f"                  {result.code} {result.subcodes}\n")

time_0 = time.time()
result = message.f_empty.ToInteger(CONTAINER_RAM)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Проверка 4 значения по-умолчанию для типа Integer")
if not check: print(f"                  {result.code} {result.subcodes}\n")

time_0 = time.time()
result = message.f_empty.ToFloat(CONTAINER_RAM)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Проверка 4 значения по-умолчанию для типа Float")
if not check: print(f"                  {result.code} {result.subcodes}\n")

time_0 = time.time()
result = message.f_empty.ToBooleans(CONTAINER_RAM)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
check &= result.data == []
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Проверка 4 значения по-умолчанию для типа [Boolean]")
if not check: print(f"                  {result.code} {result.subcodes}\n")

time_0 = time.time()
result = message.f_empty.ToDatetimes(CONTAINER_RAM)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
check &= result.data == []
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Проверка 4 значения по-умолчанию для типа [Datetime]")
if not check: print(f"                  {result.code} {result.subcodes}\n")

time_0 = time.time()
result = message.f_empty.ToIntegers(CONTAINER_RAM)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
check &= result.data == []
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Проверка 4 значения по-умолчанию для типа [Integer]")
if not check: print(f"                  {result.code} {result.subcodes}\n")

time_0 = time.time()
result = message.f_empty.ToFloats(CONTAINER_RAM)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
check &= result.data == []
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Проверка 4 значения по-умолчанию для типа [Floats]")
if not check: print(f"                  {result.code} {result.subcodes}\n")

time_0 = time.time()
result = message.f_empty.ToStrings(CONTAINER_RAM)
time_1 = time.time()
check  = result.code == CODES_COMPLETION.COMPLETED
check &= CODES_DATA.NO_DATA in result.subcodes
check &= result.data == []
print(f"{(time_1 - time_0):0.3f} сек  ", "[+]" if check else "[ ]", "  Проверка 4 значения по-умолчанию для типа [Strings]")
if not check: print(f"                  {result.code} {result.subcodes}\n")
