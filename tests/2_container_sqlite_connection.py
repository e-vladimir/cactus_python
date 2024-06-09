from G00_result_codes                 import RESULT_OK
from G30_cactus_controller_containers import controller_containers

print("Тест SQLite-Контейнера: Работа с подключением")
print("")

container = controller_containers.RegisterContainerSQLite("sqlite")
container.OptionsFilename("./data.sqlite")
result = container.Connect().code == RESULT_OK
print(f"{'[+]' if result else '[ ]'} Подключение к контейнеру")

result = container.Disconnect().code == RESULT_OK
print(f"{'[+]' if result else '[ ]'} Отключение от контейнера")

container.ConnectMode_Auto(True)

oci    = "class_01"
result = container.RegisterClass(oci).code == RESULT_OK
print(f"{'[+]' if result else '[ ]'} Регистрация класса")

result = container.Disconnect().code == RESULT_OK
print(f"{'[+]' if result else '[ ]'} Отключение от контейнера")
