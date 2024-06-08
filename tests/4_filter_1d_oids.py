from G30_cactus_controller_containers import controller_containers
from G30_cactus_frame                 import C30_StructFrame, C30_StructField
from G30_cactus_datafilters           import C30_FilterLinear1D

print("Тест линейного 1D-Фильтра на выборку OID")
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
		self.f_exist   = C30_StructField(self, PID_EXIST,   False)


container               = controller_containers.RegisterContainerRAM("RAM")
book                    = C40_Book()

oids_source : list[str] = []
oids_source.append("book-1-12")
oids_source.append("book-2-100")
oids_source.append("book-3-110")
oids_source.append("book-4-300")
oids_source.append("book-5-200")
oids_source.append("book-6-250")
oids_source.append("book-7-500")
oids_source.append("book-8-1000")
oids_source.append("book-9-1000")

prices_source : list[int] = []
prices_source.append(12)
prices_source.append(100)
prices_source.append(110)
prices_source.append(300)
prices_source.append(200)
prices_source.append(250)
prices_source.append(500)
prices_source.append(1000)
prices_source.append(1000)

for index_item in range(len(oids_source)):
	book.Oid(oids_source[index_item])
	book.RegisterObject("RAM")
	book.f_price.FromInteger("RAM", prices_source[index_item])


filter_1d = C30_FilterLinear1D(book.Oci().text)
filter_1d.Capture("RAM")

print("Проверка без фильтрации")
oids_result : list[str] = filter_1d.Oids().items
result = set(oids_result) == set(oids_source)
print(f"{'[+]' if result else '[ ]'} Выборка OID без фильтрации")

print('')

print("Проверка с фильтрацией")
oids_result : list[str] = filter_1d.Oids(book.f_price.Pid().text).items
result = oids_result == ["book-1-12", "book-2-100", "book-3-110", "book-5-200", "book-6-250", "book-4-300", "book-7-500", "book-8-1000", "book-9-1000"]
print(f"{'[+]' if result else '[ ]'} Выборка OID с сортировкой по PID")

print('')
print("Проверка с фильтрацией и уникальностью")
values_result : list[str] = filter_1d.ToIntegers(book.f_price.Pid().text, True, True).items
result = values_result == [12, 100, 110, 200, 250, 300, 500, 1000]
print(f"{'[+]' if result else '[ ]'} Выборка PID с сортировкой и уникальностью")
