/* sieve_swig.i */
%module sieve_swig

%{
#include "sieve_swig.h"
%}

%include "std_vector.i"

namespace std {
    %template(IntVector) vector<int>;
}

%include "sieve_swig.h"