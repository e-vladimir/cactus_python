# ТЕСТИРОВАНИЕ ПРОИЗВОДИТЕЛЬНОСТИ КОНТЕЙНЕРА SQLite
# 09 окт 2026

import random
import time

from   G20_cactus_structs       import T20_StructCell
from   G32_cactus_container_sql import C32_ContainerPostgreSQL

COUNT = 1000


print("Тест Контейнера-SQL.PostgreSQL: Замер производительности")
print("")


container = C32_ContainerPostgreSQL()
container.OptionsServerIp("")
container.OptionsServerTcpPort(5432)
container.OptionsServerLogin("")
container.OptionsServerPassword("")
container.OptionsServerDBase("")
container.Connect()

oci    = "class_01"
container.RegisterClass(oci)

print(f"Запись {COUNT} S-Ячеек")

oci        = "class_01"
oid        = "object-01"

time_0     = time.time()
for index in range(COUNT):
	pid    = f"field-{index}"
	cvl    = f"value-{index}"
	cut    = 1
	cell   = T20_StructCell(oci, oid, pid, cvl, cut)
	container.WriteSCell(cell)

time_1     = time.time()
time_delta = time_1 - time_0
print(f"{COUNT:6d} ячеек записано за {time_delta:0.5f} сек = {(time_delta / COUNT):0.10f} сек на операцию")

print("")
print(f"Перезапись {COUNT} S-Ячеек с режимом пропуска")

oci        = "class_01"
oid        = "object-01"

time_0     = time.time()
for index in range(COUNT):
	pid    = f"field-{random.randint(0, COUNT)}"
	cvl    = f"value-{random.randint(0, COUNT)}"
	cut    = random.randint(0, 100000)
	cell   = T20_StructCell(oci, oid, pid, cvl, cut)
	container.WriteSCell(cell, False)

time_1     = time.time()
time_delta = time_1 - time_0
print(f"{COUNT:6d} ячеек перезаписано за {time_delta:0.5f} сек = {(time_delta / COUNT):0.10f} сек на операцию")

print("")
print(f"Перезапись {COUNT} S-Ячеек с режимом перезаписи")

oci        = "class_01"
oid        = "object-01"

time_0     = time.time()
for index in range(COUNT):
	pid    = f"field-{random.randint(0, COUNT)}"
	cvl    = f"value-{random.randint(0, COUNT)}"
	cut    = random.randint(0, 100000)
	cell   = T20_StructCell(oci, oid, pid, cvl, cut)
	container.WriteSCell(cell)

time_1     = time.time()
time_delta = time_1 - time_0
print(f"{COUNT:6d} ячеек перезаписано за {time_delta:0.5f} сек = {(time_delta / COUNT):0.10f} сек на операцию")

print("")
print(f"Синхронизация {COUNT} S-Ячеек")

oci        = "class_01"
oid        = "object-01"

time_0     = time.time()
for index in range(COUNT):
	pid    = f"field-{random.randint(0, COUNT)}"
	cvl    = f"value-{random.randint(0, COUNT)}"
	cut    = random.randint(0, 100000)
	cell   = T20_StructCell(oci, oid, pid, cvl, cut)
	container.SyncSCell(cell)

time_1     = time.time()
time_delta = time_1 - time_0
print(f"{COUNT:6d} ячеек синхронизировано за {time_delta:0.5f} сек = {(time_delta / COUNT):0.10f} сек на операцию")

print("")
print(f"Запись {COUNT} D-Ячеек")

oci        = "class_01"
oid        = "object-01"

time_0     = time.time()
for index in range(COUNT):
	pid    = f"field-{random.randint(0, COUNT)}"
	cvl    = f"value-{random.randint(0, COUNT)}"
	cut    = random.randint(0, 100000)
	cell   = T20_StructCell(oci, oid, pid, cvl, cut)
	container.WriteDCell(cell)

time_1     = time.time()
time_delta = time_1 - time_0
print(f"{COUNT:6d} ячеек записано за {time_delta:0.5f} сек = {(time_delta / COUNT):0.10f} сек на операцию")

print("")
print("===============")
print("Замер производительности пакетного режима")
cells = []

oci        = "class_01"
oid        = "object-01"

for index in range(COUNT):
	pid    = f"field-{random.randint(0, COUNT)}"
	cvl    = f"value-{random.randint(0, COUNT)}"
	cut    = random.randint(0, 100000)
	cell   = T20_StructCell(oci, oid, pid, cvl, cut)
	cells.append(cell)

print(f"Запись {COUNT} S-Ячеек")

time_0     = time.time()
container.WriteSCells(cells)
time_1     = time.time()
time_delta = time_1 - time_0
print(f"{COUNT:6d} ячеек записано за {time_delta:0.5f} сек = {(time_delta / COUNT):0.10f} сек на операцию")

print("")
print(f"Перезапись {COUNT} S-Ячеек с режимом перезаписи")

time_0     = time.time()
container.WriteSCells(cells)
time_1     = time.time()
time_delta = time_1 - time_0
print(f"{COUNT:6d} ячеек перезаписано за {time_delta:0.5f} сек = {(time_delta / COUNT):0.10f} сек на операцию")


print("")
print(f"Синхронизация {COUNT} S-Ячеек")
time_0     = time.time()
container.SyncSCells(cells)
time_1     = time.time()
time_delta = time_1 - time_0
print(f"{COUNT:6d} ячеек синхронизировано за {time_delta:0.5f} сек = {(time_delta / COUNT):0.10f} сек на операцию")
