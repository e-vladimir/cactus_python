import time

from G00_result_codes                 import RESULT_OK
from G30_cactus_controller_containers import controller_containers
from G30_cactus_frame                 import C30_StructFrame, C30_StructField

print("Тест структурного параметра: Тест передачи данных между контейнерами RAM и SQLite")
print("")


class C40_Book(C30_StructFrame):
	_oci = "Книга"

	def InitFields(self):
		self.f_name    = C30_StructField(self, "Наименование",   "Неизвестно")
		self.f_year    = C30_StructField(self, "Год издания",     1900)
		self.f_author  = C30_StructField(self, "Автор",          "Неизвестно")
		self.f_reprint = C30_StructField(self, "Года переиздания")


book      = C40_Book("Книга 1")

container_1 = controller_containers.RegisterContainerRAM("R1")

container_2 = controller_containers.RegisterContainerSQLite("sqlite")
container_2.OptionsFilename("./data.sqlite")
container_2.Connect()

book.RegisterClass("sqlite")

book.f_name.FromString("R1", "001")
result = book.f_name.CopyToContainer("R1", "sqlite").code == RESULT_OK
print(f"{'[+]' if result else '[ ]'} Копирование S-Ячейки из контейнера в контейнер")

time.sleep(1)

book.f_name.FromString("R1", "Название 1")
result = book.f_name.SyncBetweenContainers("R1", "sqlite").code == RESULT_OK
result = result and book.f_name.ToString("R1").text == book.f_name.ToString("sqlite").text
print(f"{'[+]' if result else '[ ]'} Синхронизация S-Ячейки между контейнерами")

result = book.f_name.DeleteFromContainer("sqlite").code == RESULT_OK
print(f"{'[+]' if result else '[ ]'} Удаление S-Ячейки из контейнера")
