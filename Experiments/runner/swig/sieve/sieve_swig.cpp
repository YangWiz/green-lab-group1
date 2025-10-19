// sieve_swig.cpp
#include "sieve_swig.h"
#include <cstring>

std::vector<int> sieve_of_eratosthenes(int limit) {
    std::vector<int> primes;
    
    if (limit < 2) {
        return primes;
    }
    
    // Create boolean array
    bool* is_prime = new bool[limit + 1];
    std::memset(is_prime, true, (limit + 1) * sizeof(bool));
    is_prime[0] = is_prime[1] = false;
    
    int p = 2;
    while (p * p <= limit) {
        if (is_prime[p]) {
            // Mark all multiples of p
            for (int i = p * p; i <= limit; i += p) {
                is_prime[i] = false;
            }
        }
        p++;
    }
    
    // Collect all primes
    for (int i = 2; i <= limit; i++) {
        if (is_prime[i]) {
            primes.push_back(i);
        }
    }
    
    delete[] is_prime;
    return primes;
}