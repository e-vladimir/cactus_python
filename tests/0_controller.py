# 08 июл 2024

from G00_status_codes                 import CODES_COMPLETION
from G30_cactus_controller_containers import controller_containers

print("")
print("[== Тест контроллера контейнеров ==]")

result = controller_containers.ContainerNames()
check  = (result.code == CODES_COMPLETION.COMPLETED) and (result.data == [])
print(f"{'[+]' if check else '[ ]'} Инициализация контроллера")

controller_containers.RegisterContainerRAM("RAM")
result = controller_containers.ContainerNames()
check  = (result.code == CODES_COMPLETION.COMPLETED) and (result.data == ["RAM"])
print(f"{'[+]' if check else '[ ]'} Регистрация контейнера RAM")

check = controller_containers.Container("RAM") is not None
print(f"{'[+]' if check else '[ ]'} Получение контейнера RAM")

result = controller_containers.UnregisterContainer("RAM")
check  = result.code == CODES_COMPLETION.COMPLETED
result = controller_containers.ContainerNames()
check  = check and (result.code == CODES_COMPLETION.COMPLETED) and (result.data == [])
print(f"{'[+]' if check else '[ ]'} Отмена регистрации контейнера RAM")
