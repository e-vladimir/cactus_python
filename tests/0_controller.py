# Тест регистрации контейнера

from G30_cactus_controller_containers import controller_containers


print("Тест регистрации контейнеров")
print("")

container_ram_1 = controller_containers.RegisterContainerRAM("RAM")
container_ram_2 = controller_containers.RegisterContainerRAM("RAM")
container_ram_3 = controller_containers.RegisterContainerRAM("RAM-2")
result          = container_ram_1 == container_ram_2
print(f"{'[+]' if result else '[!]'} Создание контейнера RAM с повтором")

names  = controller_containers.ContainerNames()
result = names.data == ["RAM", "RAM-2"]
print(f"{'[+]' if result else '[!]'} Получение списка контейнеров")

controller_containers.UnregisterContainer('RAM')
names  = controller_containers.ContainerNames()
result = names.data == ["RAM-2"]
print(f"{'[+]' if result else '[!]'} Удаление контейнера RAM")
