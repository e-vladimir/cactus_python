# ТЕСТИРОВАНИЕ КОНТЕЙНЕРА-SQL: SQLITE
# 08 июл 2024

import time

from   G00_status_codes         import *

from   G32_cactus_container_sql import C32_ContainerSQLite

print("")
print("[== Тест Контейнера-SQL-SQLite ==]")

container = C32_ContainerSQLite()
container.OptionsFilename("./data.sqlite")

result    = container.StateConnected()
check     = (result.code        == CODES_COMPLETION.COMPLETED)
check    &= result.data == False
print(f"{'[+]' if check else '[ ]'} Проверка состояния контейнера после инициализации")

result    = container.Connect()
check     = (result.code        == CODES_COMPLETION.COMPLETED)
print(f"{'[+]' if check else '[ ]'} Подключение к контейнеру SQLite (data.sqlite)")

result    = container.StateConnected()
check     = (result.code        == CODES_COMPLETION.COMPLETED)
check    &= result.data == True
print(f"{'[+]' if check else '[ ]'} Проверка состояния контейнера после подключения")

result    = container.Disconnect()
check     = (result.code        == CODES_COMPLETION.COMPLETED)
print(f"{'[+]' if check else '[ ]'} Отключение от контейнера SQLite")

result    = container.StateConnected()
check     = (result.code        == CODES_COMPLETION.COMPLETED)
check    &= result.data == False
print(f"{'[+]' if check else '[ ]'} Проверка состояния контейнера после отключения")

container.DisconnectMode_Timeout(True)
container.DisconnectTimeout(2)

container.Connect()
for index in range(6):
	time.sleep(1)
	result = container.StateConnected()
	print(f"[{5 - index}] Текущее состояние: {'Подключено' if result.data else 'Отключено'}")

result    = container.StateConnected()
check     = (result.code        == CODES_COMPLETION.COMPLETED)
check    &= result.data == False
print(f"{'[+]' if check else '[ ]'} Проверка состояния контейнера после авто-отключения")
