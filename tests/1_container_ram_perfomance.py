import random
import time

from G30_cactus_struct                import T30_StructCell
from G30_cactus_controller_containers import controller_containers

print("Тест RAM-Контейнера: Замер производительности")
print("")

container  = controller_containers.RegisterContainerRAM("RAM")

print("Запись S-Ячеек")

oci        = "class_01"
oid        = "object-01"

for count in range(0, 110000, 10000):
	if count == 0: count = 1000

	container.Clear()

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
print("Перезапись S-Ячеек с режимом пропуска")

oci        = "class_01"
oid        = "object-01"

for count in range(0, 110000, 10000):
	if count == 0: count = 1000

	container.Clear()

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
print("Перезапись S-Ячеек с режимом перезаписи")

oci        = "class_01"
oid        = "object-01"

for count in range(0, 110000, 10000):
	if count == 0: count = 1000

	container.Clear()

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
print("Синхронизация S-Ячеек")

oci        = "class_01"
oid        = "object-01"

for count in range(0, 110000, 10000):
	if count == 0: count = 1000

	container.Clear()

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
print("Запись D-Ячеек")

oci        = "class_01"
oid        = "object-01"

for count in range(0, 110000, 10000):
	if count == 0: count = 1000

	container.Clear()

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

