# bfs_cy.pyx
# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False

cimport cython
from libc.stdlib cimport malloc, free, realloc
from libc.string cimport memset
import random

# --- Graph Initialization (Cython optimized) ---

def create_sparse_graph_cy(int V, int E, bint directed=False):
    """
    Cython-optimized random sparse graph generation using adjacency list.
    
    Args:
        V (int): Number of vertices (nodes).
        E (int): Number of edges.
        directed (bool): If True, graph is directed.
    
    Returns:
        dict: Adjacency list representation {node: [neighbors]}
    """
    cdef int max_edges, u, v
    cdef tuple edge
    
    if V <= 0:
        return {}
    
    max_edges = V * (V - 1) // 2
    if E > max_edges:
        E = max_edges
    
    # Python dict for adjacency list (for compatibility with main code)
    adj = {i: [] for i in range(V)}
    
    # Generate unique edges
    cdef set edges = set()
    
    while len(edges) < E:
        u = random.randrange(V)
        v = random.randrange(V)
        if u == v:
            continue
        
        # Canonical order
        if u > v:
            u, v = v, u
        edge = (u, v)
        edges.add(edge)
    
    # Populate adjacency list
    for u, v in edges:
        adj[u].append(v)
        if not directed:
            adj[v].append(u)
    
    return adj


# --- BFS Implementation (Highly Optimized) ---

@cython.boundscheck(False)
@cython.wraparound(False)
def breadth_first_search_cy(dict graph, int start_node):
    """
    Cython-optimized BFS implementation.
    Complexity is O(V + E), where V is vertices and E is edges.
    
    Returns:
        tuple: (visited_count, path_info)
    """
    # Declare all C variables at the start
    cdef int V, queue_size, queue_head, queue_tail
    cdef int* queue
    cdef unsigned char* visited_array
    cdef int u, v, visited_count
    cdef list neighbors
    
    if start_node not in graph:
        return 0, {}
    
    V = len(graph)
    queue_size = V
    queue_head = 0
    queue_tail = 0
    
    # Allocate queue for BFS
    queue = <int*>malloc(queue_size * sizeof(int))
    if queue == NULL:
        raise MemoryError("Failed to allocate queue")
    
    visited_array = <unsigned char*>malloc(V * sizeof(unsigned char))
    if visited_array == NULL:
        free(queue)
        raise MemoryError("Failed to allocate visited array")
    
    try:
        # Initialize visited array
        memset(visited_array, 0, V * sizeof(unsigned char))
        
        # Mark start node as visited and enqueue
        visited_array[start_node] = 1
        queue[queue_tail] = start_node
        queue_tail += 1
        
        # Path dictionary for result
        path = {start_node: None}
        visited_count = 1
        
        # BFS main loop
        while queue_head < queue_tail:
            u = queue[queue_head]
            queue_head += 1
            
            # Get neighbors
            neighbors = graph.get(u, [])
            
            for v in neighbors:
                if visited_array[v] == 0:
                    visited_array[v] = 1
                    visited_count += 1
                    path[v] = u
                    queue[queue_tail] = v
                    queue_tail += 1
        
        return visited_count, path
    
    finally:
        free(queue)
        free(visited_array)


# --- Alternative: BFS with C++ style vector simulation ---

@cython.boundscheck(False)
@cython.wraparound(False)
def breadth_first_search_cy_v2(dict graph, int start_node):
    """
    Alternative Cython BFS using dynamic arrays.
    Slightly different memory management strategy.
    
    Returns:
        tuple: (visited_count, path_info)
    """
    # Declare all C variables at the start
    cdef int queue_idx, u, v
    cdef list neighbors
    cdef set visited
    cdef list queue
    cdef dict path
    
    if start_node not in graph:
        return 0, {}
    
    # Use Python set for visited (hybrid approach)
    visited = {start_node}
    queue = [start_node]
    path = {start_node: None}
    queue_idx = 0
    
    while queue_idx < len(queue):
        u = queue[queue_idx]
        queue_idx += 1
        
        neighbors = graph.get(u, [])
        
        for v in neighbors:
            if v not in visited:
                visited.add(v)
                path[v] = u
                queue.append(v)
    
    return len(visited), path


# --- Fast BFS for dense graphs (adjacency matrix representation) ---

@cython.boundscheck(False)
@cython.wraparound(False)
def breadth_first_search_matrix_cy(unsigned char[:, :] adj_matrix, int start_node):
    """
    Cython BFS optimized for adjacency matrix representation.
    Best for dense graphs.
    
    Args:
        adj_matrix: 2D numpy array (uint8) where adj_matrix[i][j] = 1 if edge exists
        start_node: Starting vertex
    
    Returns:
        tuple: (visited_count, path_dict)
    """
    # Declare all C variables at the start
    cdef int V, queue_head, queue_tail, u, v, visited_count
    cdef int* queue
    cdef unsigned char* visited
    cdef dict path
    
    V = adj_matrix.shape[0]
    
    if start_node < 0 or start_node >= V:
        return 0, {}
    
    queue = <int*>malloc(V * sizeof(int))
    visited = <unsigned char*>malloc(V * sizeof(unsigned char))
    
    if queue == NULL or visited == NULL:
        if queue != NULL:
            free(queue)
        if visited != NULL:
            free(visited)
        raise MemoryError("Failed to allocate memory")
    
    try:
        memset(visited, 0, V * sizeof(unsigned char))
        
        queue_head = 0
        queue_tail = 0
        visited_count = 1
        path = {start_node: None}
        
        visited[start_node] = 1
        queue[queue_tail] = start_node
        queue_tail += 1
        
        while queue_head < queue_tail:
            u = queue[queue_head]
            queue_head += 1
            
            # Check all possible neighbors
            for v in range(V):
                if adj_matrix[u, v] == 1 and visited[v] == 0:
                    visited[v] = 1
                    visited_count += 1
                    path[v] = u
                    queue[queue_tail] = v
                    queue_tail += 1
        
        return visited_count, path
    
    finally:
        free(queue)
        free(visited)