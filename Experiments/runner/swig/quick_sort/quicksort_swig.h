// quicksort_swig.h
#ifndef QUICKSORT_SWIG_H
#define QUICKSORT_SWIG_H

#include <vector>

// Quicksort implementation that returns a sorted copy
std::vector<double> quicksort(const std::vector<double>& arr);

// In-place quicksort (modifies the input vector)
void quicksort_inplace(std::vector<double>& arr);

#endif // QUICKSORT_SWIG_H