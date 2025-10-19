#!/usr/bin/env python3
"""
Dense Matrix Multiplication Benchmark
-------------------------------------
Measures runtime and GFLOPS for dense matrix multiplication.
Usage:
    python matmul_bench.py --size 1024 --runs 5 --method numpy
Methods:
    - naive : pure Python triple loop
    - numpy : NumPy's optimized dot()
    - blocked : cache-friendly blocked implementation
    - naive_cy : Cython optimized naive
    - blocked_cy : Cython optimized blocked
    - transpose_cy : Cython with transposed B
"""
import numpy as np
import time
import argparse
import csv
from matmul_cy import matmul_naive_cy, matmul_blocked_cy, matmul_transpose_cy

# ------------------ Implementations ------------------

def matmul_naive(A, B):
    """Naive O(N^3) triple loop matrix multiplication."""
    n = A.shape[0]
    C = np.zeros((n, n), dtype=A.dtype)
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i, j] += A[i, k] * B[k, j]
    return C


def matmul_blocked(A, B, block_size=64):
    """Blocked/tiled matrix multiplication for better cache reuse."""
    n = A.shape[0]
    C = np.zeros((n, n), dtype=A.dtype)
    for ii in range(0, n, block_size):
        for jj in range(0, n, block_size):
            for kk in range(0, n, block_size):
                i_max = min(ii + block_size, n)
                j_max = min(jj + block_size, n)
                k_max = min(kk + block_size, n)
                C[ii:i_max, jj:j_max] += np.dot(
                    A[ii:i_max, kk:k_max],
                    B[kk:k_max, jj:j_max]
                )
    return C


def matmul_numpy(A, B):
    """Optimized NumPy-based matrix multiplication."""
    return A @ B  # or np.dot(A, B)


# ------------------ Benchmark Logic ------------------

def benchmark(method, N, runs=3, block_size=64, seed=0):
    np.random.seed(seed)
    A = np.random.rand(N, N)
    B = np.random.rand(N, N)
    
    # Warmup
    if method == "naive":
        _ = matmul_naive(A[:8, :8], B[:8, :8])
    elif method in ["naive_cy", "blocked_cy", "transpose_cy"]:
        _ = matmul_naive_cy(A[:8, :8], B[:8, :8])
    else:
        _ = matmul_numpy(A[:8, :8], B[:8, :8])
    
    results = []
    for r in range(runs):
        start = time.perf_counter()
        
        if method == "naive":
            C = matmul_naive(A, B)
        elif method == "blocked":
            C = matmul_blocked(A, B, block_size)
        elif method == "numpy":
            C = matmul_numpy(A, B)
        elif method == "naive_cy":
            C = matmul_naive_cy(A, B)
        elif method == "blocked_cy":
            C = matmul_blocked_cy(A, B, block_size)
        elif method == "transpose_cy":
            C = matmul_transpose_cy(A, B)
        else:
            raise ValueError(f"Unknown method: {method}")
        
        end = time.perf_counter()
        elapsed = end - start
        flops = 2 * (N ** 3)
        gflops = flops / (elapsed * 1e9)
        
        results.append({
            "method": method,
            "N": N,
            "run": r,
            "time_s": elapsed,
            "GFLOPS": gflops
        })
        
        print(f"[Run {r+1}/{runs}] {method:12s} | N={N:4d} | Time={elapsed:.4f}s | {gflops:.2f} GFLOPS")
    
    return results


# ------------------ CLI ------------------

def main():
    parser = argparse.ArgumentParser(description="Dense matrix multiplication benchmark.")
    parser.add_argument("--size", "-n", type=int, default=512, help="Matrix size N (NxN)")
    parser.add_argument("--runs", "-r", type=int, default=3, help="Number of runs")
    parser.add_argument("--method", "-m", 
                       choices=["naive", "blocked", "numpy", "naive_cy", "blocked_cy", "transpose_cy"], 
                       default="numpy")
    parser.add_argument("--block", "-b", type=int, default=64, help="Block size for blocked method")
    parser.add_argument("--output", "-o", type=str, default="", help="Optional CSV output file")
    
    args = parser.parse_args()
    
    results = benchmark(args.method, args.size, args.runs, args.block)
    
    if args.output:
        with open(args.output, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["method", "N", "run", "time_s", "GFLOPS"])
            writer.writeheader()
            writer.writerows(results)
        print(f"\nResults saved to {args.output}")


if __name__ == "__main__":
    main()