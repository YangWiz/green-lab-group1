/* conv_swig.i */
%module conv_swig

%{
#include "conv_swig.h"
%}

%include "std_vector.i"

namespace std {
    %template(DoubleVector) vector<double>;
    %template(Matrix2D) vector<vector<double>>;
}

%include "conv_swig.h"