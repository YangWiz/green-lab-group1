# quicksort_cy.pyx
# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False

cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
cdef int _partition_cy(double* items, int low, int high) nogil:
    """Cython partition function using pointer arithmetic."""
    cdef double pivot = items[high]
    cdef int i = low - 1
    cdef int j
    cdef double temp
    
    for j in range(low, high):
        if items[j] <= pivot:
            i += 1
            # Swap items[i] and items[j]
            temp = items[i]
            items[i] = items[j]
            items[j] = temp
    
    # Swap items[i + 1] and items[high] (pivot)
    temp = items[i + 1]
    items[i + 1] = items[high]
    items[high] = temp
    
    return i + 1


@cython.boundscheck(False)
@cython.wraparound(False)
cdef void _quicksort_recursive_cy(double* items, int low, int high) nogil:
    """Cython recursive quicksort implementation."""
    cdef int pi
    
    if low < high:
        pi = _partition_cy(items, low, high)
        _quicksort_recursive_cy(items, low, pi - 1)
        _quicksort_recursive_cy(items, pi + 1, high)


def quicksort_cy(list arr):
    """
    Cython-optimized in-place Quicksort implementation.
    Returns a new sorted list.
    """
    cdef int n = len(arr)
    cdef int i
    cdef double* items
    cdef list arr_copy
    
    if n == 0:
        return []
    
    # Create a copy
    arr_copy = arr[:]
    
    # Allocate C array
    items = <double*>malloc(n * sizeof(double))
    if items == NULL:
        raise MemoryError("Failed to allocate memory")
    
    try:
        # Copy data to C array
        for i in range(n):
            items[i] = arr_copy[i]
        
        # Sort the C array (release GIL for better performance)
        with nogil:
            _quicksort_recursive_cy(items, 0, n - 1)
        
        # Copy back to Python list
        for i in range(n):
            arr_copy[i] = items[i]
        
        return arr_copy
    
    finally:
        free(items)


# Import malloc and free
from libc.stdlib cimport malloc, free