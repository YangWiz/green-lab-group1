// bfs_swig.cpp
#include "bfs_swig.h"
#include <queue>
#include <set>
#include <cstdlib>
#include <ctime>
#include <algorithm>

BFSResult breadth_first_search(const Graph& graph, int start_node) {
    std::map<int, int> path;
    
    if (graph.find(start_node) == graph.end()) {
        return BFSResult(0, path);
    }
    
    std::queue<int> queue;
    std::set<int> visited;
    
    queue.push(start_node);
    visited.insert(start_node);
    path[start_node] = -1; // No parent for start node
    
    while (!queue.empty()) {
        int u = queue.front();
        queue.pop();
        
        auto it = graph.find(u);
        if (it != graph.end()) {
            for (int v : it->second) {
                if (visited.find(v) == visited.end()) {
                    visited.insert(v);
                    path[v] = u;
                    queue.push(v);
                }
            }
        }
    }
    
    return BFSResult(visited.size(), path);
}

Graph create_sparse_graph(int V, int E, bool directed) {
    Graph adj;
    
    if (V <= 0) {
        return adj;
    }
    
    // Initialize adjacency list
    for (int i = 0; i < V; i++) {
        adj[i] = std::vector<int>();
    }
    
    int max_edges = V * (V - 1) / 2;
    if (E > max_edges) {
        E = max_edges;
    }
    
    std::set<std::pair<int, int>> edges;
    
    // Seed random number generator
    static bool seeded = false;
    if (!seeded) {
        std::srand(std::time(nullptr));
        seeded = true;
    }
    
    while ((int)edges.size() < E) {
        int u = std::rand() % V;
        int v = std::rand() % V;
        
        if (u == v) continue;
        
        // Canonical order
        if (u > v) std::swap(u, v);
        
        edges.insert(std::make_pair(u, v));
    }
    
    // Populate adjacency list
    for (const auto& edge : edges) {
        adj[edge.first].push_back(edge.second);
        if (!directed) {
            adj[edge.second].push_back(edge.first);
        }
    }
    
    return adj;
}