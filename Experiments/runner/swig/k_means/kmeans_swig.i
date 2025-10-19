/* kmeans_swig.i */
%module kmeans_swig

%{
#include "kmeans_swig.h"
%}

%include "std_vector.i"

namespace std {
    %template(DoubleVector) vector<double>;
    %template(DataSet) vector<vector<double>>;
}

%include "kmeans_swig.h"