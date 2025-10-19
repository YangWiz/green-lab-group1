// conv_swig.cpp
#include "conv_swig.h"

Vector1D convolution_1d(const Vector1D& data, const Vector1D& kernel) {
    int data_len = data.size();
    int kernel_len = kernel.size();
    
    Vector1D output(data_len, 0.0);
    
    if (data_len == 0 || kernel_len == 0) {
        return output;
    }
    
    // Determine padding length for 'same' output
    int pad_len = kernel_len / 2;
    
    // Create padded data
    Vector1D padded_data(data_len + 2 * pad_len, 0.0);
    
    // Copy original data to padded array
    for (int i = 0; i < data_len; i++) {
        padded_data[pad_len + i] = data[i];
    }
    
    // Perform 1D convolution
    for (int i = 0; i < data_len; i++) {
        double sum_val = 0.0;
        
        // Iterate over the kernel
        for (int k = 0; k < kernel_len; k++) {
            sum_val += padded_data[i + k] * kernel[k];
        }
        
        output[i] = sum_val;
    }
    
    return output;
}

Matrix2D convolution_2d(const Matrix2D& image, const Matrix2D& kernel) {
    int rows = image.size();
    
    if (rows == 0) {
        return Matrix2D();
    }
    
    int cols = image[0].size();
    int k_size = kernel.size();
    
    if (k_size == 0) {
        return Matrix2D(rows, Vector1D(cols, 0.0));
    }
    
    int pad = k_size / 2;
    
    // Initialize output image
    Matrix2D output(rows, Vector1D(cols, 0.0));
    
    // Create padded image
    int padded_rows = rows + 2 * pad;
    int padded_cols = cols + 2 * pad;
    Matrix2D padded_image(padded_rows, Vector1D(padded_cols, 0.0));
    
    // Copy original image to padded image
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            padded_image[i + pad][j + pad] = image[i][j];
        }
    }
    
    // Perform 2D convolution
    for (int r = 0; r < rows; r++) {
        for (int c = 0; c < cols; c++) {
            double sum_val = 0.0;
            
            // Iterate over the kernel
            for (int kr = 0; kr < k_size; kr++) {
                for (int kc = 0; kc < k_size; kc++) {
                    // Coordinates in the padded image
                    int ir = r + kr;
                    int ic = c + kc;
                    
                    // Apply kernel
                    sum_val += padded_image[ir][ic] * kernel[kr][kc];
                }
            }
            
            output[r][c] = sum_val;
        }
    }
    
    return output;
}