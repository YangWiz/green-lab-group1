/* nbody_swig.i */
%module nbody_swig

%{
#include "nbody_swig.h"
%}

%include "std_vector.i"

// Make Body structure accessible from Python
%include "nbody_swig.h"

namespace std {
    %template(BodiesVector) vector<Body>;
}

// Allow Python to access Body fields
%extend Body {
    %pythoncode %{
        def __repr__(self):
            return f"Body(x={self.x:.2f}, y={self.y:.2f}, vx={self.vx:.2f}, vy={self.vy:.2f}, m={self.m:.2f})"
    %}
}