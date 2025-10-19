# fft_cy.pyx
# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True

cimport cython
from libc.math cimport sin, cos, M_PI
import numpy as np
cimport numpy as cnp

cnp.import_array()

@cython.boundscheck(False)
@cython.wraparound(False)
def dft_naive_cy(cnp.ndarray[cnp.complex128_t, ndim=1] x):
    """
    Cython-optimized Naive Discrete Fourier Transform (O(N^2)).
    Input: x — 1D complex array.
    Output: complex DFT result.
    """
    cdef int N = x.shape[0]
    cdef int k, n
    cdef double angle, real_part, imag_part
    cdef double complex s
    cdef double x_real, x_imag
    cdef cnp.ndarray[cnp.complex128_t, ndim=1] X = np.zeros(N, dtype=np.complex128)
    cdef double two_pi = 2.0 * M_PI
    
    for k in range(N):
        s = 0.0 + 0.0j
        for n in range(N):
            angle = -two_pi * k * n / N
            # Manually compute exp(i*angle) = cos(angle) + i*sin(angle)
            real_part = cos(angle)
            imag_part = sin(angle)
            
            # Get real and imaginary parts of x[n]
            x_real = x[n].real
            x_imag = x[n].imag
            
            # Complex multiplication: (x_real + i*x_imag) * (real_part + i*imag_part)
            s += (x_real * real_part - x_imag * imag_part) + 1j * (x_real * imag_part + x_imag * real_part)
        
        X[k] = s
    
    return X


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def fft_cooley_tukey_cy(cnp.ndarray[cnp.complex128_t, ndim=1] x):
    """
    Cython-optimized Cooley-Tukey FFT algorithm (O(N log N)).
    Recursive implementation.
    Input: x — 1D complex array (length must be power of 2).
    Output: complex FFT result.
    """
    cdef int N = x.shape[0]
    
    # Base case
    if N <= 1:
        return x
    
    # Check if N is power of 2
    if N & (N - 1) != 0:
        raise ValueError("Input size must be a power of 2")
    
    # Divide
    cdef cnp.ndarray[cnp.complex128_t, ndim=1] even = fft_cooley_tukey_cy(x[0::2])
    cdef cnp.ndarray[cnp.complex128_t, ndim=1] odd = fft_cooley_tukey_cy(x[1::2])
    
    # Conquer
    cdef cnp.ndarray[cnp.complex128_t, ndim=1] T = np.zeros(N // 2, dtype=np.complex128)
    cdef int k
    cdef double angle
    cdef double complex w
    
    for k in range(N // 2):
        angle = -2.0 * M_PI * k / N
        w = cos(angle) + 1j * sin(angle)
        T[k] = w * odd[k]
    
    # Combine
    cdef cnp.ndarray[cnp.complex128_t, ndim=1] X = np.zeros(N, dtype=np.complex128)
    for k in range(N // 2):
        X[k] = even[k] + T[k]
        X[k + N // 2] = even[k] - T[k]
    
    return X


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def fft_iterative_cy(cnp.ndarray[cnp.complex128_t, ndim=1] x):
    """
    Cython-optimized iterative Cooley-Tukey FFT (O(N log N)).
    Non-recursive, more efficient implementation.
    Input: x — 1D complex array (length must be power of 2).
    Output: complex FFT result.
    """
    cdef int N = x.shape[0]
    
    if N & (N - 1) != 0:
        raise ValueError("Input size must be a power of 2")
    
    # Bit-reversal permutation
    cdef cnp.ndarray[cnp.complex128_t, ndim=1] X = np.array(x, dtype=np.complex128)
    cdef int i, j, k, n, m
    cdef double complex temp, w, wm
    cdef double angle
    
    # Bit reversal
    j = 0
    for i in range(N - 1):
        if i < j:
            temp = X[i]
            X[i] = X[j]
            X[j] = temp
        
        k = N >> 1
        while k <= j:
            j -= k
            k >>= 1
        j += k
    
    # Iterative FFT
    cdef int size = 2
    cdef int half, idx
    
    while size <= N:
        half = size >> 1
        angle = -2.0 * M_PI / size
        wm = cos(angle) + 1j * sin(angle)
        
        for i in range(0, N, size):
            w = 1.0 + 0.0j
            for j in range(half):
                idx = i + j
                temp = w * X[idx + half]
                X[idx + half] = X[idx] - temp
                X[idx] = X[idx] + temp
                w *= wm
        
        size <<= 1
    
    return X