import time
import random
import math

# --- Quicksort Implementation ---

def quicksort(arr):
    """
    In-place Quicksort implementation (using the rightmost element as pivot).
    Returns a new sorted list.
    """
    def _partition(items, low, high):
        # Pivot (Choosing the rightmost element)
        pivot = items[high]
        i = low - 1 # Index of smaller element

        for j in range(low, high):
            # If current element is smaller than or equal to pivot
            if items[j] <= pivot:
                i = i + 1
                items[i], items[j] = items[j], items[i] # Swap

        items[i + 1], items[high] = items[high], items[i + 1] # Swap pivot to correct position
        return i + 1

    def _quicksort_recursive(items, low, high):
        if low < high:
            # pi is partitioning index, items[pi] is now at right place
            pi = _partition(items, low, high)
            
            # Recursively sort elements before partition and after partition
            _quicksort_recursive(items, low, pi - 1)
            _quicksort_recursive(items, pi + 1, high)

    # Create a copy to perform the sort on (Quicksort is typically in-place)
    arr_copy = arr[:]
    
    if arr_copy:
        _quicksort_recursive(arr_copy, 0, len(arr_copy) - 1)
        
    return arr_copy

# --- Benchmarking Function ---

def benchmark_quicksort(data_size, num_runs=10):
    """
    Benchmarks the Quicksort algorithm using random arrays.
    
    Args:
        data_size (int): The number of elements in the array to sort.
        num_runs (int): The number of times to run the sort for averaging.
        
    Returns:
        dict: Results including average time.
    """
    total_time = 0
    
    # Generate the set of arrays to sort outside the timing loop
    # We use a fresh random array for each run to avoid best/worst-case bias
    datasets = [
        [random.random() for _ in range(data_size)]
        for _ in range(num_runs)
    ]
    
    # Warm-up run
    # Perform a quick, small sort to ensure Python's JIT/interpreter caches are primed
    quicksort([random.random() for _ in range(int(data_size * 0.1))]) 
    
    for data in datasets:
        # Create a mutable copy for the sort process
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


# --- Execution ---

if __name__ == "__main__":
    
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
