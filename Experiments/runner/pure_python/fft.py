#!/usr/bin/env python3
"""
Fast Fourier Transform (FFT) Benchmark
--------------------------------------
Measures runtime and performance of FFT implementations.

Usage:
    python fft_bench.py --size 1024 --runs 5 --method numpy
Methods:
    - naive : pure Python O(N^2) DFT (slow, for small N)
    - numpy : NumPy's optimized FFT (uses Cooley–Tukey)
"""

import numpy as np
import time
import argparse
import csv

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
    if method == "naive":
        _ = dft_naive(x[:8])
    else:
        _ = fft_numpy(x[:8])

    results = []
    for r in range(runs):
        start = time.perf_counter()
        if method == "naive":
            X = dft_naive(x)
        elif method == "numpy":
            X = fft_numpy(x)
        else:
            raise ValueError(f"Unknown method: {method}")
        end = time.perf_counter()

        elapsed = end - start
        # Approximate operation count for FFT: ~5*N*log2(N) complex ops
        flops = 5 * N * np.log2(N)
        gflops = flops / (elapsed * 1e9)

        results.append({
            "method": method,
            "N": N,
            "run": r,
            "time_s": elapsed,
            "GFLOPS_eq": gflops
        })
        print(f"[Run {r+1}/{runs}] {method:6s} | N={N:6d} | Time={elapsed:.6f}s | {gflops:.3f} GFLOPS-eq")

    return results

# ------------------ CLI ------------------

def main():
    parser = argparse.ArgumentParser(description="FFT benchmark (naive vs numpy).")
    parser.add_argument("--size", "-n", type=int, default=1024, help="Signal size N")
    parser.add_argument("--runs", "-r", type=int, default=3, help="Number of runs")
    parser.add_argument("--method", "-m", choices=["naive", "numpy"], default="numpy")
    parser.add_argument("--output", "-o", type=str, default="", help="Optional CSV output file")
    args = parser.parse_args()

    results = benchmark_fft(args.method, args.size, args.runs)

    if args.output:
        with open(args.output, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["method", "N", "run", "time_s", "GFLOPS_eq"])
            writer.writeheader()
            writer.writerows(results)
        print(f"\nResults saved to {args.output}")

if __name__ == "__main__":
    main()
