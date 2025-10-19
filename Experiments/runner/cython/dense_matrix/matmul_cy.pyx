# matmul_cy.pyx
# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True

cimport cython
import numpy as np
cimport numpy as cnp

cnp.import_array()

@cython.boundscheck(False)
@cython.wraparound(False)
def matmul_naive_cy(double[:, :] A, double[:, :] B):
    """Cython-optimized naive O(N^3) triple loop matrix multiplication."""
    cdef int n = A.shape[0]
    cdef int i, j, k
    cdef double s
    cdef cnp.ndarray[cnp.float64_t, ndim=2] C = np.zeros((n, n), dtype=np.float64)
    cdef double[:, :] C_view = C
    
    for i in range(n):
        for j in range(n):
            s = 0.0
            for k in range(n):
                s += A[i, k] * B[k, j]
            C_view[i, j] = s
    
    return C


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def matmul_blocked_cy(double[:, :] A, double[:, :] B, int block_size=64):
    """Cython-optimized blocked/tiled matrix multiplication for better cache reuse."""
    cdef int n = A.shape[0]
    cdef int ii, jj, kk, i, j, k
    cdef int i_max, j_max, k_max
    cdef double s
    cdef cnp.ndarray[cnp.float64_t, ndim=2] C = np.zeros((n, n), dtype=np.float64)
    cdef double[:, :] C_view = C
    
    for ii in range(0, n, block_size):
        for jj in range(0, n, block_size):
            for kk in range(0, n, block_size):
                i_max = min(ii + block_size, n)
                j_max = min(jj + block_size, n)
                k_max = min(kk + block_size, n)
                
                # Process the block
                for i in range(ii, i_max):
                    for j in range(jj, j_max):
                        s = C_view[i, j]
                        for k in range(kk, k_max):
                            s += A[i, k] * B[k, j]
                        C_view[i, j] = s
    
    return C


@cython.boundscheck(False)
@cython.wraparound(False)
def matmul_transpose_cy(double[:, :] A, double[:, :] B):
    """
    Cython matrix multiplication with transposed B for better cache locality.
    This improves memory access patterns.
    """
    cdef int n = A.shape[0]
    cdef int i, j, k
    cdef double s
    cdef cnp.ndarray[cnp.float64_t, ndim=2] C = np.zeros((n, n), dtype=np.float64)
    cdef cnp.ndarray[cnp.float64_t, ndim=2] B_T = np.ascontiguousarray(B.T)
    cdef double[:, :] C_view = C
    cdef double[:, :] B_T_view = B_T
    
    for i in range(n):
        for j in range(n):
            s = 0.0
            for k in range(n):
                s += A[i, k] * B_T_view[j, k]
            C_view[i, j] = s
    
    return C