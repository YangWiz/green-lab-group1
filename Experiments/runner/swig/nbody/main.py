import time
import random
import math
import nbody_swig

# --- Quicksort Implementation (Python - unchanged) ---

def quicksort(arr):
    """
    In-place Quicksort implementation (using the rightmost element as pivot).
    Returns a new sorted list.
    """
    def _partition(items, low, high):
        pivot = items[high]
        i = low - 1
        
        for j in range(low, high):
            if items[j] <= pivot:
                i = i + 1
                items[i], items[j] = items[j], items[i]
        
        items[i + 1], items[high] = items[high], items[i + 1]
        return i + 1
    
    def _quicksort_recursive(items, low, high):
        if low < high:
            pi = _partition(items, low, high)
            _quicksort_recursive(items, low, pi - 1)
            _quicksort_recursive(items, pi + 1, high)
    
    arr_copy = arr[:]
    if arr_copy:
        _quicksort_recursive(arr_copy, 0, len(arr_copy) - 1)
    return arr_copy


def benchmark_quicksort(data_size, num_runs=10):
    """Benchmarks the Quicksort algorithm using random arrays."""
    total_time = 0
    
    datasets = [
        [random.random() for _ in range(data_size)]
        for _ in range(num_runs)
    ]
    
    quicksort([random.random() for _ in range(int(data_size * 0.1))])
    
    for data in datasets:
        arr_to_sort = data[:]
        start_time = time.perf_counter()
        quicksort(arr_to_sort)
        end_time = time.perf_counter()
        total_time += (end_time - start_time)
    
    avg_time_ms = (total_time / num_runs) * 1000
    
    return {
        "algorithm": "Quicksort",
        "data_size": data_size,
        "num_runs": num_runs,
        "avg_time_ms": avg_time_ms,
    }


# --- N-body Simulation Implementation (Python version for reference) ---

def initialize_bodies(N, box_size=100.0, max_mass=1.0):
    """Generates N bodies with random positions, velocities, and masses."""
    bodies = []
    for _ in range(N):
        bodies.append({
            'x': random.uniform(0, box_size),
            'y': random.uniform(0, box_size),
            'vx': random.uniform(-1, 1),
            'vy': random.uniform(-1, 1),
            'm': random.uniform(0.1, max_mass),
        })
    return bodies


def nbody_step_update(bodies, dt, G=6.674e-11, softening=1e-9):
    """Calculates one step of a 2D N-body simulation using pairwise interactions."""
    N = len(bodies)
    accelerations = []
    
    for i in range(N):
        ax, ay = 0.0, 0.0
        body_i = bodies[i]
        
        for j in range(N):
            if i == j:
                continue
            
            body_j = bodies[j]
            dx = body_j['x'] - body_i['x']
            dy = body_j['y'] - body_i['y']
            dist_sq = dx*dx + dy*dy
            dist_soft = math.sqrt(dist_sq + softening)
            inv_dist_cube = 1.0 / (dist_soft * dist_soft * dist_soft)
            force_factor = G * body_j['m'] * inv_dist_cube
            ax += dx * force_factor
            ay += dy * force_factor
        
        accelerations.append((ax, ay))
    
    for i in range(N):
        body = bodies[i]
        ax, ay = accelerations[i]
        body['vx'] += ax * dt
        body['vy'] += ay * dt
        body['x'] += body['vx'] * dt
        body['y'] += body['vy'] * dt
    
    return bodies


# --- N-body Benchmarking Function (SWIG version) ---

def benchmark_nbody(N, num_runs=5, dt=0.01):
    """Benchmarks a single N-body step update (SWIG version)."""
    total_time = 0
    
    # Generate the starting state (this is only done once)
    initial_bodies = nbody_swig.initialize_bodies(N, box_size=1000.0)
    
    # Create fresh copies for each run
    datasets = [nbody_swig.BodiesVector(initial_bodies) for _ in range(num_runs)]
    
    # Warm-up run (small number of bodies)
    nbody_swig.nbody_step_update(nbody_swig.initialize_bodies(int(N * 0.1)), dt)
    
    for bodies in datasets:
        start_time = time.perf_counter()
        nbody_swig.nbody_step_update(bodies, dt)
        end_time = time.perf_counter()
        
        total_time += (end_time - start_time)
    
    avg_time_ms = (total_time / num_runs) * 1000
    
    return {
        "algorithm": "N-Body Step Update (O(N^2)) - SWIG",
        "N": N,
        "num_runs": num_runs,
        "avg_time_ms": avg_time_ms,
    }


# --- Execution ---

if __name__ == "__main__":
    
    # --- Quicksort Benchmarks ---
    print("--- Quicksort Benchmark Test Runs ---")
    
    # Test 1: Moderate array size
    data_size_1 = 50000
    runs_1 = 10
    print(f"\n--- Benchmarking Quicksort (Array Size: {data_size_1:,}) ---")
    results_1 = benchmark_quicksort(data_size_1, runs_1)
    
    print(f"Algorithm: {results_1['algorithm']}")
    print(f"Data Size: {results_1['data_size']:,} elements (Random floats)")
    print(f"Total Runs: {results_1['num_runs']}")
    print(f"Average Execution Time: {results_1['avg_time_ms']:.4f} ms")
    
    print("-" * 40)
    
    # Test 2: Larger array size
    data_size_2 = 150000
    runs_2 = 5
    print(f"\n--- Benchmarking Quicksort (Array Size: {data_size_2:,}) ---")
    results_2 = benchmark_quicksort(data_size_2, runs_2)
    
    print(f"Algorithm: {results_2['algorithm']}")
    print(f"Data Size: {results_2['data_size']:,} elements (Random floats)")
    print(f"Total Runs: {results_2['num_runs']}")
    print(f"Average Execution Time: {results_2['avg_time_ms']:.4f} ms")
    
    print("-" * 40)
    print("-" * 40)
    
    # --- N-Body Benchmarks (SWIG) ---
    print("--- N-Body Step Update Benchmark Test Runs (O(N^2)) ---")
    
    # Test 3: Moderate number of bodies
    N_3 = 500
    runs_3 = 10
    print(f"\n--- Benchmarking N-Body (N={N_3:,} bodies) ---")
    results_3 = benchmark_nbody(N_3, runs_3)
    
    print(f"Algorithm: {results_3['algorithm']}")
    print(f"Number of Bodies (N): {results_3['N']:,}")
    print(f"Total Runs: {results_3['num_runs']}")
    print(f"Average Execution Time: {results_3['avg_time_ms']:.4f} ms")
    
    print("-" * 40)
    
    # Test 4: Larger number of bodies
    N_4 = 1500
    runs_4 = 3
    print(f"\n--- Benchmarking N-Body (N={N_4:,} bodies) ---")
    results_4 = benchmark_nbody(N_4, runs_4)
    
    print(f"Algorithm: {results_4['algorithm']}")
    print(f"Number of Bodies (N): {results_4['N']:,}")
    print(f"Total Runs: {results_4['num_runs']}")
    print(f"Average Execution Time: {results_4['avg_time_ms']:.4f} ms")