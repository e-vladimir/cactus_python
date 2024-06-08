import random
import time

from G30_cactus_struct                import T30_StructCell
from G30_cactus_controller_containers import controller_containers

count = 1000

print("Тест PostgreSQL-Контейнера: Замер производительности")
print("")

container = controller_containers.RegisterContainerPostgreSQL("postgresql")
container.OptionsServerIp("195.161.41.96")
container.OptionsServerTcpPort(5432)
container.OptionsServerDBase("fin_sync")
container.OptionsServerLogin("a6540920979")
container.OptionsServerPassword('!-dg7/X"0c@JqSOd')
container.Connect()

oci    = "class_01"
container.RegisterClass(oci)

print(f"Запись {count} S-Ячеек")

oci        = "class_01"
oid        = "object-01"

time_0     = time.time()
for index in range(count):
	pid    = f"field-{index}"
	cvl    = f"value-{index}"
	cut    = 1
	cell   = T30_StructCell(oci=oci, oid=oid, pid=pid, cvl=cvl, cut=cut)
	container.WriteSCell(cell)

time_1     = time.time()
time_delta = time_1 - time_0
print(f"{count:6d} ячеек записано за {time_delta:0.5f} сек = {(time_delta / count):0.10f} сек на операцию")

print("")
print(f"Перезапись {count} S-Ячеек с режимом пропуска")

oci        = "class_01"
oid        = "object-01"

time_0     = time.time()
for index in range(count):
	pid    = f"field-{random.randint(0, count)}"
	cvl    = f"value-{random.randint(0, count)}"
	cut    = random.randint(0, 100000)
	cell   = T30_StructCell(oci=oci, oid=oid, pid=pid, cvl=cvl, cut=cut)
	container.WriteSCell(cell, False)

time_1     = time.time()
time_delta = time_1 - time_0
print(f"{count:6d} ячеек перезаписано за {time_delta:0.5f} сек = {(time_delta / count):0.10f} сек на операцию")

print("")
print(f"Перезапись {count} S-Ячеек с режимом перезаписи")

oci        = "class_01"
oid        = "object-01"

time_0     = time.time()
for index in range(count):
	pid    = f"field-{random.randint(0, count)}"
	cvl    = f"value-{random.randint(0, count)}"
	cut    = random.randint(0, 100000)
	cell   = T30_StructCell(oci=oci, oid=oid, pid=pid, cvl=cvl, cut=cut)
	container.WriteSCell(cell)

time_1     = time.time()
time_delta = time_1 - time_0
print(f"{count:6d} ячеек перезаписано за {time_delta:0.5f} сек = {(time_delta / count):0.10f} сек на операцию")

print("")
print(f"Синхронизация {count} S-Ячеек")

oci        = "class_01"
oid        = "object-01"

time_0     = time.time()
for index in range(count):
	pid    = f"field-{random.randint(0, count)}"
	cvl    = f"value-{random.randint(0, count)}"
	cut    = random.randint(0, 100000)
	cell   = T30_StructCell(oci=oci, oid=oid, pid=pid, cvl=cvl, cut=cut)
	container.SyncSCell(cell)

time_1     = time.time()
time_delta = time_1 - time_0
print(f"{count:6d} ячеек синхронизировано за {time_delta:0.5f} сек = {(time_delta / count):0.10f} сек на операцию")

print("")
print(f"Запись {count} D-Ячеек")

oci        = "class_01"
oid        = "object-01"

time_0     = time.time()
for index in range(count):
	pid    = f"field-{random.randint(0, count)}"
	cvl    = f"value-{random.randint(0, count)}"
	cut    = random.randint(0, 100000)
	cell   = T30_StructCell(oci=oci, oid=oid, pid=pid, cvl=cvl, cut=cut)
	container.WriteDCell(cell)

time_1     = time.time()
time_delta = time_1 - time_0
print(f"{count:6d} ячеек записано за {time_delta:0.5f} сек = {(time_delta / count):0.10f} сек на операцию")

print("")
print("===============")
print("Замер производительности пакетного режима")
cells = []

oci        = "class_01"
oid        = "object-01"

for index in range(count):
	pid    = f"field-{random.randint(0, count)}"
	cvl    = f"value-{random.randint(0, count)}"
	cut    = random.randint(0, 100000)
	cell   = T30_StructCell(oci=oci, oid=oid, pid=pid, cvl=cvl, cut=cut)
	cells.append(cell)

print(f"Запись {count} S-Ячеек")

time_0     = time.time()
container.WriteSCells(cells)
time_1     = time.time()
time_delta = time_1 - time_0
print(f"{count:6d} ячеек записано за {time_delta:0.5f} сек = {(time_delta / count):0.10f} сек на операцию")

print("")
print(f"Перезапись {count} S-Ячеек с режимом перезаписи")

time_0     = time.time()
container.WriteSCells(cells)
time_1     = time.time()
time_delta = time_1 - time_0
print(f"{count:6d} ячеек перезаписано за {time_delta:0.5f} сек = {(time_delta / count):0.10f} сек на операцию")


print("")
print(f"Синхронизация {count} S-Ячеек")
time_0     = time.time()
container.SyncSCells(cells)
time_1     = time.time()
time_delta = time_1 - time_0
print(f"{count:6d} ячеек синхронизировано за {time_delta:0.5f} сек = {(time_delta / count):0.10f} сек на операцию")
