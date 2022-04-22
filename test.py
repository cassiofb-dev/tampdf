import time
from tampdf.datasets.happy_a import HappyA


t0 = time.perf_counter()

for index in range(5): 
  print(index)
  happy_a = HappyA()

t1 = time.perf_counter()

print(t1 - t0)