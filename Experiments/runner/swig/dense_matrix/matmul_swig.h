// matmul_swig.h
#ifndef MATMUL_SWIG_H
#define MATMUL_SWIG_H

#include <vector>

// Type definitions
typedef std::vector<double> Vector1D;
typedef std::vector<Vector1D> Matrix2D;

// Naive O(N^3) triple loop matrix multiplication
Matrix2D matmul_naive(const Matrix2D& A, const Matrix2D& B);

// Blocked/tiled matrix multiplication for better cache reuse
Matrix2D matmul_blocked(const Matrix2D& A, const Matrix2D& B, int block_size = 64);

// Optimized matrix multiplication with transposed B
Matrix2D matmul_transpose(const Matrix2D& A, const Matrix2D& B);

#endif // MATMUL_SWIG_H