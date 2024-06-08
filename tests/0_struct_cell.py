from G30_cactus_struct import T30_StructCell

print("Тест регенерации параметров sid, cid структурой ячейки")
print("")

print("[+] Инициализация структурной ячейки")
oci = "class_01"
oid = "object-01"
pid = "field-01"
cvl = "00"
cut = 1
sid = f"{oid}.{pid}"
cid = f"{oci}.{oid}.{pid}"

cell = T30_StructCell(oci=oci, oid=oid, pid=pid, cvl=cvl, cut=cut)
result = f"{oid}.{pid}" == cell.sid
print(f"{'[+]' if result else '[  ]'} Проверка sid после инициализации")
result = f"{oci}.{oid}.{pid}" == cell.cid
print(f"{'[+]' if result else '[  ]'} Проверка cid после инициализации")

pid = "field-02"
cell.pid = pid

result = f"{oid}.{pid}" == cell.sid
print(f"{'[+]' if result else '[  ]'} Проверка sid после изменения параметров")
result = f"{oci}.{oid}.{pid}" == cell.cid
print(f"{'[+]' if result else '[  ]'} Проверка cid после изменения параметров")
