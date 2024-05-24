import random

from G30_cactus_struct                import T30_StructCell, T31_StructRange
from G30_cactus_controller_containers import controller_containers


count = 100

print("Тест PostgreSQL-Контейнера: Работа с D-Ячейками")
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
container.DeleteDCells(T31_StructRange(oci=oci))

result = len(container.ReadDCells(T31_StructRange(oci=oci)).cells) == 0
print(f"{'[+]' if result else '[ ]'} Проверка удаления всех D-Ячеек")

oci        = "class_01"
oid        = "object-01"
cells      = []

for index in range(count):
	pid    = f"field-{random.randint(0, count)}"
	cvl    = f"value-{random.randint(0, count)}"
	cut    = random.randint(0, 100000)
	cell   = T30_StructCell(oci=oci, oid=oid, pid=pid, cvl=cvl, cut=cut)
	cells.append(cell)

container.WriteDCells(cells)
result = len(container.ReadDCells(T31_StructRange(oci=oci)).cells) == count
print(f"{'[+]' if result else '[ ]'} Проверка записи {count} D-Ячеек")

container.DeleteDCells(T31_StructRange(oci=oci))
result = len(container.ReadDCells(T31_StructRange(oci=oci)).cells) == 0
print(f"{'[+]' if result else '[ ]'} Проверка удаления всех D-Ячеек")
