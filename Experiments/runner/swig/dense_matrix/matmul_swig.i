/* matmul_swig.i */
%module matmul_swig

%{
#include "matmul_swig.h"
%}

%include "std_vector.i"

namespace std {
    %template(DoubleVector) vector<double>;
    %template(Matrix2D) vector<vector<double>>;
}

%include "matmul_swig.h"