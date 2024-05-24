# КАКТУС: ГЕНЕРАТОРЫ
# 2022-10-31

import random
import time

STEP_ID : int = 6


# ГЕНЕРАТОРЫ ID
def GenerateID() -> str:
	""" Генерация ID """
	utime      : float = time.time()
	identifier : str   = f"{int(utime * 1000000)}{random.randint(10, 1000):04d}{random.randint(10, 1000):04d}"

	return '-'.join(identifier[index:index + STEP_ID] for index in range(0, len(identifier), STEP_ID))
