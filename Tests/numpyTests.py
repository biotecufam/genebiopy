import numpy as np

'''
size = 0.2
vals = np.array([[200, 32, 60], [37, 40, 30], [29, 10, 87], [29, 10, 24], [10, 20, 10]])

print(np.arange(4)*4)
print(np.array([1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15]))

print(vals.sum(axis=0))
print(vals.flatten())
'''
array = "abcdefghij"
start = 1
stop = 10

if stop < start:
    print (array[start-1:stop-1:-1] + array[stop-1])
else:
    print (array[start-1:stop])
