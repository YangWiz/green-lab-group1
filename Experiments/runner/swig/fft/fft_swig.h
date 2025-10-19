// fft_swig.h
#ifndef FFT_SWIG_H
#define FFT_SWIG_H

#include <vector>
#include <complex>

// Type definitions
typedef std::complex<double> Complex;
typedef std::vector<Complex> ComplexVector;

// Naive O(N^2) Discrete Fourier Transform
ComplexVector dft_naive(const ComplexVector& x);

// Cooley-Tukey FFT algorithm (recursive, O(N log N))
ComplexVector fft_cooley_tukey(const ComplexVector& x);

// Iterative FFT (in-place, O(N log N))
ComplexVector fft_iterative(const ComplexVector& x);

#endif // FFT_SWIG_H