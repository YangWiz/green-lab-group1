// matmul_swig.cpp
#include "matmul_swig.h"
#include <algorithm>

Matrix2D matmul_naive(const Matrix2D& A, const Matrix2D& B) {
    if (A.empty() || B.empty()) {
        return Matrix2D();
    }
    
    int n = A.size();
    Matrix2D C(n, Vector1D(n, 0.0));
    
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            double sum = 0.0;
            for (int k = 0; k < n; k++) {
                sum += A[i][k] * B[k][j];
            }
            C[i][j] = sum;
        }
    }
    
    return C;
}

Matrix2D matmul_blocked(const Matrix2D& A, const Matrix2D& B, int block_size) {
    if (A.empty() || B.empty()) {
        return Matrix2D();
    }
    
    int n = A.size();
    Matrix2D C(n, Vector1D(n, 0.0));
    
    for (int ii = 0; ii < n; ii += block_size) {
        for (int jj = 0; jj < n; jj += block_size) {
            for (int kk = 0; kk < n; kk += block_size) {
                int i_max = std::min(ii + block_size, n);
                int j_max = std::min(jj + block_size, n);
                int k_max = std::min(kk + block_size, n);
                
                // Process the block
                for (int i = ii; i < i_max; i++) {
                    for (int j = jj; j < j_max; j++) {
                        double sum = C[i][j];
                        for (int k = kk; k < k_max; k++) {
                            sum += A[i][k] * B[k][j];
                        }
                        C[i][j] = sum;
                    }
                }
            }
        }
    }
    
    return C;
}

Matrix2D matmul_transpose(const Matrix2D& A, const Matrix2D& B) {
    if (A.empty() || B.empty()) {
        return Matrix2D();
    }
    
    int n = A.size();
    Matrix2D C(n, Vector1D(n, 0.0));
    
    // Transpose B for better cache locality
    Matrix2D B_T(n, Vector1D(n, 0.0));
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            B_T[j][i] = B[i][j];
        }
    }
    
    // Multiply A with transposed B
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            double sum = 0.0;
            for (int k = 0; k < n; k++) {
                sum += A[i][k] * B_T[j][k];
            }
            C[i][j] = sum;
        }
    }
    
    return C;
}