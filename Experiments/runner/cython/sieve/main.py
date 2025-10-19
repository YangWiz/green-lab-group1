# main.py
import time
from sieve_cy import sieve_of_eratosthenes

def benchmark_sieve(limit, num_runs=10):
    """
    Benchmarks the Sieve of Eratosthenes algorithm.
    Args:
        limit (int): The upper limit for finding primes.
        num_runs (int): The number of times to run the sieve for averaging.
    Returns:
        dict: Results including average time and the number of primes found.
    """
    total_time = 0
    prime_count = 0
    
    # Warming up the system (optional but good practice for microbenchmarks)
    sieve_of_eratosthenes(int(limit * 0.1))
    
    for _ in range(num_runs):
        start_time = time.perf_counter()
        primes = sieve_of_eratosthenes(limit)
        end_time = time.perf_counter()
        total_time += (end_time - start_time)
        prime_count = len(primes)  # Should be the same every run
    
    avg_time_ms = (total_time / num_runs) * 1000
    
    return {
        "limit": limit,
        "num_runs": num_runs,
        "avg_time_ms": avg_time_ms,
        "prime_count": prime_count,
    }

# --- Execution ---
if __name__ == "__main__":
    # Test 1: Finding primes up to a moderate limit (e.g., 100,000)
    limit_1 = 100000
    runs_1 = 20
    print(f"--- Benchmarking Sieve of Eratosthenes (Limit: {limit_1:,}) ---")
    results_1 = benchmark_sieve(limit_1, runs_1)
    print(f"Limit: {results_1['limit']:,}")
    print(f"Primes Found: {results_1['prime_count']:,}")
    print(f"Total Runs: {results_1['num_runs']}")
    print(f"Average Execution Time: {results_1['avg_time_ms']:.4f} ms")
    print("-" * 40)
    
    # Test 2: Finding primes up to a larger limit (fewer runs needed due to longer runtime)
    limit_2 = 1000000
    runs_2 = 5
    print(f"--- Benchmarking Sieve of Eratosthenes (Limit: {limit_2:,}) ---")
    results_2 = benchmark_sieve(limit_2, runs_2)
    print(f"Limit: {results_2['limit']:,}")
    print(f"Primes Found: {results_2['prime_count']:,}")
    print(f"Total Runs: {results_2['num_runs']}")
    print(f"Average Execution Time: {results_2['avg_time_ms']:.4f} ms")