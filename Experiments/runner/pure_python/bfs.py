import time
import random
import collections # Used for the efficient deque in BFS

# --- Graph Initialization ---

def create_sparse_graph(V, E, directed=False):
    """
    Generates a random sparse graph using an adjacency list.
    
    Args:
        V (int): Number of vertices (nodes).
        E (int): Number of edges.
        directed (bool): If True, graph is directed.
    """
    if V <= 0:
        return {}
    
    # Cap edges for an undirected simple graph
    max_edges = V * (V - 1) // 2
    if E > max_edges:
        E = max_edges 

    adj = {i: [] for i in range(V)}
    
    # Simple method to generate E unique edges
    edges = set()
    while len(edges) < E:
        u = random.randrange(V)
        v = random.randrange(V)
        if u == v:
            continue
        
        # Store edges in canonical order (u, v) where u < v to prevent duplicates like (u,v) and (v,u) in the set
        edge = tuple(sorted((u, v)))
        edges.add(edge)

    # Populate the adjacency list
    for u, v in edges:
        adj[u].append(v)
        if not directed:
            adj[v].append(u)
            
    return adj

# --- BFS Implementation ---

def breadth_first_search(graph, start_node):
    """
    Performs BFS on a graph starting from a given node.
    Complexity is O(V + E), where V is vertices and E is edges.
    
    Returns:
        tuple: (visited_count, path_info)
    """
    if start_node not in graph:
        return 0, {}

    # Use deque for efficient queue operations (O(1) append and popleft)
    queue = collections.deque([start_node])
    
    # Set for O(1) visited lookups
    visited = {start_node}
    
    # Dictionary to store path/parent information
    path = {start_node: None}
    
    while queue:
        u = queue.popleft()
        
        # Iterate over neighbors
        for v in graph.get(u, []):
            if v not in visited:
                visited.add(v)
                path[v] = u
                queue.append(v)
                
    return len(visited), path

# --- BFS Benchmarking Function ---

def benchmark_bfs(V, E, num_runs=5):
    """
    Benchmarks the BFS algorithm on a sparse graph.
    
    Args:
        V (int): Number of vertices.
        E (int): Number of edges.
        num_runs (int): The number of times to run the iteration for averaging.
        
    Returns:
        dict: Results including average time.
    """
    total_time = 0
    
    # Generate the initial graphs and start nodes for each run
    datasets = []
    for _ in range(num_runs):
        graph = create_sparse_graph(V, E, directed=False)
        # Choose a random start node
        start_node = random.randrange(V) if V > 0 else 0
        datasets.append((graph, start_node))
    
    # Warm-up run
    V_warmup = max(10, V // 10)
    E_warmup = max(5, E // 10)
    graph_warmup = create_sparse_graph(V_warmup, E_warmup)
    
    if graph_warmup:
        breadth_first_search(graph_warmup, 0)
    
    for graph, start_node in datasets:
        start_time = time.perf_counter()
        # Execute BFS
        breadth_first_search(graph, start_node)
        end_time = time.perf_counter()
        
        total_time += (end_time - start_time)

    avg_time_ms = (total_time / num_runs) * 1000
    
    return {
        "algorithm": "Breadth-First Search (BFS)",
        "V": V,
        "E": E,
        "complexity": "O(V + E)",
        "num_runs": num_runs,
        "avg_time_ms": avg_time_ms,
    }


# --- Execution ---

if __name__ == "__main__":
    
    print("--- Breadth-First Search (BFS) Benchmark Test Runs ---")
    print("Benchmarking on sparse graphs. Complexity is O(V + E).")
    print("-" * 60)
    
    # --- BFS Benchmark Test 1: Moderate V and E ---
    V1, E1 = 10000, 25000 # 10k nodes, 25k edges
    runs1 = 5
    
    print(f"\n--- Test 1: V={V1:,}, E={E1:,} (Moderate Sparse Graph) ---")
    results1 = benchmark_bfs(V1, E1, runs1)
    
    print(f"Algorithm: {results1['algorithm']}")
    print(f"Vertices (V): {results1['V']:,}")
    print(f"Edges (E): {results1['E']:,}")
    print(f"Complexity: {results1['complexity']}")
    print(f"Total Runs: {results1['num_runs']}")
    print(f"Average Execution Time: {results1['avg_time_ms']:.4f} ms")
    
    print("-" * 60)
    
    # --- BFS Benchmark Test 2: High V (many nodes), Low E (very sparse) ---
    V2, E2 = 50000, 75000 # 50k nodes, 75k edges
    runs2 = 5
    
    print(f"\n--- Test 2: V={V2:,}, E={E2:,} (Larger, Sparser Graph) ---")
    results2 = benchmark_bfs(V2, E2, runs2)
    
    print(f"Algorithm: {results2['algorithm']}")
    print(f"Vertices (V): {results2['V']:,}")
    print(f"Edges (E): {results2['E']:,}")
    print(f"Complexity: {results2['complexity']}")
    print(f"Total Runs: {results2['num_runs']}")
    print(f"Average Execution Time: {results2['avg_time_ms']:.4f} ms")
    
    print("-" * 60)
