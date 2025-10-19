# sieve_cy.pyx
# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True

cimport cython
from libc.stdlib cimport malloc, free
from libc.string cimport memset

def sieve_of_eratosthenes(int limit):
    """
    Cython-optimized Sieve of Eratosthenes to find all prime numbers up to 'limit'.
    Returns a list of primes.
    """
    if limit < 2:
        return []
    
    cdef int i, p, multiple
    cdef unsigned char* is_prime
    cdef list primes = []
    
    # Allocate memory for the sieve array
    is_prime = <unsigned char*>malloc((limit + 1) * sizeof(unsigned char))
    if is_prime == NULL:
        raise MemoryError("Failed to allocate memory for sieve")
    
    try:
        # Initialize all values to 1 (True/prime)
        memset(is_prime, 1, limit + 1)
        is_prime[0] = 0
        is_prime[1] = 0
        
        p = 2
        # Sieve algorithm
        while p * p <= limit:
            if is_prime[p]:
                # Mark all multiples of p starting from p*p
                multiple = p * p
                while multiple <= limit:
                    is_prime[multiple] = 0
                    multiple += p
            p += 1
        
        # Collect all primes
        for i in range(2, limit + 1):
            if is_prime[i]:
                primes.append(i)
        
        return primes
    
    finally:
        # Free allocated memory
        free(is_prime)