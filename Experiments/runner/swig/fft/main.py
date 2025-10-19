#!/usr/bin/env python3
"""
Fast Fourier Transform (FFT) Benchmark (SWIG)
--------------------------------------
Measures runtime and performance of FFT implementations.
Usage:
    python fft_bench.py --size 1024 --runs 5 --method swig_iterative
Methods:
    - naive : pure Python O(N^2) DFT (slow, for small N)
    - numpy : NumPy's optimized FFT (uses Cooley–Tukey)
    - swig_naive : SWIG naive DFT O(N^2)
    - swig_recursive : SWIG recursive Cooley-Tukey FFT
    - swig_iterative : SWIG iterative FFT (fastest)
"""
import numpy as np
import time
import argparse
import csv
import fft_swig

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
    
    # Convert to SWIG ComplexVector for SWIG methods
    if method.startswith("swig_"):
        x_swig = fft_swig.ComplexVector()
        for val in x:
            x_swig.append(complex(val))
    
    # Warmup (avoid startup overheads)
    if method == "naive":
        _ = dft_naive(x[:8])
    elif method.startswith("swig_"):
        warmup = fft_swig.ComplexVector()
        for i in range(8):
            warmup.append(complex(x[i]))
        _ = fft_swig.dft_naive(warmup)
    else:
        _ = fft_numpy(x[:8])
    
    results = []
    for r in range(runs):
        start = time.perf_counter()
        
        if method == "naive":
            X = dft_naive(x)
        elif method == "numpy":
            X = fft_numpy(x)
        elif method == "swig_naive":
            X = fft_swig.dft_naive(x_swig)
        elif method == "swig_recursive":
            X = fft_swig.fft_cooley_tukey(x_swig)
        elif method == "swig_iterative":
            X = fft_swig.fft_iterative(x_swig)
        else:
            raise ValueError(f"Unknown method: {method}")
        
        end = time.perf_counter()
        elapsed = end - start
        
        # Approximate operation count for FFT: ~5*N*log2(N) complex ops
        # For DFT: ~N^2 operations
        if method in ["naive", "swig_naive"]:
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
        
        print(f"[Run {r+1}/{runs}] {method:15s} | N={N:6d} | Time={elapsed:.6f}s | {gflops:.3f} GFLOPS-eq")
    
    return results


# ------------------ CLI ------------------

def main():
    parser = argparse.ArgumentParser(description="FFT benchmark (Python vs NumPy vs SWIG).")
    parser.add_argument("--size", "-n", type=int, default=1024, help="Signal size N")
    parser.add_argument("--runs", "-r", type=int, default=3, help="Number of runs")
    parser.add_argument("--method", "-m", 
                       choices=["naive", "numpy", "swig_naive", "swig_recursive", "swig_iterative"], 
                       default="swig_iterative")
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