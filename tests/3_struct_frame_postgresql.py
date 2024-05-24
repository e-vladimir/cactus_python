from G00_result_codes                 import RESULT_OK
from G30_cactus_controller_containers import controller_containers
from G30_cactus_frame                 import C30_StructFrame

print("Тест структурного объекта: Работа с контейнером PostgreSQL")
print("")


class C40_Book(C30_StructFrame):
	_oci = "Книга"


book = C40_Book()

container = controller_containers.RegisterContainerPostgreSQL("postgresql")
container.OptionsServerIp("195.161.41.96")
container.OptionsServerTcpPort(5432)
container.OptionsServerDBase("fin_sync")
container.OptionsServerLogin("a6540920979")
container.OptionsServerPassword('!-dg7/X"0c@JqSOd')
container.Connect()

result = book.RegisterClass("postgresql").code == RESULT_OK
print(f"{'[+]' if result else '[ ]'} Регистрация класса")
