// conv_swig.h
#ifndef CONV_SWIG_H
#define CONV_SWIG_H

#include <vector>

// Type definitions
typedef std::vector<double> Vector1D;
typedef std::vector<Vector1D> Matrix2D;

// 1D Convolution with 'same' padding
Vector1D convolution_1d(const Vector1D& data, const Vector1D& kernel);

// 2D Convolution with 'same' padding
Matrix2D convolution_2d(const Matrix2D& image, const Matrix2D& kernel);

#endif // CONV_SWIG_H