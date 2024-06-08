from G00_result_codes                 import RESULT_OK
from G20_cactus_struct import T20_StructCell
from G21_struct_result import T21_StructRange
from G30_cactus_controller_containers import controller_containers


print("Тест RAM-Контейнера: Работа с D-Ячейкой")
print("")

container = controller_containers.RegisterContainerRAM("RAM")

oci    = "class_01"
oid    = "object-01"
pid    = "field-01"
cvl    = "value-01"
cut    = 100
cell   = T20_StructCell(oci=oci, oid=oid, pid=pid, cvl=cvl, cut=cut)
result = container.WriteDCell(cell).code == RESULT_OK
print(f"{'[+]' if result else '[ ]'} Запись D-Ячейки")
cell   = T20_StructCell(oci=oci, oid=oid, pid=pid, cut=cut)
cell   = container.ReadDCell(cell).cell
result = True
if   not cell.oci == oci: result = False
elif not cell.oid == oid: result = False
elif not cell.pid == pid: result = False
elif not cell.cvl == cvl: result = False
elif not cell.cut == cut: result = False
print(f"{'[+]' if result else '[ ]'} Чтение D-Ячейки")

cvl    = "value-02"
cut    = 100
cell   = T20_StructCell(oci=oci, oid=oid, pid=pid, cvl=cvl, cut=cut)
container.WriteDCell(cell)
cell   = T20_StructCell(oci=oci, oid=oid, pid=pid, cut=cut)
cell   = container.ReadDCell(cell).cell
result = True
if   not cell.oci == oci: result = False
elif not cell.oid == oid: result = False
elif not cell.pid == pid: result = False
elif not cell.cvl == cvl: result = False
elif not cell.cut == cut: result = False
print(f"{'[+]' if result else '[ ]'} Перезапись D-Ячейки")

for cut in range(1, 11):
	cvl    = f"value-{cut:02d}"
	cell   = T20_StructCell(oci=oci, oid=oid, pid=pid, cvl=cvl, cut=cut)
	container.WriteDCell(cell)

cell   = T21_StructRange(oci=oci, oid=oid, pid=pid)
drange = container.DCutRange(cell).range
result = True
if not drange.cut_l ==   1: result = False
if not drange.cut_r == 100: result = False
print(f"{'[+]' if result else '[ ]'} Запрос диапазона D-Ячейки")

cell   = T21_StructRange(oci=oci, oid=oid, pid=pid, cut_l=1, cut_r=5)
cuts   = container.DCuts(cell)
result = cuts.items == [1, 2, 3, 4, 5]
print(f"{'[+]' if result else '[ ]'} Запрос списка CUT")

for cut in range(11):
	cell   = T20_StructCell(oci=oci, oid=oid, pid=pid, cut=cut)
	container.DeleteDCell(cell)

result = len(container._d_cells) == 1
print(f"{'[+]' if result else '[ ]'} Удаление D-Ячейки (10 шт)")
