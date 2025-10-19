# conv_cy.pyx
# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True

cimport cython
from libc.stdlib cimport malloc, free
import numpy as np
cimport numpy as cnp

cnp.import_array()

@cython.boundscheck(False)
@cython.wraparound(False)
def convolution_1d_cy(list data, list kernel):
    """
    Cython-optimized 1D convolution with 'same' padding.
    Complexity is O(N * K), where N is data length and K is kernel size.
    """
    cdef int data_len = len(data)
    cdef int kernel_len = len(kernel)
    cdef int pad_len = kernel_len // 2
    cdef int padded_len = data_len + 2 * pad_len
    cdef int i, k
    cdef double sum_val
    cdef double* padded_data
    cdef double* kernel_arr
    cdef list output = [0.0] * data_len
    
    # Allocate C arrays
    padded_data = <double*>malloc(padded_len * sizeof(double))
    kernel_arr = <double*>malloc(kernel_len * sizeof(double))
    
    if padded_data == NULL or kernel_arr == NULL:
        if padded_data != NULL:
            free(padded_data)
        if kernel_arr != NULL:
            free(kernel_arr)
        raise MemoryError("Failed to allocate memory")
    
    try:
        # Initialize padded data with zeros
        for i in range(pad_len):
            padded_data[i] = 0.0
        for i in range(data_len):
            padded_data[pad_len + i] = data[i]
        for i in range(pad_len):
            padded_data[pad_len + data_len + i] = 0.0
        
        # Copy kernel to C array
        for k in range(kernel_len):
            kernel_arr[k] = kernel[k]
        
        # Perform 1D convolution
        for i in range(data_len):
            sum_val = 0.0
            for k in range(kernel_len):
                sum_val += padded_data[i + k] * kernel_arr[k]
            output[i] = sum_val
        
        return output
    
    finally:
        free(padded_data)
        free(kernel_arr)


@cython.boundscheck(False)
@cython.wraparound(False)
def convolution_2d_cy(list image, list kernel):
    """
    Cython-optimized 2D convolution with 'same' padding.
    Complexity is O(R * C * K^2), where R and C are image dimensions and K is kernel size.
    """
    cdef int rows = len(image)
    cdef int cols, k_size, pad, padded_rows, padded_cols
    cdef int r, c, kr, kc, ir, ic
    cdef double sum_val
    cdef double** padded_image
    cdef double** kernel_arr
    cdef double** output
    cdef int i
    
    if rows == 0:
        return []
    
    cols = len(image[0])
    k_size = len(kernel)
    pad = k_size // 2
    padded_rows = rows + 2 * pad
    padded_cols = cols + 2 * pad
    
    # Allocate 2D arrays
    padded_image = <double**>malloc(padded_rows * sizeof(double*))
    kernel_arr = <double**>malloc(k_size * sizeof(double*))
    output = <double**>malloc(rows * sizeof(double*))
    
    if padded_image == NULL or kernel_arr == NULL or output == NULL:
        if padded_image != NULL:
            free(padded_image)
        if kernel_arr != NULL:
            free(kernel_arr)
        if output != NULL:
            free(output)
        raise MemoryError("Failed to allocate memory")
    
    try:
        # Allocate rows for padded_image
        for i in range(padded_rows):
            padded_image[i] = <double*>malloc(padded_cols * sizeof(double))
            if padded_image[i] == NULL:
                raise MemoryError("Failed to allocate memory")
        
        # Allocate rows for kernel
        for i in range(k_size):
            kernel_arr[i] = <double*>malloc(k_size * sizeof(double))
            if kernel_arr[i] == NULL:
                raise MemoryError("Failed to allocate memory")
        
        # Allocate rows for output
        for i in range(rows):
            output[i] = <double*>malloc(cols * sizeof(double))
            if output[i] == NULL:
                raise MemoryError("Failed to allocate memory")
        
        # Initialize padded_image with zeros and copy image data
        for r in range(padded_rows):
            for c in range(padded_cols):
                padded_image[r][c] = 0.0
        
        for r in range(rows):
            for c in range(cols):
                padded_image[r + pad][c + pad] = image[r][c]
        
        # Copy kernel to C array
        for kr in range(k_size):
            for kc in range(k_size):
                kernel_arr[kr][kc] = kernel[kr][kc]
        
        # Perform 2D convolution
        for r in range(rows):
            for c in range(cols):
                sum_val = 0.0
                for kr in range(k_size):
                    for kc in range(k_size):
                        ir = r + kr
                        ic = c + kc
                        sum_val += padded_image[ir][ic] * kernel_arr[kr][kc]
                output[r][c] = sum_val
        
        # Convert output to Python list
        result = [[output[r][c] for c in range(cols)] for r in range(rows)]
        
        return result
    
    finally:
        # Free all allocated memory
        if padded_image != NULL:
            for i in range(padded_rows):
                if padded_image[i] != NULL:
                    free(padded_image[i])
            free(padded_image)
        
        if kernel_arr != NULL:
            for i in range(k_size):
                if kernel_arr[i] != NULL:
                    free(kernel_arr[i])
            free(kernel_arr)
        
        if output != NULL:
            for i in range(rows):
                if output[i] != NULL:
                    free(output[i])
            free(output)