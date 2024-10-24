# ТЕСТИРОВАНИЕ КОНТЕЙНЕРА-SQL.PostgreSQL
# 24 окт 2024

import time

import pytest

from   G00_status_codes         import *

from   G32_cactus_container_sql import C32_ContainerPostgreSQL

print("")
print("[== Тест Контейнера-SQL-PostgreSQL ==]")

@pytest.mark.default
@pytest.mark.sql
@pytest.mark.postgresql
def test_container_sql_postgresql():
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
	if not check: print(f"                  {result.code} {result.subcodes}\n")
	assert check

	time_0 = time.time()
	result    = container.Connect()
	time_1 = time.time()
	check     = (result.code        == CODES_COMPLETION.COMPLETED)
	print(f"{(time_1 - time_0):0.3f} сек  ", f"{'[+]' if check else '[ ]'} Подключение к контейнеру")
	if not check: print(f"                  {result.code} {result.subcodes}\n")
	assert check

	time_0 = time.time()
	result    = container.StateConnected()
	time_1 = time.time()
	check     = (result.code        == CODES_COMPLETION.COMPLETED)
	check    &= result.data == True
	print(f"{(time_1 - time_0):0.3f} сек  ", f"{'[+]' if check else '[ ]'} Проверка состояния контейнера после подключения")
	if not check: print(f"                  {result.code} {result.subcodes}\n")
	assert check

	time_0 = time.time()
	result    = container.Disconnect()
	time_1 = time.time()
	check     = (result.code        == CODES_COMPLETION.COMPLETED)
	print(f"{(time_1 - time_0):0.3f} сек  ", f"{'[+]' if check else '[ ]'} Отключение от контейнера")
	if not check: print(f"                  {result.code} {result.subcodes}\n")
	assert check

	time_0 = time.time()
	result    = container.StateConnected()
	time_1 = time.time()
	check     = (result.code        == CODES_COMPLETION.COMPLETED)
	check    &= result.data == False
	print(f"{(time_1 - time_0):0.3f} сек  ", f"{'[+]' if check else '[ ]'} Проверка состояния контейнера после отключения")
	if not check: print(f"                  {result.code} {result.subcodes}\n")
	assert check

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
	if not check: print(f"                  {result.code} {result.subcodes}\n")
	assert check
