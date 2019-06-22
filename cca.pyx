from cpython cimport array
import array
import numpy as np
cimport numpy as np

"""
I think ill need the boudnary checks off for speed.
#cython: boundscheck=False, wraparound=False, nonecheck=False
"""


cdef int next_val(int n, int max_val):
    if n < max_val:
        return n + 1
    else:
        return 0

cdef int next_state(long[:, :] arr, int x, int y, 
                     int h, int w, int max_val):
    """
    Return True if there is a value higher than the current 
    value in the Moore neighbourhood.

    arr: Numpy array with game state
    x: column index
    y: row index
    h: number of columns in arr
    w: number of rows in arr 
    """
    cdef int val = arr[x, y]
    cdef int top = max(x - 1, 0)
    cdef int bottom = min(x + 2, h)
    cdef int left = max(y - 1, 0)
    cdef int right = min(y + 2, w)

    for row in range(top, bottom):
        for col in range(left, right):
            successor = next_val(val, max_val)
            if arr[row, col] == successor:
                return successor
    return val
    
cpdef next_phase(arr, max_val):
    h, w = arr.shape[1], arr.shape[0]
    A = np.empty((w, h))
    for i in range(w):
        for j in range(h):
            A[i, j] = next_state(arr, i, j, w, h, max_val)
    return A







    
