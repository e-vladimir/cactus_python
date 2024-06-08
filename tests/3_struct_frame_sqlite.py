from G00_result_codes                 import RESULT_OK
from G30_cactus_controller_containers import controller_containers
from G30_cactus_frame                 import C30_StructFrame

print("Тест структурного объекта: Работа с контейнером SQLite")
print("")


class C40_Book(C30_StructFrame):
	_oci = "Книга"


book = C40_Book()

container = controller_containers.RegisterContainerSQLite("sqlite")
container.OptionsFilename("./data.sqlite")
container.Connect()

result = book.RegisterClass("sqlite").code == RESULT_OK
print(f"{'[+]' if result else '[ ]'} Регистрация класса")
