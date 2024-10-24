# ТЕСТИРОВАНИЕ ПРОИЗВОДИТЕЛЬНОСТИ КОНТЕЙНЕРА SQLite
# 24 окт 2024
import os
import random
import time

import pytest

from G20_cactus_struct                import T20_StructCell
from G30_cactus_controller_containers import controller_containers

count = 1

print("Тест SQLite-Контейнера: Замер производительности")
print("")

try   : os.remove("./data.sqlite")
except: pass

container  = controller_containers.RegisterContainerSQLite("SQL")
container.OptionsFilename("./data")
container.Connect()

oci    = "class_01"
container.RegisterClass(oci)

def s_cells_write():
	print(f"Запись {count} S-Ячеек")

	oci        = "class_01"
	oid        = "object-01"

	time_0     = time.time()
	for index in range(count):
		pid    = f"field-{index}"
		cvl    = f"value-{index}"
		cut    = 1
		cell   = T20_StructCell(oci, oid, pid, cvl, cut)
		container.WriteSCell(cell)

	time_1     = time.time()
	time_delta = time_1 - time_0
	print(f"{count:6d} ячеек записано за {time_delta:0.5f} сек = {(time_delta / count):0.10f} сек на операцию")

@pytest.mark.perfomance
def test_s_cells_write(benchmark):
	benchmark(s_cells_write)


def s_cells_write_skip():
	print(f"Перезапись {count} S-Ячеек с режимом пропуска")

	oci        = "class_01"
	oid        = "object-01"

	time_0     = time.time()
	for index in range(count):
		pid    = f"field-{random.randint(0, count)}"
		cvl    = f"value-{random.randint(0, count)}"
		cut    = random.randint(0, 100000)
		cell   = T20_StructCell(oci, oid, pid, cvl, cut)
		container.WriteSCell(cell, False)

	time_1     = time.time()
	time_delta = time_1 - time_0
	print(f"{count:6d} ячеек перезаписано за {time_delta:0.5f} сек = {(time_delta / count):0.10f} сек на операцию")

@pytest.mark.perfomance
def test_s_cells_write_skip(benchmark):
	benchmark(s_cells_write_skip)


def s_cells_write_rewrite():
	print(f"Перезапись {count} S-Ячеек с режимом перезаписи")

	oci        = "class_01"
	oid        = "object-01"

	time_0     = time.time()
	for index in range(count):
		pid    = f"field-{random.randint(0, count)}"
		cvl    = f"value-{random.randint(0, count)}"
		cut    = random.randint(0, 100000)
		cell   = T20_StructCell(oci, oid, pid, cvl, cut)
		container.WriteSCell(cell)

	time_1     = time.time()
	time_delta = time_1 - time_0
	print(f"{count:6d} ячеек перезаписано за {time_delta:0.5f} сек = {(time_delta / count):0.10f} сек на операцию")

@pytest.mark.perfomance
def test_s_cells_write_rewrite(benchmark):
	benchmark(s_cells_write_rewrite)


def s_cells_sync():
	print(f"Синхронизация {count} S-Ячеек")

	oci        = "class_01"
	oid        = "object-01"

	time_0     = time.time()
	for index in range(count):
		pid    = f"field-{random.randint(0, count)}"
		cvl    = f"value-{random.randint(0, count)}"
		cut    = random.randint(0, 100000)
		cell   = T20_StructCell(oci, oid, pid, cvl, cut)
		container.SyncSCell(cell)

	time_1     = time.time()
	time_delta = time_1 - time_0
	print(f"{count:6d} ячеек синхронизировано за {time_delta:0.5f} сек = {(time_delta / count):0.10f} сек на операцию")

@pytest.mark.perfomance
def test_s_cells_sync(benchmark):
	benchmark(s_cells_sync)


def d_cells_write():
	print(f"Запись {count} D-Ячеек")

	oci        = "class_01"
	oid        = "object-01"

	time_0     = time.time()
	for index in range(count):
		pid    = f"field-{random.randint(0, count)}"
		cvl    = f"value-{random.randint(0, count)}"
		cut    = random.randint(0, 100000)
		cell   = T20_StructCell(oci, oid, pid, cvl, cut)
		container.WriteDCell(cell)

	time_1     = time.time()
	time_delta = time_1 - time_0
	print(f"{count:6d} ячеек записано за {time_delta:0.5f} сек = {(time_delta / count):0.10f} сек на операцию")

@pytest.mark.perfomance
def test_d_cells_write(benchmark):
	benchmark(d_cells_write)


@pytest.fixture
def cells():
	""" Fixture-зависимость для тестов """
	print("Замер производительности пакетного режима")
	cells = []

	oci        = "class_01"
	oid        = "object-01"

	for index in range(count):
		pid    = f"field-{random.randint(0, count)}"
		cvl    = f"value-{random.randint(0, count)}"
		cut    = random.randint(0, 100000)
		cell   = T20_StructCell(oci, oid, pid, cvl, cut)
		cells.append(cell)
	return cells


def pkg_s_cells_write(cells):
	print(f"Запись {count} S-Ячеек")

	time_0     = time.time()
	container.WriteSCells(cells)
	time_1     = time.time()
	time_delta = time_1 - time_0
	print(f"{count:6d} ячеек записано за {time_delta:0.5f} сек = {(time_delta / count):0.10f} сек на операцию")

@pytest.mark.perfomance
def test_pkg_s_cells_write(benchmark, cells):
	benchmark(pkg_s_cells_write, cells)


def pkg_s_cells_write_rewrite(cells):
	print(f"Перезапись {count} S-Ячеек с режимом перезаписи")

	time_0     = time.time()
	container.WriteSCells(cells)
	time_1     = time.time()
	time_delta = time_1 - time_0
	print(f"{count:6d} ячеек перезаписано за {time_delta:0.5f} сек = {(time_delta / count):0.10f} сек на операцию")

@pytest.mark.perfomance
def test_pkg_s_cells_write_rewrite(benchmark, cells):
	benchmark(pkg_s_cells_write_rewrite, cells)


def pkg_s_cells_sync(cells):
	print(f"Синхронизация {count} S-Ячеек")
	time_0     = time.time()
	container.SyncSCells(cells)
	time_1     = time.time()
	time_delta = time_1 - time_0
	print(f"{count:6d} ячеек синхронизировано за {time_delta:0.5f} сек = {(time_delta / count):0.10f} сек на операцию")

@pytest.mark.perfomance
def test_pkg_s_cells_sync(benchmark, cells):
	benchmark(pkg_s_cells_sync, cells)