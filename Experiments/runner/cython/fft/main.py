#!/usr/bin/env python3
"""
Fast Fourier Transform (FFT) Benchmark
--------------------------------------
Measures runtime and performance of FFT implementations.
Usage:
    python fft_bench.py --size 1024 --runs 5 --method numpy
Methods:
    - naive      : pure Python O(N^2) DFT (slow, for small N)
    - naive_cy   : Cython-optimized O(N^2) DFT
    - cooley_cy  : Cython recursive Cooley-Tukey FFT O(N log N)
    - iterative_cy: Cython iterative FFT O(N log N) - fastest
    - numpy      : NumPy's optimized FFT (uses Cooley–Tukey)
"""
import numpy as np
import time
import argparse
import csv
from fft_cy import dft_naive_cy, fft_cooley_tukey_cy, fft_iterative_cy

# ------------------ Implementations ------------------

def dft_naive(x):
    """
    Naive Discrete Fourier Transform (O(N^2)).
    Input: x — 1D complex array.
    Output: complex DFT result.
    """
    N = len(x)
    X = np.zeros(N, dtype=complex)
    for k in range(N):
        s = 0j
        for n in range(N):
            angle = -2j * np.pi * k * n / N
            s += x[n] * np.exp(angle)
        X[k] = s
    return X


def fft_numpy(x):
    """Optimized FFT using NumPy (highly optimized, Cooley–Tukey)."""
    return np.fft.fft(x)


# ------------------ Benchmark Logic ------------------

def benchmark_fft(method, N, runs=3, seed=0):
    np.random.seed(seed)
    x = np.random.rand(N) + 1j * np.random.rand(N)
    
    # Warmup (avoid startup overheads)
    warmup_size = min(8, N)
    if method == "naive":
        _ = dft_naive(x[:warmup_size])
    elif method == "naive_cy":
        _ = dft_naive_cy(x[:warmup_size])
    elif method in ["cooley_cy", "iterative_cy"]:
        # Need power of 2 for warmup
        warmup_pow2 = 8 if N >= 8 else N
        _ = fft_iterative_cy(x[:warmup_pow2])
    else:
        _ = fft_numpy(x[:warmup_size])
    
    results = []
    for r in range(runs):
        start = time.perf_counter()
        
        if method == "naive":
            X = dft_naive(x)
        elif method == "naive_cy":
            X = dft_naive_cy(x)
        elif method == "cooley_cy":
            X = fft_cooley_tukey_cy(x)
        elif method == "iterative_cy":
            X = fft_iterative_cy(x)
        elif method == "numpy":
            X = fft_numpy(x)
        else:
            raise ValueError(f"Unknown method: {method}")
        
        end = time.perf_counter()
        elapsed = end - start
        
        # Approximate operation count for FFT: ~5*N*log2(N) complex ops
        # For DFT: ~N^2 operations
        if method in ["naive", "naive_cy"]:
            flops = 8 * N * N  # 8 real ops per complex multiply
        else:
            flops = 5 * N * np.log2(N)
        
        gflops = flops / (elapsed * 1e9)
        
        results.append({
            "method": method,
            "N": N,
            "run": r,
            "time_s": elapsed,
            "GFLOPS_eq": gflops
        })
        
        print(f"[Run {r+1}/{runs}] {method:12s} | N={N:6d} | Time={elapsed:.6f}s | {gflops:.3f} GFLOPS-eq")
    
    return results


# ------------------ CLI ------------------

def main():
    parser = argparse.ArgumentParser(description="FFT benchmark (naive vs numpy vs Cython).")
    parser.add_argument("--size", "-n", type=int, default=1024, help="Signal size N")
    parser.add_argument("--runs", "-r", type=int, default=3, help="Number of runs")
    parser.add_argument("--method", "-m", 
                       choices=["naive", "naive_cy", "cooley_cy", "iterative_cy", "numpy"], 
                       default="numpy",
                       help="FFT method to benchmark")
    parser.add_argument("--output", "-o", type=str, default="", help="Optional CSV output file")
    parser.add_argument("--compare", action="store_true", 
                       help="Run all methods and compare (size must be power of 2)")
    
    args = parser.parse_args()
    
    if args.compare:
        # Check if size is power of 2
        if args.size & (args.size - 1) != 0:
            print(f"Warning: Size {args.size} is not a power of 2. Setting to {2**int(np.log2(args.size))}")
            args.size = 2**int(np.log2(args.size))
        
        print(f"\n{'='*70}")
        print(f"FFT COMPARISON BENCHMARK (N={args.size}, Runs={args.runs})")
        print(f"{'='*70}\n")
        
        all_results = []
        methods = ["numpy", "iterative_cy", "cooley_cy"]
        
        # Only include naive methods for small sizes
        if args.size <= 2048:
            methods.extend(["naive_cy", "naive"])
        
        for method in methods:
            print(f"\n--- {method.upper()} ---")
            try:
                results = benchmark_fft(method, args.size, args.runs)
                all_results.extend(results)
            except Exception as e:
                print(f"Error with {method}: {e}")
        
        # Print summary
        print(f"\n{'='*70}")
        print("SUMMARY (Average Times)")
        print(f"{'='*70}")
        for method in methods:
            method_results = [r for r in all_results if r['method'] == method]
            if method_results:
                avg_time = np.mean([r['time_s'] for r in method_results])
                avg_gflops = np.mean([r['GFLOPS_eq'] for r in method_results])
                print(f"{method:12s}: {avg_time:.6f}s | {avg_gflops:.3f} GFLOPS-eq")
        
        if args.output:
            with open(args.output, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["method", "N", "run", "time_s", "GFLOPS_eq"])
                writer.writeheader()
                writer.writerows(all_results)
            print(f"\nResults saved to {args.output}")
    else:
        results = benchmark_fft(args.method, args.size, args.runs)
        
        if args.output:
            with open(args.output, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["method", "N", "run", "time_s", "GFLOPS_eq"])
                writer.writeheader()
                writer.writerows(results)
            print(f"\nResults saved to {args.output}")


if __name__ == "__main__":
    main()