import time
from tampdf.datasets.happy_a import HappyA


t0 = time.perf_counter()

for index in range(5): 
  print(index)
  happy_a_dataset = HappyA(
    name="happy_a",
    url="https://raw.githubusercontent.com/COINtoolbox/photoz_catalogues/master/Teddy/forTemplateBased/teddyT_A.cat",
  )

t1 = time.perf_counter()

print(t1 - t0)