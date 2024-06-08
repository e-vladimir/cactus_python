from G00_result_codes                 import RESULT_OK
from G30_cactus_controller_containers import controller_containers
from G30_cactus_frame                 import C30_StructFrame

print("Тест структурного объекта: Общая проверка с контейнером RAM")
print("")


class C40_Book(C30_StructFrame):
	_oci = "Книга"


book = C40_Book()
result = book.Oci().text == "книга"
print(f"{'[+]' if result else '[ ]'} Запрос OCI")

result = book.GenerateOid().code == RESULT_OK
print(f"{'[+]' if result else '[ ]'} Генерация OID")

result = not book.Oid().text == ""
print(f"{'[+]' if result else '[ ]'} Запрос OID")

result = book.Oid("123").code == RESULT_OK
result = result and (not book.Oid().text == "")
print(f"{'[+]' if result else '[ ]'} Установка OID")

result = not book.Oid("1.22").code == RESULT_OK
print(f"{'[+]' if result else '[ ]'} Проверка валидации OID")


container = controller_containers.RegisterContainerRAM("RAM")

result = book.RegisterObject("RAM").code == RESULT_OK
result = result and len(container._s_cells) == 1
print(f"{'[+]' if result else '[ ]'} Регистрация объекта")

result = book.DeleteObject("RAM").code == RESULT_OK
result = result and len(container._s_cells) == 0
print(f"{'[+]' if result else '[ ]'} Удаление объекта из контейнера")

