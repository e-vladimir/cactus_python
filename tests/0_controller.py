# ТЕСТ КОНТРОЛЛЕРА КОНТЕЙНЕРОВ
# 24 окт 2024

from G00_status_codes                 import CODES_COMPLETION
from G30_cactus_controller_containers import ControllerContainers

print("")
print("[== Тест контроллера контейнеров ==]")

result = ControllerContainers.ContainerNames()
check  = (result.code == CODES_COMPLETION.COMPLETED) and (result.data == [])
print(f"{'[+]' if check else '[ ]'} Инициализация контроллера")
if not check: print(f"                  {result.code} {result.subcodes}\n")

ControllerContainers.RegisterContainerRAM("RAM")
result = ControllerContainers.ContainerNames()
check  = (result.code == CODES_COMPLETION.COMPLETED) and (result.data == ["RAM"])
print(f"{'[+]' if check else '[ ]'} Регистрация контейнера RAM")
if not check: print(f"                  {result.code} {result.subcodes}\n")

check = ControllerContainers.Container("RAM") is not None
print(f"{'[+]' if check else '[ ]'} Получение контейнера RAM")
if not check: print(f"                  {result.code} {result.subcodes}\n")

result = ControllerContainers.UnregisterContainer("RAM")
check  = result.code == CODES_COMPLETION.COMPLETED
result = ControllerContainers.ContainerNames()
check  = check and (result.code == CODES_COMPLETION.COMPLETED) and (result.data == [])
print(f"{'[+]' if check else '[ ]'} Отмена регистрации контейнера RAM")
if not check: print(f"                  {result.code} {result.subcodes}\n")
