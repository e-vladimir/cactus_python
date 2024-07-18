# ТЕСТИРОВАНИЕ КОНТЕЙНЕРА-SQL: SQLITE
# 17 июл 2024

import time

from   G00_status_codes         import *

from   G32_cactus_container_sql import C32_ContainerPostgreSQL

print("")
print("[== Тест Контейнера-SQL-PostgreSQL ==]")

container = C32_ContainerPostgreSQL()
container.OptionsServerIp("195.161.41.96")
container.OptionsServerTcpPort(5432)
container.OptionsServerLogin("a6540920979")
container.OptionsServerPassword("!-dg7/X\"0c@JqSOd")
container.OptionsServerDBase("cactus-test")

time_0 = time.time()
result    = container.StateConnected()
time_1 = time.time()
check     = (result.code        == CODES_COMPLETION.COMPLETED)
check    &= result.data == False
print(f"{(time_1 - time_0):0.3f} сек  ", f"{'[+]' if check else '[ ]'} Проверка состояния контейнера после инициализации")

time_0 = time.time()
result    = container.Connect()
time_1 = time.time()
check     = (result.code        == CODES_COMPLETION.COMPLETED)
print(f"{(time_1 - time_0):0.3f} сек  ", f"{'[+]' if check else '[ ]'} Подключение к контейнеру")

time_0 = time.time()
result    = container.StateConnected()
time_1 = time.time()
check     = (result.code        == CODES_COMPLETION.COMPLETED)
check    &= result.data == True
print(f"{(time_1 - time_0):0.3f} сек  ", f"{'[+]' if check else '[ ]'} Проверка состояния контейнера после подключения")

time_0 = time.time()
result    = container.Disconnect()
time_1 = time.time()
check     = (result.code        == CODES_COMPLETION.COMPLETED)
print(f"{(time_1 - time_0):0.3f} сек  ", f"{'[+]' if check else '[ ]'} Отключение от контейнера SQLite")

time_0 = time.time()
result    = container.StateConnected()
time_1 = time.time()
check     = (result.code        == CODES_COMPLETION.COMPLETED)
check    &= result.data == False
print(f"{(time_1 - time_0):0.3f} сек  ", f"{'[+]' if check else '[ ]'} Проверка состояния контейнера после отключения")

container.DisconnectMode_Timeout(True)
container.DisconnectTimeout(2)

container.Connect()
for index in range(6):
	time.sleep(1)
	result = container.StateConnected()
	print(f"[{5 - index}] Текущее состояние: {'Подключено' if result.data else 'Отключено'}")

time_0 = time.time()
result    = container.StateConnected()
time_1 = time.time()
check     = (result.code        == CODES_COMPLETION.COMPLETED)
check    &= result.data == False
print(f"{(time_1 - time_0):0.3f} сек  ", f"{'[+]' if check else '[ ]'} Проверка состояния контейнера после авто-отключения")
