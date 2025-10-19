// quicksort_swig.cpp
#include "quicksort_swig.h"

// Partition function for quicksort
static int partition(std::vector<double>& items, int low, int high) {
    double pivot = items[high];
    int i = low - 1;
    
    for (int j = low; j < high; j++) {
        if (items[j] <= pivot) {
            i++;
            // Swap items[i] and items[j]
            double temp = items[i];
            items[i] = items[j];
            items[j] = temp;
        }
    }
    
    // Swap items[i + 1] and items[high] (pivot)
    double temp = items[i + 1];
    items[i + 1] = items[high];
    items[high] = temp;
    
    return i + 1;
}

// Recursive quicksort helper
static void quicksort_recursive(std::vector<double>& items, int low, int high) {
    if (low < high) {
        int pi = partition(items, low, high);
        
        // Recursively sort elements before and after partition
        quicksort_recursive(items, low, pi - 1);
        quicksort_recursive(items, pi + 1, high);
    }
}

std::vector<double> quicksort(const std::vector<double>& arr) {
    // Create a copy
    std::vector<double> arr_copy = arr;
    
    if (!arr_copy.empty()) {
        quicksort_recursive(arr_copy, 0, arr_copy.size() - 1);
    }
    
    return arr_copy;
}

void quicksort_inplace(std::vector<double>& arr) {
    if (!arr.empty()) {
        quicksort_recursive(arr, 0, arr.size() - 1);
    }
}