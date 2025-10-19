#!/usr/bin/env python3
"""
Dense Matrix Multiplication Benchmark (SWIG)
-------------------------------------
Measures runtime and GFLOPS for dense matrix multiplication.
Usage:
    python matmul_bench.py --size 512 --runs 5 --method swig_naive
Methods:
    - naive : pure Python triple loop
    - numpy : NumPy's optimized dot()
    - blocked : cache-friendly blocked implementation
    - swig_naive : SWIG naive implementation
    - swig_blocked : SWIG blocked implementation
    - swig_transpose : SWIG with transposed B
"""
import numpy as np
import time
import argparse
import csv
import matmul_swig

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
    
    # Convert to list of lists for SWIG methods
    if method.startswith("swig_"):
        A_list = A.tolist()
        B_list = B.tolist()
    
    # Warmup
    if method == "naive":
        _ = matmul_naive(A[:8, :8], B[:8, :8])
    elif method.startswith("swig_"):
        warmup_A = [[A[i][j] for j in range(8)] for i in range(8)]
        warmup_B = [[B[i][j] for j in range(8)] for i in range(8)]
        _ = matmul_swig.matmul_naive(warmup_A, warmup_B)
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
        elif method == "swig_naive":
            C = matmul_swig.matmul_naive(A_list, B_list)
        elif method == "swig_blocked":
            C = matmul_swig.matmul_blocked(A_list, B_list, block_size)
        elif method == "swig_transpose":
            C = matmul_swig.matmul_transpose(A_list, B_list)
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
        
        print(f"[Run {r+1}/{runs}] {method:15s} | N={N:4d} | Time={elapsed:.4f}s | {gflops:.2f} GFLOPS")
    
    return results


# ------------------ CLI ------------------

def main():
    parser = argparse.ArgumentParser(description="Dense matrix multiplication benchmark (SWIG).")
    parser.add_argument("--size", "-n", type=int, default=512, help="Matrix size N (NxN)")
    parser.add_argument("--runs", "-r", type=int, default=3, help="Number of runs")
    parser.add_argument("--method", "-m", 
                       choices=["naive", "blocked", "numpy", "swig_naive", "swig_blocked", "swig_transpose"], 
                       default="swig_naive")
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