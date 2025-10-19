import time
import random
from bfs_cy import create_sparse_graph_cy, breadth_first_search_cy

# --- BFS Benchmarking Function ---

def benchmark_bfs(V, E, num_runs=5):
    """
    Benchmarks the Cython BFS algorithm on a sparse graph.
    
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
        graph = create_sparse_graph_cy(V, E, directed=False)
        # Choose a random start node
        start_node = random.randrange(V) if V > 0 else 0
        datasets.append((graph, start_node))
    
    # Warm-up run
    V_warmup = max(10, V // 10)
    E_warmup = max(5, E // 10)
    graph_warmup = create_sparse_graph_cy(V_warmup, E_warmup)
    
    if graph_warmup:
        breadth_first_search_cy(graph_warmup, 0)
    
    for graph, start_node in datasets:
        start_time = time.perf_counter()
        # Execute BFS
        breadth_first_search_cy(graph, start_node)
        end_time = time.perf_counter()
        
        total_time += (end_time - start_time)

    avg_time_ms = (total_time / num_runs) * 1000
    
    return {
        "algorithm": "Breadth-First Search (BFS) - Cython",
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
    V1, E1 = 10000, 25000  # 10k nodes, 25k edges
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
    V2, E2 = 50000, 75000  # 50k nodes, 75k edges
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