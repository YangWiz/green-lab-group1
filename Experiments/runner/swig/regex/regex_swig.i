/* regex_swig.i */
%module regex_swig

%{
#include "regex_swig.h"
%}

%include "std_string.i"
%include "std_vector.i"

namespace std {
    %template(StringVector) vector<string>;
}

%include "regex_swig.h"