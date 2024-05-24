from G30_cactus_controller_containers import controller_containers
from G30_cactus_struct                import T30_StructCell

print("Тест RAM-Контейнера: Работа с пакетами S-Ячеек")
print("")

container = controller_containers.RegisterContainerRAM("ram")

oci    = "class_01"

cell   = T30_StructCell(oci=oci)
container.DeleteSCells(cell)

result = len(container.ReadSCells(cell).cells) == 0
print(f"{'[+]' if result else '[ ]'} Подготовка контейнера")

oci        = "class_01"
oid        = "object-01"
cells      = []

for index in range(0, 100):
	pid    = f"field-{index}"
	cvl    = f"value-{index}"
	cut    = 1
	cell   = T30_StructCell(oci=oci, oid=oid, pid=pid, cvl=cvl, cut=cut)
	cells.append(cell)

container.WriteSCells(cells)

cell   = T30_StructCell(oci=oci)
result = len(container.ReadSCells(cell).cells) == 100
print(f"{'[+]' if result else '[ ]'} Запись 100 S-Ячеек")

container.DeleteSCells(cell)
result = len(container.ReadSCells(cell).cells) == 0
print(f"{'[+]' if result else '[ ]'} Удаление S-Ячеек")
