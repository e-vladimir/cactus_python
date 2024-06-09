import time

from G00_result_codes                 import RESULT_OK
from G30_cactus_controller_containers import controller_containers

print("Тест SQLite-Контейнера: Работа с автоотключением")
print("")

container = controller_containers.RegisterContainerSQLite("sqlite")
container.OptionsFilename("./data.sqlite")
result = container.Connect().code == RESULT_OK
print(f"{'[+]' if result else '[ ]'} Подключение к контейнеру")

container.DisconnectMode_Timeout(True)
container.DisconnectTimeout(3)

container.PrepareDisconnect()

for second in range(1, 6):
	time.sleep(1)
	result = container.ConnectionState().flag
	print(f"{'[+]' if result else '[ ]'} Состояние подключения. Секунда: {second}")
