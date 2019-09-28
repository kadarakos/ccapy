from cpython cimport array
import array
import numpy as np
cimport numpy as np

"""
I think ill need the boudnary checks off for speed.
#cython: boundscheck=False, wraparound=False, nonecheck=False
"""

cdef long[:, :] COLORS = np.array([
    [249,208,137],
    [255,156,91],
    [58,128,130],
    [245,99,74],
    [235,47,59],
])

cdef int next_val(int n, int max_val):
    if n < max_val:
        return n + 1
    else:
        return 0


cdef int next_state_moore(long[:, :] arr, int x, int y, 
                          int h, int w, int max_val, 
                          int threshold, int rang):
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
    cdef int top = max(x - rang, 0)
    cdef int bottom = min(x + rang + 1, h)
    cdef int left = max(y - rang, 0)
    cdef int right = min(y + rang + 1, w)
    cdef int n_succesor = 0
    cdef int row, col

    for row in range(top, bottom):
        for col in range(left, right):
            successor = next_val(val, max_val)
            if arr[row, col] == successor:
                n_succesor += 1
            if n_succesor == threshold:
                return successor
    return val
    
cdef int next_state_neumann(long[:, :] arr, int x, int y, 
                          int h, int w, int max_val, 
                          int threshold, int rang):
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
    cdef int top = max(x - rang, 0)
    cdef int bottom = min(x + rang + 1, h)
    cdef int left = max(y - rang, 0)
    cdef int right = min(y + rang + 1, w)
    cdef int n_succesor = 0
    cdef int row, col

    for row in range(top, bottom):
        for col in range(left, right):
            if (abs(x - row) + abs(y - col)) > rang:
                continue
            successor = next_val(val, max_val)
            if arr[row, col] == successor:
                n_succesor += 1
            if n_succesor == threshold:
                return successor
    return val

cpdef next_phase(long[:, :] arr, int max_val, int threshold, int rang, str hood):
    h, w = arr.shape[0], arr.shape[1]
    cdef long[:, :] A = np.empty((h, w), dtype=int)
    cdef long[:, :, :] B = np.empty((h, w, 3), dtype=int)

    for i in range(h):
        for j in range(w):
            if hood == 'moore':
                s = next_state_moore(arr, i, j, h, w, max_val, threshold, rang)
                A[i, j] = s
                B[i, j, :] = COLORS[s]
            else:
                s = next_state_neumann(arr, i, j, h, w, max_val, threshold, rang)
                A[i, j] = s
                B[i, j, :] = COLORS[s]    
    return A, B
