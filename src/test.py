import numpy as np

arr = np.array([[1,2,3], [4,5,6]])
print(arr)
print()
print(arr.shape)
print()
arr = arr.T
print(arr)
print()
print(arr.shape)
print()

arr = np.array([[[1,2],[3,4],[5,6]], [[7,8],[9,10],[11,12]]])
print(arr)
print()
print(arr.shape)
print()
arr = arr.swapaxes(0,1)
print(arr)
print()
print(arr.shape)
print()