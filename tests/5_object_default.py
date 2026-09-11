# ТЕСТИРОВАНИЕ СТРУКТУРНОГО ОБЪЕКТА: 4 СЦЕНАРИЯ
# 11 сен 2026

from   G00_status_codes                 import (CODES_COMPLETION,
                                                CODES_DATA,
                                                CODES_CACTUS,
                                                CODES_PROCESSING)
from   G30_cactus_controller_containers import ControllerContainers
from   G30_cactus_frames import (C30_StructFrame,
                               C30_StructField, SEPARATOR_LIST)


# Имена контейнеров для разных сценариев
CONTAINER_NONE       = "NONE"        # Сценарий 1: не зарегистрирован
CONTAINER_EMPTY      = "EMPTY"       # Сценарий 2: зарегистрирован, ячейки нет
CONTAINER_EMPTY_DATA = "EMPTY_DATA"  # Сценарий 3: зарегистрирован, ячейка есть, vlp=""
CONTAINER_DATA       = "DATA"        # Сценарий 4: зарегистрирован, ячейка есть, данные есть


print("Тест Структурного объекта: 4 сценария")
print(f"SEPARATOR_LIST = {repr(SEPARATOR_LIST)}")
print("")


# ============================================================================
# Класс объекта
# ============================================================================
class CObj(C30_StructFrame):
	_idc = "Сообщение"

	def Init_10(self):
		super().Init_10()

		self.f_number   = C30_StructField(self, "Число", 1)
		self.f_text     = C30_StructField(self, "Текст", "2w")
		self.f_list     = C30_StructField(self, "Список", [1, 2, 3])
		self.f_empty    = C30_StructField(self, "Пусто")
		self.f_empty_10 = C30_StructField(self, "Пусто10", 10)


# ============================================================================
# Вспомогательная функция проверки
# ============================================================================
def check_result(result, expected_code, expected_subcodes, expected_data, test_name):
	"""Проверка результата с выводом"""
	check  = result.code == expected_code
	for sc in expected_subcodes:
		check &= sc in result.subcodes
	if expected_data is not _SKIP_CHECK:
		check &= result.data == expected_data

	print("  [+]" if check else "  [ ]", test_name)
	if not check:
		print(f"         Ожидание: code={expected_code}, subcodes={expected_subcodes}, data={expected_data}")
		print(f"         Факт:     code={result.code}, subcodes={result.subcodes}, data={result.data}")
		print("")
	return check


_SKIP_CHECK = object()  # Маркер: не проверять data


# ============================================================================
# Регистрация контейнеров
# ============================================================================
# Сценарий 1: CONTAINER_NONE НЕ регистрируем
ControllerContainers.RegisterContainerRAM(CONTAINER_EMPTY)
ControllerContainers.RegisterContainerRAM(CONTAINER_EMPTY_DATA)
ControllerContainers.RegisterContainerRAM(CONTAINER_DATA)


# ============================================================================
# Создание объекта и запись данных
# ============================================================================
message = CObj()
message.GenerateIdo()

# Сценарий 3: записываем пустые строки во все поля
message.f_number.FromString(CONTAINER_EMPTY_DATA, "")
message.f_text.FromString(CONTAINER_EMPTY_DATA, "")
message.f_list.FromString(CONTAINER_EMPTY_DATA, "")
message.f_empty.FromString(CONTAINER_EMPTY_DATA, "")
message.f_empty_10.FromString(CONTAINER_EMPTY_DATA, "")

# Сценарий 4: записываем валидные данные (используем SEPARATOR_LIST для списков)
message.f_number.FromString(CONTAINER_DATA, "42")
message.f_text.FromString(CONTAINER_DATA, "hello")
message.f_list.FromString(CONTAINER_DATA, SEPARATOR_LIST.join(["10", "20", "30"]))
message.f_empty.FromString(CONTAINER_DATA, "")
message.f_empty_10.FromString(CONTAINER_DATA, "")


# ============================================================================
# СЦЕНАРИЙ 1: Контейнер не зарегистрирован
# ============================================================================
print("=" * 60)
print("СЦЕНАРИЙ 1: Контейнер не зарегистрирован")
print("Ожидание: INTERRUPTED + NO_CONTAINER + NO_DATA")
print("          Дефолт используется, если есть")
print("=" * 60)

# f_empty (нет дефолта)
result = message.f_empty.ToInteger(CONTAINER_NONE)
check_result(result,
             CODES_COMPLETION.INTERRUPTED,
             {CODES_CACTUS.NO_CONTAINER, CODES_DATA.NO_DATA},
             0,
             "f_empty.ToInteger (нет дефолта)")

# f_empty_10 (дефолт 10)
result = message.f_empty_10.ToInteger(CONTAINER_NONE)
check_result(result,
             CODES_COMPLETION.INTERRUPTED,
             {CODES_CACTUS.NO_CONTAINER, CODES_DATA.NO_DATA},
             10,
             "f_empty_10.ToInteger (дефолт 10)")

# f_number (дефолт 1)
result = message.f_number.ToInteger(CONTAINER_NONE)
check_result(result,
             CODES_COMPLETION.INTERRUPTED,
             {CODES_CACTUS.NO_CONTAINER, CODES_DATA.NO_DATA},
             1,
             "f_number.ToInteger (дефолт 1)")

result = message.f_number.ToBoolean(CONTAINER_NONE)
check_result(result,
             CODES_COMPLETION.INTERRUPTED,
             {CODES_CACTUS.NO_CONTAINER, CODES_DATA.NO_DATA},
             True,
             "f_number.ToBoolean (дефолт 1 → True)")

result = message.f_number.ToFloat(CONTAINER_NONE)
check_result(result,
             CODES_COMPLETION.INTERRUPTED,
             {CODES_CACTUS.NO_CONTAINER, CODES_DATA.NO_DATA},
             1.0,
             "f_number.ToFloat (дефолт 1 → 1.0)")

result = message.f_number.ToString(CONTAINER_NONE)
check_result(result,
             CODES_COMPLETION.INTERRUPTED,
             {CODES_CACTUS.NO_CONTAINER, CODES_DATA.NO_DATA},
             "1",
             "f_number.ToString (дефолт 1 → '1')")

# f_text (дефолт "2w")
result = message.f_text.ToBoolean(CONTAINER_NONE)
check_result(result,
             CODES_COMPLETION.INTERRUPTED,
             {CODES_CACTUS.NO_CONTAINER, CODES_DATA.NO_DATA},
             False,
             "f_text.ToBoolean (дефолт '2w' → False)")

result = message.f_text.ToInteger(CONTAINER_NONE)
check_result(result,
             CODES_COMPLETION.INTERRUPTED,
             {CODES_CACTUS.NO_CONTAINER, CODES_DATA.NO_DATA, CODES_DATA.ERROR_CONVERT},
             _SKIP_CHECK,
             "f_text.ToInteger (дефолт '2w' → ошибка конвертации)")

result = message.f_text.ToString(CONTAINER_NONE)
check_result(result,
             CODES_COMPLETION.INTERRUPTED,
             {CODES_CACTUS.NO_CONTAINER, CODES_DATA.NO_DATA},
             "2w",
             "f_text.ToString (дефолт '2w')")

# f_list (дефолт [1, 2, 3])
result = message.f_list.ToIntegers(CONTAINER_NONE)
check_result(result,
             CODES_COMPLETION.INTERRUPTED,
             {CODES_CACTUS.NO_CONTAINER, CODES_DATA.NO_DATA},
             [1, 2, 3],
             "f_list.ToIntegers (дефолт [1,2,3])")

result = message.f_list.ToFloats(CONTAINER_NONE)
check_result(result,
             CODES_COMPLETION.INTERRUPTED,
             {CODES_CACTUS.NO_CONTAINER, CODES_DATA.NO_DATA},
             [1.0, 2.0, 3.0],
             "f_list.ToFloats (дефолт [1.0,2.0,3.0])")

result = message.f_list.ToStrings(CONTAINER_NONE)
check_result(result,
             CODES_COMPLETION.INTERRUPTED,
             {CODES_CACTUS.NO_CONTAINER, CODES_DATA.NO_DATA},
             ["1", "2", "3"],
             "f_list.ToStrings (дефолт ['1','2','3'])")

print("")


# ============================================================================
# СЦЕНАРИЙ 2: Контейнер есть, ячейки нет
# ============================================================================
print("=" * 60)
print("СЦЕНАРИЙ 2: Контейнер есть, ячейки нет")
print("Ожидание: INTERRUPTED + NO_DATA")
print("          Дефолт используется, если есть")
print("=" * 60)

# f_empty (нет дефолта)
result = message.f_empty.ToInteger(CONTAINER_EMPTY)
check_result(result,
             CODES_COMPLETION.INTERRUPTED,
             {CODES_DATA.NO_DATA},
             0,
             "f_empty.ToInteger (нет дефолта)")

# f_empty_10 (дефолт 10)
result = message.f_empty_10.ToInteger(CONTAINER_EMPTY)
check_result(result,
             CODES_COMPLETION.INTERRUPTED,
             {CODES_DATA.NO_DATA},
             10,
             "f_empty_10.ToInteger (дефолт 10)")

# f_number (дефолт 1)
result = message.f_number.ToInteger(CONTAINER_EMPTY)
check_result(result,
             CODES_COMPLETION.INTERRUPTED,
             {CODES_DATA.NO_DATA},
             1,
             "f_number.ToInteger (дефолт 1)")

result = message.f_number.ToBoolean(CONTAINER_EMPTY)
check_result(result,
             CODES_COMPLETION.INTERRUPTED,
             {CODES_DATA.NO_DATA},
             True,
             "f_number.ToBoolean (дефолт 1 → True)")

result = message.f_number.ToFloat(CONTAINER_EMPTY)
check_result(result,
             CODES_COMPLETION.INTERRUPTED,
             {CODES_DATA.NO_DATA},
             1.0,
             "f_number.ToFloat (дефолт 1 → 1.0)")

result = message.f_number.ToString(CONTAINER_EMPTY)
check_result(result,
             CODES_COMPLETION.INTERRUPTED,
             {CODES_DATA.NO_DATA},
             "1",
             "f_number.ToString (дефолт 1 → '1')")

# f_text (дефолт "2w")
result = message.f_text.ToBoolean(CONTAINER_EMPTY)
check_result(result,
             CODES_COMPLETION.INTERRUPTED,
             {CODES_DATA.NO_DATA},
             False,
             "f_text.ToBoolean (дефолт '2w' → False)")

result = message.f_text.ToInteger(CONTAINER_EMPTY)
check_result(result,
             CODES_COMPLETION.INTERRUPTED,
             {CODES_DATA.NO_DATA, CODES_DATA.ERROR_CONVERT},
             _SKIP_CHECK,
             "f_text.ToInteger (дефолт '2w' → ошибка конвертации)")

result = message.f_text.ToString(CONTAINER_EMPTY)
check_result(result,
             CODES_COMPLETION.INTERRUPTED,
             {CODES_DATA.NO_DATA},
             "2w",
             "f_text.ToString (дефолт '2w')")

# f_list (дефолт [1, 2, 3])
result = message.f_list.ToIntegers(CONTAINER_EMPTY)
check_result(result,
             CODES_COMPLETION.INTERRUPTED,
             {CODES_DATA.NO_DATA},
             [1, 2, 3],
             "f_list.ToIntegers (дефолт [1,2,3])")

result = message.f_list.ToFloats(CONTAINER_EMPTY)
check_result(result,
             CODES_COMPLETION.INTERRUPTED,
             {CODES_DATA.NO_DATA},
             [1.0, 2.0, 3.0],
             "f_list.ToFloats (дефолт [1.0,2.0,3.0])")

result = message.f_list.ToStrings(CONTAINER_EMPTY)
check_result(result,
             CODES_COMPLETION.INTERRUPTED,
             {CODES_DATA.NO_DATA},
             ["1", "2", "3"],
             "f_list.ToStrings (дефолт ['1','2','3'])")

print("")


# ============================================================================
# СЦЕНАРИЙ 3: Контейнер есть, ячейка есть, данных нет (vlp="")
# ============================================================================
print("=" * 60)
print("СЦЕНАРИЙ 3: Контейнер есть, ячейка есть, vlp=''")
print("Ожидание: COMPLETED (ячейка есть)")
print("  Одиночные методы: ERROR_CONVERT (пустая строка)")
print("  ToBoolean: '' → False (особенность конвертера)")
print("  Списочные методы: vlp=='' → flag_no_data → дефолт")
print("=" * 60)

# --- Одиночные методы ---

# f_number (дефолт 1, но vlp="" в контейнере)
result = message.f_number.ToInteger(CONTAINER_EMPTY_DATA)
check_result(result,
             CODES_COMPLETION.COMPLETED,
             {CODES_DATA.ERROR_CONVERT},
             _SKIP_CHECK,
             "f_number.ToInteger ('' → ошибка конвертации)")

result = message.f_number.ToFloat(CONTAINER_EMPTY_DATA)
check_result(result,
             CODES_COMPLETION.COMPLETED,
             {CODES_DATA.ERROR_CONVERT},
             _SKIP_CHECK,
             "f_number.ToFloat ('' → ошибка конвертации)")

result = message.f_number.ToBoolean(CONTAINER_EMPTY_DATA)
check_result(result,
             CODES_COMPLETION.COMPLETED,
             set(),
             False,
             "f_number.ToBoolean ('' → False, особенность конвертера)")

result = message.f_number.ToString(CONTAINER_EMPTY_DATA)
check_result(result,
             CODES_COMPLETION.COMPLETED,
             set(),
             "",
             "f_number.ToString ('' → '')")

# f_text
result = message.f_text.ToString(CONTAINER_EMPTY_DATA)
check_result(result,
             CODES_COMPLETION.COMPLETED,
             set(),
             "",
             "f_text.ToString ('' → '')")

result = message.f_text.ToInteger(CONTAINER_EMPTY_DATA)
check_result(result,
             CODES_COMPLETION.COMPLETED,
             {CODES_DATA.ERROR_CONVERT},
             _SKIP_CHECK,
             "f_text.ToInteger ('' → ошибка конвертации)")

# --- Списочные методы: vlp=='' → flag_no_data → используется дефолт ---

result = message.f_number.ToIntegers(CONTAINER_EMPTY_DATA)
check_result(result,
             CODES_COMPLETION.COMPLETED,
             set(),
             [1],
             "f_number.ToIntegers (дефолт 1 → [1])")

result = message.f_number.ToFloats(CONTAINER_EMPTY_DATA)
check_result(result,
             CODES_COMPLETION.COMPLETED,
             set(),
             [1.0],
             "f_number.ToFloats (дефолт 1 → [1.0])")

result = message.f_number.ToBooleans(CONTAINER_EMPTY_DATA)
check_result(result,
             CODES_COMPLETION.COMPLETED,
             set(),
             [True],
             "f_number.ToBooleans (дефолт 1 → [True])")

result = message.f_number.ToStrings(CONTAINER_EMPTY_DATA)
check_result(result,
             CODES_COMPLETION.COMPLETED,
             set(),
             ["1"],
             "f_number.ToStrings (дефолт 1 → ['1'])")

result = message.f_text.ToStrings(CONTAINER_EMPTY_DATA)
check_result(result,
             CODES_COMPLETION.COMPLETED,
             set(),
             ["2w"],
             "f_text.ToStrings榨汁机s (дефолт '2w' → ['2w'])")

result = message.f_list.ToIntegers(CONTAINER_EMPTY_DATA)
check_result(result,
             CODES_COMPLETION.COMPLETED,
             set(),
             [1, 2, 3],
             "f_list.ToIntegers (дефолт [1,2,3])")

result = message.f_list.ToFloats(CONTAINER_EMPTY_DATA)
check_result(result,
             CODES_COMPLETION.COMPLETED,
             set(),
             [1.0, 2.0, 3.0],
             "f_list.ToFloats (дефолт [1.0,2.0,3.0])")

result = message.f_list.ToStrings(CONTAINER_EMPTY_DATA)
check_result(result,
             CODES_COMPLETION.COMPLETED,
             set(),
             ["1", "2", "3"],
             "f_list.ToStrings (дефолт ['1','2','3'])")

# f_empty (нет дефолта)
result = message.f_empty.ToString(CONTAINER_EMPTY_DATA)
check_result(result,
             CODES_COMPLETION.COMPLETED,
             set(),
             "",
             "f_empty.ToString ('' → '')")

result = message.f_empty.ToIntegers(CONTAINER_EMPTY_DATA)
check_result(result,
             CODES_COMPLETION.COMPLETED,
             {CODES_DATA.NO_DATA},
             [],
             "f_empty.ToIntegers (нет дефолта → [])")

result = message.f_empty_10.ToIntegers(CONTAINER_EMPTY_DATA)
check_result(result,
             CODES_COMPLETION.COMPLETED,
             set(),
             [10],
             "f_empty_10.ToIntegers (дефолт 10 → [10])")

print("")


# ============================================================================
# СЦЕНАРИЙ 4: Контейнер есть, ячейка есть, данные есть
# ============================================================================
print("=" * 60)
print("СЦЕНАРИЙ 4: Контейнер есть, ячейка есть, данные есть")
print("Ожидание: COMPLETED, успешная конвертация")
print("  ToBoolean: любое значение → False (особенность конвертера)")
print("=" * 60)

# --- f_number: vlp="42" ---
print("  --- f_number (vlp='42') ---")

result = message.f_number.ToInteger(CONTAINER_DATA)
check_result(result,
             CODES_COMPLETION.COMPLETED,
             set(),
             42,
             "f_number.ToInteger ('42' → 42)")

result = message.f_number.ToFloat(CONTAINER_DATA)
check_result(result,
             CODES_COMPLETION.COMPLETED,
             set(),
             42.0,
             "f_number.ToFloat ('42' → 42.0)")

result = message.f_number.ToBoolean(CONTAINER_DATA)
check_result(result,
             CODES_COMPLETION.COMPLETED,
             set(),
             False,
             "f_number.ToBoolean ('42' → False, особенность конвертера)")

result = message.f_number.ToString(CONTAINER_DATA)
check_result(result,
             CODES_COMPLETION.COMPLETED,
             set(),
             "42",
             "f_number.ToString ('42' → '42')")

result = message.f_number.ToIntegers(CONTAINER_DATA)
check_result(result,
             CODES_COMPLETION.COMPLETED,
             {CODES_DATA.SINGLE},
             [42],
             "f_number.ToIntegers ('42' → [42])")

result = message.f_number.ToFloats(CONTAINER_DATA)
check_result(result,
             CODES_COMPLETION.COMPLETED,
             {CODES_DATA.SINGLE},
             [42.0],
             "f_number.ToFloats ('42' → [42.0])")

result = message.f_number.ToBooleans(CONTAINER_DATA)
check_result(result,
             CODES_COMPLETION.COMPLETED,
             {CODES_DATA.SINGLE},
             [False],
             "f_number.ToBooleans ('42' → [False])")

result = message.f_number.ToStrings(CONTAINER_DATA)
check_result(result,
             CODES_COMPLETION.COMPLETED,
             {CODES_DATA.SINGLE},
             ["42"],
             "f_number.ToStrings ('42' → ['42'])")

# --- f_text: vlp="hello" ---
print("  --- f_text (vlp='hello') ---")

result = message.f_text.ToString(CONTAINER_DATA)
check_result(result,
             CODES_COMPLETION.COMPLETED,
             set(),
             "hello",
             "f_text.ToString ('hello' → 'hello')")

result = message.f_text.ToInteger(CONTAINER_DATA)
check_result(result,
             CODES_COMPLETION.COMPLETED,
             {CODES_DATA.ERROR_CONVERT},
             _SKIP_CHECK,
             "f_text.ToInteger ('hello' → ошибка конвертации)")

result = message.f_text.ToFloat(CONTAINER_DATA)
check_result(result,
             CODES_COMPLETION.COMPLETED,
             {CODES_DATA.ERROR_CONVERT},
             _SKIP_CHECK,
             "f_text.ToFloat ('hello' → ошибка конвертации)")

result = message.f_text.ToBoolean(CONTAINER_DATA)
check_result(result,
             CODES_COMPLETION.COMPLETED,
             set(),
             False,
             "f_text.ToBoolean ('hello' → False, особенность конвертера)")

result = message.f_text.ToStrings(CONTAINER_DATA)
check_result(result,
             CODES_COMPLETION.COMPLETED,
             {CODES_DATA.SINGLE},
             ["hello"],
             "f_text.ToStrings ('hello' → ['hello'])")

# --- f_list: vlp="10\n20\n30" ---
print("  --- f_list (vlp='10\\n20\\n30') ---")

result = message.f_list.ToIntegers(CONTAINER_DATA)
check_result(result,
             CODES_COMPLETION.COMPLETED,
             set(),
             [10, 20, 30],
             "f_list.ToIntegers ('10\\n20\\n30' → [10,20,30])")

result = message.f_list.ToFloats(CONTAINER_DATA)
check_result(result,
             CODES_COMPLETION.COMPLETED,
             set(),
             [10.0, 20.0, 30.0],
             "f_list.ToFloats ('10\\n20\\n30' → [10.0,20.0,30.0])")

result = message.f_list.ToStrings(CONTAINER_DATA)
check_result(result,
             CODES_COMPLETION.COMPLETED,
             set(),
             ["10", "20", "30"],
             "f_list.ToStrings ('10\\n20\\n30' → ['10','20','30'])")

result = message.f_list.ToBooleans(CONTAINER_DATA)
check_result(result,
             CODES_COMPLETION.COMPLETED,
             set(),
             [False, False, False],
             "f_list.ToBooleans ('10\\n20\\n30' → [False,False,False])")

result = message.f_list.ToString(CONTAINER_DATA)
check_result(result,
             CODES_COMPLETION.COMPLETED,
             set(),
             SEPARATOR_LIST.join(["10", "20", "30"]),
             "f_list.ToString ('10\\n20\\n30' → '10\\n20\\n30')")

# --- f_empty: vlp="" ---
print("  --- f_empty (vlp='', нет дефолта) ---")

result = message.f_empty.ToString(CONTAINER_DATA)
check_result(result,
             CODES_COMPLETION.COMPLETED,
             set(),
             "",
             "f_empty.ToString ('' → '')")

result = message.f_empty.ToInteger(CONTAINER_DATA)
check_result(result,
             CODES_COMPLETION.COMPLETED,
             {CODES_DATA.ERROR_CONVERT},
             _SKIP_CHECK,
             "f_empty.ToInteger ('' → ошибка конвертации)")

result = message.f_empty.ToIntegers(CONTAINER_DATA)
check_result(result,
             CODES_COMPLETION.COMPLETED,
             {CODES_DATA.NO_DATA},
             [],
             "f_empty.ToIntegers ('' → [], vlp=='' → flag_no_data, нет дефолта)")

# --- f_empty_10: vlp="" ---
print("  --- f_empty_10 (vlp='', дефолт 10) ---")

result = message.f_empty_10.ToString(CONTAINER_DATA)
check_result(result,
             CODES_COMPLETION.COMPLETED,
             set(),
             "",
             "f_empty_10.ToString ('' → '')")

result = message.f_empty_10.ToInteger(CONTAINER_DATA)
check_result(result,
             CODES_COMPLETION.COMPLETED,
             {CODES_DATA.ERROR_CONVERT},
             _SKIP_CHECK,
             "f_empty_10.ToInteger ('' → ошибка конвертации)")

result = message.f_empty_10.ToIntegers(CONTAINER_DATA)
check_result(result,
             CODES_COMPLETION.COMPLETED,
             set(),
             [10],
             "f_empty_10.ToIntegers ('' → [10], vlp=='' → flag_no_data, дефолт 10)")

print("")
print("=" * 60)
print("Тест завершён")
print("=" * 60)
