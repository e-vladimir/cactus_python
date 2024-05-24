from G00_result_codes                 import RESULT_WARNING_NO_DATA, RESULT_OK
from G30_cactus_controller_containers import controller_containers
from G30_cactus_frame                 import C30_StructFrame, C30_StructField
from G30_cactus_datafilters           import C30_FilterLinear1D

print("Тест линейного объектного S-Фильтра с контейнером RAM")
print("")


PID_NAME    = "Наименование"
PID_YEAR    = "Год издания"
PID_AUTHOR  = "Автор"
PID_REPRINT = "Года переиздания"
PID_PRICE   = "Стоимость"
PID_EXIST   = "Наличие"


class C40_Book(C30_StructFrame):
	_oci = "Книга"

	def InitFields(self):
		self.f_name    = C30_StructField(self, PID_NAME,   "Неизвестно")
		self.f_year    = C30_StructField(self, PID_YEAR,   1900)
		self.f_author  = C30_StructField(self, PID_AUTHOR, "Неизвестно")
		self.f_reprint = C30_StructField(self, PID_REPRINT)
		self.f_price   = C30_StructField(self, PID_PRICE,   0)
		self.f_exist   = C30_StructField(self, PID_EXIST, False)


container       = controller_containers.RegisterContainerRAM("RAM")
book            = C40_Book()
total_sum : int = 0

for index in range(50):
	book.Oid(f"Книга-{index:02d}")
	book.RegisterObject("RAM")
	book.f_author.FromString("RAM", f"Автор-{index}")
	book.f_year.FromInteger("RAM", 1900 + index)
	book.f_price.FromInteger("RAM", 10 + index)
	book.f_exist.FromBoolean("RAM", index % 2 == 0)

	total_sum += (10 + index)

filter_book = C30_FilterLinear1D(book.Oci().text)

print("Проверка без фильтрации")
result = filter_book.Capture("RAM").code == RESULT_OK
print(f"{'[+]' if result else '[ ]'} Захват данных из контейнера RAM")

result = len(filter_book.Oids().items) == 50
print(f"{'[+]' if result else '[ ]'} Запрос OID")

result = len(filter_book.ToStrings(PID_AUTHOR).items) == 50
print(f"{'[+]' if result else '[ ]'} Запрос CVL для PID списком строк")

result = sum(filter_book.ToIntegers(PID_PRICE).items) == total_sum
print(f"{'[+]' if result else '[ ]'} Запрос CVL для PID списком целых чисел")

result = sum(filter_book.ToFloats(PID_PRICE).items) == total_sum
print(f"{'[+]' if result else '[ ]'} Запрос CVL для PID списком дробных чисел")

result = len(filter_book.ToBooleans(PID_EXIST).items) == 50
result = result and sum(filter_book.ToBooleans(PID_EXIST).items) == 25
print(f"{'[+]' if result else '[ ]'} Запрос CVL для PID списком логических значений")

result = len(filter_book.ToDateTimes(PID_REPRINT).items) == 0
print(f"{'[+]' if result else '[ ]'} Запрос CVL для PID списком отметок даты-времени")

print("")
print("Проверка выборок")

filter_book.ResetFiltersPidCvl()
filter_book.FilterPidCvlByEqual(PID_PRICE, 20)
filter_book.Capture("RAM")
result = len(filter_book.Oids().items) == 1
filter_book.ResetFiltersPidCvl()
filter_book.FilterPidCvlByEqual(PID_PRICE, 20, True)
filter_book.Capture("RAM")
result = result and len(filter_book.Oids().items) == 49
print(f"{'[+]' if result else '[ ]'} Фильтрация PID-CVL EQUAL")

filter_book.ResetFiltersPidCvl()
filter_book.FilterPidCvlByMore(PID_PRICE, 20)
filter_book.Capture("RAM")
result = len(filter_book.Oids().items) == 39
filter_book.ResetFiltersPidCvl()
filter_book.FilterPidCvlByMore(PID_PRICE, 20, False, True)
filter_book.Capture("RAM")
result = result and len(filter_book.Oids().items) == 40
filter_book.ResetFiltersPidCvl()
filter_book.FilterPidCvlByMore(PID_PRICE, 20, True, True)
filter_book.Capture("RAM")
result = result and len(filter_book.Oids().items) == 10
print(f"{'[+]' if result else '[ ]'} Фильтрация PID-CVL MORE")

filter_book.ResetFiltersPidCvl()
filter_book.FilterPidCvlByLess(PID_PRICE, 20)
filter_book.Capture("RAM")
result = len(filter_book.Oids().items) == 10
filter_book.ResetFiltersPidCvl()
filter_book.FilterPidCvlByLess(PID_PRICE, 20, False, True)
filter_book.Capture("RAM")
result = result and len(filter_book.Oids().items) == 11
filter_book.ResetFiltersPidCvl()
filter_book.FilterPidCvlByLess(PID_PRICE, 20, True, True)
filter_book.Capture("RAM")
result = result and len(filter_book.Oids().items) == 39
print(f"{'[+]' if result else '[ ]'} Фильтрация PID-CVL LESS")

filter_book.ResetFiltersPidCvl()
filter_book.FilterPidCvlByInclude(PID_AUTHOR, "10")
filter_book.Capture("RAM")
result = len(filter_book.Oids().items) == 1
filter_book.ResetFiltersPidCvl()
filter_book.FilterPidCvlByInclude(PID_AUTHOR, "10", True)
filter_book.Capture("RAM")
result = result and len(filter_book.Oids().items) == 49
print(f"{'[+]' if result else '[ ]'} Фильтрация PID-CVL INCLUDE")

filter_book.ResetFiltersPidCvl()
filter_book.FilterPidCvlByIn(PID_PRICE, [10, 15, 20])
filter_book.Capture("RAM")
result = len(filter_book.Oids().items) == 3
filter_book.ResetFiltersPidCvl()
filter_book.FilterPidCvlByIn(PID_PRICE, [10, 15, 20], True)
filter_book.Capture("RAM")
result = result and len(filter_book.Oids().items) == 47
print(f"{'[+]' if result else '[ ]'} Фильтрация PID-CVL IN")

filter_book.ResetFiltersPidCvl()
filter_book.FilterPidCvlByBetween(PID_PRICE, 20, 30)
filter_book.Capture("RAM")
result = len(filter_book.Oids().items) == 9
filter_book.ResetFiltersPidCvl()
filter_book.FilterPidCvlByBetween(PID_PRICE, 20, 30, False, True)
filter_book.Capture("RAM")
result = result and len(filter_book.Oids().items) == 11
filter_book.ResetFiltersPidCvl()
filter_book.FilterPidCvlByBetween(PID_PRICE, 20, 30, True, True)
filter_book.Capture("RAM")
result = result and len(filter_book.Oids().items) == 39
print(f"{'[+]' if result else '[ ]'} Фильтрация PID-CVL BETWEEN")

