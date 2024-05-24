import time

from G00_result_codes                 import RESULT_OK
from G30_cactus_controller_containers import controller_containers
from G30_cactus_frame                 import C30_StructFrame, C30_StructField

print("Тест структурного объекта: Тест передачи данных между контейнерами RAM и SQLite")
print("")


class C40_Book(C30_StructFrame):
	_oci = "Книга"

	def InitFields(self):
		self.f_name    = C30_StructField(self, "Наименование",   "Неизвестно")
		self.f_year    = C30_StructField(self, "Год издания",     1900)
		self.f_author  = C30_StructField(self, "Автор",          "Неизвестно")
		self.f_reprint = C30_StructField(self, "Года переиздания")


container_1 = controller_containers.RegisterContainerRAM("R1")

container_2 = controller_containers.RegisterContainerSQLite("sqlite")
container_2.OptionsFilename("./data.sqlite")
container_2.Connect()

book = C40_Book("Книга 1")

book.RegisterClass("sqlite")

book.RegisterObject("R1")
book.f_name.FromString("R1", "Название 1")
book.f_year.FromInteger("R1", 2000)
book.f_author.FromString("R1", "ХЗ")

book.Oid("Книга 2")
book.RegisterObject("R1")
book.f_name.FromString("R1", "Название 2")
book.f_year.FromInteger("R1", 2020)
book.f_author.FromString("R1", "Йа")

result = book.CopyToContainer("R1", "sqlite").code == RESULT_OK
print(f"{'[+]' if result else '[ ]'} Копирование объекта из контейнера в контейнер")

time.sleep(1)
book.f_year.FromInteger("R1", 2010)

time.sleep(1)
book.f_year.FromInteger("sqlite", 2021)
book.f_author.FromString("R1", "Йорик")

result = book.SyncBetweenContainers("R1", "sqlite").code == RESULT_OK
result = result and book.f_year.ToInteger("R1").value == 2021

result = result and book.f_author.ToString("sqlite").text == "Йорик"
print(f"{'[+]' if result else '[ ]'} Синхронизация объекта между контейнерами")

result_oids = book.Oids("sqlite")
result = result_oids.code == RESULT_OK
oids = result_oids.items
oids.sort()
result = result and oids == ["Книга 2"]
print(f"{'[+]' if result else '[ ]'} Запрос списка oid объектов класса из контейнера")

result_pids = book.Pids("sqlite")
result = result_oids.code == RESULT_OK
pids = result_pids.items
pids.sort()
result = result and pids == ['oci', 'Автор', 'Год издания', 'Наименование']
print(f"{'[+]' if result else '[ ]'} Запрос списка pid S-Ячеек из контейнера")
