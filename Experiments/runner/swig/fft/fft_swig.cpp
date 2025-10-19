// fft_swig.cpp
#include "fft_swig.h"
#include <cmath>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

ComplexVector dft_naive(const ComplexVector& x) {
    int N = x.size();
    ComplexVector X(N);
    
    for (int k = 0; k < N; k++) {
        Complex s(0.0, 0.0);
        for (int n = 0; n < N; n++) {
            double angle = -2.0 * M_PI * k * n / N;
            Complex w(std::cos(angle), std::sin(angle));
            s += x[n] * w;
        }
        X[k] = s;
    }
    
    return X;
}

ComplexVector fft_cooley_tukey(const ComplexVector& x) {
    int N = x.size();
    
    // Base case
    if (N <= 1) {
        return x;
    }
    
    // Check if N is power of 2
    if (N & (N - 1)) {
        // Not a power of 2, fall back to DFT
        return dft_naive(x);
    }
    
    // Divide
    ComplexVector even, odd;
    even.reserve(N / 2);
    odd.reserve(N / 2);
    
    for (int i = 0; i < N; i += 2) {
        even.push_back(x[i]);
        odd.push_back(x[i + 1]);
    }
    
    // Conquer
    ComplexVector even_fft = fft_cooley_tukey(even);
    ComplexVector odd_fft = fft_cooley_tukey(odd);
    
    // Combine
    ComplexVector X(N);
    for (int k = 0; k < N / 2; k++) {
        double angle = -2.0 * M_PI * k / N;
        Complex w(std::cos(angle), std::sin(angle));
        Complex t = w * odd_fft[k];
        
        X[k] = even_fft[k] + t;
        X[k + N / 2] = even_fft[k] - t;
    }
    
    return X;
}

ComplexVector fft_iterative(const ComplexVector& x) {
    int N = x.size();
    
    // Check if N is power of 2
    if (N & (N - 1)) {
        // Not a power of 2, fall back to DFT
        return dft_naive(x);
    }
    
    // Copy input
    ComplexVector X = x;
    
    // Bit-reversal permutation
    int j = 0;
    for (int i = 0; i < N - 1; i++) {
        if (i < j) {
            std::swap(X[i], X[j]);
        }
        
        int k = N >> 1;
        while (k <= j) {
            j -= k;
            k >>= 1;
        }
        j += k;
    }
    
    // Iterative FFT
    for (int size = 2; size <= N; size <<= 1) {
        int half = size >> 1;
        double angle = -2.0 * M_PI / size;
        Complex wm(std::cos(angle), std::sin(angle));
        
        for (int i = 0; i < N; i += size) {
            Complex w(1.0, 0.0);
            for (int j = 0; j < half; j++) {
                int idx = i + j;
                Complex t = w * X[idx + half];
                X[idx + half] = X[idx] - t;
                X[idx] = X[idx] + t;
                w *= wm;
            }
        }
    }
    
    return X;
}