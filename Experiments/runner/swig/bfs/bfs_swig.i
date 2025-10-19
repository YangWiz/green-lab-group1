/* bfs_swig.i */
%module bfs_swig

%{
#include "bfs_swig.h"
%}

%include "std_vector.i"
%include "std_map.i"
%include "std_pair.i"

namespace std {
    %template(IntVector) vector<int>;
    %template(IntMap) map<int, int>;
    %template(Graph) map<int, vector<int>>;
    %template(BFSResult) pair<int, map<int, int>>;
}

%include "bfs_swig.h"