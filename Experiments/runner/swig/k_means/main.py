import time
import random
import math
import kmeans_swig

# --- K-means Implementations (Python version for reference) ---

def _euclidean_distance(p1, p2):
    """Calculates the Euclidean distance between two D-dimensional points."""
    distance_sq = sum((p1[i] - p2[i]) ** 2 for i in range(len(p1)))
    return math.sqrt(distance_sq)


def initialize_data(N, D, max_val=100):
    """Generates N random D-dimensional data points."""
    data = []
    for _ in range(N):
        point = tuple(random.uniform(0, max_val) for _ in range(D))
        data.append(point)
    return data


def initialize_centroids(data, K):
    """Selects K random data points as initial centroids."""
    return random.sample(data, K)


def kmeans_iteration(data, centroids):
    """
    Performs a single K-means iteration (assignment and centroid update).
    Complexity is O(N * K * D), where N is data points, K is clusters, and D is dimensions.
    
    Returns:
        list: The new list of centroids.
    """
    N = len(data)
    K = len(centroids)
    if N == 0 or K == 0:
        return centroids

    D = len(data[0])
    
    # 1. Assignment Step (O(N * K * D))
    clusters = [[] for _ in range(K)]
    
    for point in data:
        min_dist = float('inf')
        closest_k = -1
        
        for k in range(K):
            dist = _euclidean_distance(point, centroids[k])
            if dist < min_dist:
                min_dist = dist
                closest_k = k
        
        clusters[closest_k].append(point)

    # 2. Update Step (O(N))
    new_centroids = []
    for k in range(K):
        cluster_points = clusters[k]
        
        if not cluster_points:
            new_centroids.append(centroids[k])
            continue
            
        # Calculate the mean of the cluster points
        new_centroid = [0.0] * D
        
        # Sum all coordinates
        for point in cluster_points:
            for d in range(D):
                new_centroid[d] += point[d]
        
        # Divide by the count to get the average
        count = len(cluster_points)
        for d in range(D):
            new_centroid[d] /= count
            
        new_centroids.append(tuple(new_centroid))
        
    return new_centroids


# --- K-means Benchmarking Function (SWIG version) ---

def benchmark_kmeans(N, D, K, num_runs=5):
    """
    Benchmarks the K-means iteration algorithm (SWIG version).
    
    Args:
        N (int): Number of data points.
        D (int): Dimensionality of data points.
        K (int): Number of clusters.
        num_runs (int): The number of times to run the iteration for averaging.
        
    Returns:
        dict: Results including average time.
    """
    total_time = 0
    
    # Generate the initial data set (static for all runs)
    initial_data = kmeans_swig.initialize_data(N, D)
    
    # Generate unique starting centroids for each run
    initial_states = [
        (initial_data, kmeans_swig.initialize_centroids(initial_data, K))
        for _ in range(num_runs)
    ]
    
    # Warm-up run with smaller data
    N_warmup = max(10, int(N * 0.1))
    D_warmup = max(1, D)
    K_warmup = max(1, K)
    
    warmup_data = kmeans_swig.initialize_data(N_warmup, D_warmup)
    warmup_centroids = kmeans_swig.initialize_centroids(warmup_data, K_warmup)
    kmeans_swig.kmeans_iteration(warmup_data, warmup_centroids)
    
    for data, centroids in initial_states:
        start_time = time.perf_counter()
        kmeans_swig.kmeans_iteration(data, centroids)
        end_time = time.perf_counter()
        
        total_time += (end_time - start_time)

    avg_time_ms = (total_time / num_runs) * 1000
    
    return {
        "algorithm": "K-means Single Iteration (SWIG)",
        "N": N,
        "D": D,
        "K": K,
        "complexity": "O(N * K * D)",
        "num_runs": num_runs,
        "avg_time_ms": avg_time_ms,
    }


# --- Execution ---

if __name__ == "__main__":
    
    print("--- K-means Single Iteration Benchmark Test Runs (SWIG) ---")
    print("Benchmarking is sensitive to N (data points), K (clusters), and D (dimensions).")
    print("-" * 60)
    
    # --- K-means Benchmark Test 1: High N (data points), Low K (clusters) ---
    N1, D1, K1 = 20000, 5, 10
    runs1 = 5
    
    print(f"\n--- Test 1: N={N1:,}, D={D1}, K={K1} ---")
    results1 = benchmark_kmeans(N1, D1, K1, runs1)
    
    print(f"Algorithm: {results1['algorithm']}")
    print(f"Data Points (N): {results1['N']:,}")
    print(f"Dimensions (D): {results1['D']}")
    print(f"Clusters (K): {results1['K']}")
    print(f"Complexity: {results1['complexity']}")
    print(f"Total Runs: {results1['num_runs']}")
    print(f"Average Execution Time: {results1['avg_time_ms']:.4f} ms")
    
    print("-" * 60)
    
    # --- K-means Benchmark Test 2: High D (dimensions), Moderate N ---
    N2, D2, K2 = 5000, 100, 15
    runs2 = 5
    
    print(f"\n--- Test 2: N={N2:,}, D={D2}, K={K2} (Focus on dimensionality) ---")
    results2 = benchmark_kmeans(N2, D2, K2, runs2)
    
    print(f"Algorithm: {results2['algorithm']}")
    print(f"Data Points (N): {results2['N']:,}")
    print(f"Dimensions (D): {results2['D']}")
    print(f"Clusters (K): {results2['K']}")
    print(f"Complexity: {results2['complexity']}")
    print(f"Total Runs: {results2['num_runs']}")
    print(f"Average Execution Time: {results2['avg_time_ms']:.4f} ms")