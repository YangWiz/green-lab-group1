/* fft_swig.i */
%module fft_swig

%{
#include "fft_swig.h"
%}

%include "std_vector.i"
%include "std_complex.i"

namespace std {
    %template(Complex) complex<double>;
    %template(ComplexVector) vector<complex<double>>;
}

%include "fft_swig.h"