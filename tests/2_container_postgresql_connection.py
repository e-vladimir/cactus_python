from G00_result_codes                 import RESULT_OK
from G30_cactus_controller_containers import controller_containers

print("Тест PostgreSQL-Контейнера: Работа с подключением")
print("")

container = controller_containers.RegisterContainerPostgreSQL("postgresql")
container.OptionsServerIp("195.161.41.96")
container.OptionsServerTcpPort(5432)
container.OptionsServerDBase("fin_sync")
container.OptionsServerLogin("a6540920979")
container.OptionsServerPassword('!-dg7/X"0c@JqSOd')

result = container.Connect().code == RESULT_OK
print(f"{'[+]' if result else '[ ]'} Подключение к контейнеру")

result = container.Disconnect().code == RESULT_OK
print(f"{'[+]' if result else '[ ]'} Отключение от контейнера")

container.AutoconnectIsAuto(True)

oci    = "class_01"
result = container.RegisterClass(oci).code == RESULT_OK
print(f"{'[+]' if result else '[ ]'} Регистрация класса")

result = container.Disconnect().code == RESULT_OK
print(f"{'[+]' if result else '[ ]'} Отключение от контейнера")
