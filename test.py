import random


array = random.sample(range(1,101),100)

for i in range(len(array) - 1, 0, -1):
    for pivot in range(i):
        compare = pivot + 1
        if array[pivot] > array[compare]:
            array[pivot], array[compare] = array[compare], array[pivot]

