/* quicksort_swig.i */
%module quicksort_swig

%{
#include "quicksort_swig.h"
%}

%include "std_vector.i"

namespace std {
    %template(DoubleVector) vector<double>;
}

%include "quicksort_swig.h"