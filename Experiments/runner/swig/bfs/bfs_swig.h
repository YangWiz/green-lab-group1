// bfs_swig.h
#ifndef BFS_SWIG_H
#define BFS_SWIG_H

#include <vector>
#include <map>
#include <utility>

// Graph type: adjacency list represented as map<int, vector<int>>
typedef std::map<int, std::vector<int>> Graph;

// Result type: pair of visited count and path map
typedef std::pair<int, std::map<int, int>> BFSResult;

// BFS implementation
BFSResult breadth_first_search(const Graph& graph, int start_node);

// Graph creation helper
Graph create_sparse_graph(int V, int E, bool directed = false);

#endif // BFS_SWIG_H