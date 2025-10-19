import time
import random
import conv_swig

# --- Convolution Implementations (Python version for reference) ---

def convolution_1d(data, kernel):
    """
    1D convolution (implemented as correlation-style) with 'same' padding.
    Complexity is O(N * K), where N is data length and K is kernel size.
    """
    data_len = len(data)
    kernel_len = len(kernel)
    output = [0.0] * data_len
    pad_len = kernel_len // 2 
    
    padded_data = [0.0] * pad_len + data + [0.0] * pad_len
    
    for i in range(data_len):
        sum_val = 0.0
        for k in range(kernel_len):
            sum_val += padded_data[i + k] * kernel[k]
        output[i] = sum_val
    return output


def convolution_2d(image, kernel):
    """
    2D convolution (implemented as correlation-style) with 'same' padding.
    Complexity is O(R * C * K^2), where R and C are image dimensions and K is kernel size.
    """
    rows = len(image)
    if rows == 0: return []
    cols = len(image[0])
    k_size = len(kernel)
    pad = k_size // 2
    
    output = [[0.0] * cols for _ in range(rows)]
    
    padded_image = [[0.0] * (cols + 2 * pad) for _ in range(rows + 2 * pad)]
    for i in range(rows):
        for j in range(cols):
            padded_image[i + pad][j + pad] = image[i][j]

    for r in range(rows):
        for c in range(cols):
            sum_val = 0.0
            for kr in range(k_size):
                for kc in range(k_size):
                    ir = r + kr
                    ic = c + kc
                    sum_val += padded_image[ir][ic] * kernel[kr][kc]
            output[r][c] = sum_val
            
    return output


# --- Convolution Benchmarking Function (SWIG version) ---

def benchmark_convolution(data_size, kernel_size, num_runs=5):
    """Benchmarks 1D and 2D convolution (SWIG version) for given data sizes and kernel sizes."""
    
    # 1. Setup 1D Data and Kernel
    data_1d = [random.random() for _ in range(data_size)]
    kernel_1d = [random.random() for _ in range(kernel_size)]
    
    # 2. Setup 2D Data (Square image) and Kernel
    image_dim = data_size
    data_2d = [[random.random() for _ in range(image_dim)] for _ in range(image_dim)]
    kernel_2d = [[random.random() for _ in range(kernel_size)] for _ in range(kernel_size)]
    
    results = {}
    
    # --- Benchmark 1D ---
    total_time_1d = 0
    # Warmup
    conv_swig.convolution_1d(data_1d[:int(data_size * 0.1)], kernel_1d) 
    
    for _ in range(num_runs):
        start_time = time.perf_counter()
        conv_swig.convolution_1d(data_1d, kernel_1d)
        end_time = time.perf_counter()
        total_time_1d += (end_time - start_time)
        
    results['1D'] = {
        'algorithm': "Convolution 1D (SWIG)",
        'data_size': f"{data_size:,} elements",
        'kernel_size': f"{kernel_size}x1",
        'complexity': "O(N * K)",
        'avg_time_ms': (total_time_1d / num_runs) * 1000,
    }

    # --- Benchmark 2D ---
    total_time_2d = 0
    # Warmup
    if image_dim > 10:
        warmup_size = 10
        conv_swig.convolution_2d(
            [row[:warmup_size] for row in data_2d[:warmup_size]], 
            kernel_2d
        ) 
    
    for _ in range(num_runs):
        start_time = time.perf_counter()
        conv_swig.convolution_2d(data_2d, kernel_2d)
        end_time = time.perf_counter()
        total_time_2d += (end_time - start_time)

    results['2D'] = {
        'algorithm': "Convolution 2D (SWIG)",
        'data_size': f"{image_dim:,}x{image_dim:,} pixels",
        'kernel_size': f"{kernel_size}x{kernel_size}",
        'complexity': "O(N^2 * K^2)",
        'avg_time_ms': (total_time_2d / num_runs) * 1000,
    }
    
    return results


# --- Execution ---

if __name__ == "__main__":
    
    print("--- 1D/2D Convolution Benchmark Test Runs (SWIG) ---")
    print("Benchmarking naive convolution, which is highly sensitive to input size.")
    print("-" * 60)
    
    # --- 1D and 2D Convolution Benchmark ---
    
    # Test 1: 1D Signal
    data_size_1d = 600
    kernel_size_1d = 7
    runs_1d = 10
    
    print(f"\n--- Benchmarking Convolution (1D Signal) ---")
    results_conv = benchmark_convolution(data_size_1d, kernel_size_1d, runs_1d)
    results_1d = results_conv['1D']
    
    print(f"Algorithm: {results_1d['algorithm']}")
    print(f"Data Size: {results_1d['data_size']}")
    print(f"Kernel Size: {results_1d['kernel_size']}")
    print(f"Complexity: {results_1d['complexity']}")
    print(f"Total Runs: {runs_1d}")
    print(f"Average Execution Time: {results_1d['avg_time_ms']:.4f} ms")
    
    print("-" * 60)
    
    # Test 2: 2D Image
    image_dim = 250
    kernel_size_2d = 5
    runs_2d = 5
    
    print(f"\n--- Benchmarking Convolution (2D Image) ---")
    results_conv = benchmark_convolution(image_dim, kernel_size_2d, runs_2d)
    results_2d = results_conv['2D']
    
    print(f"Algorithm: {results_2d['algorithm']}")
    print(f"Data Size: {results_2d['data_size']}")
    print(f"Kernel Size: {results_2d['kernel_size']}")
    print(f"Complexity: {results_2d['complexity']}")
    print(f"Total Runs: {runs_2d}")
    print(f"Average Execution Time: {results_2d['avg_time_ms']:.4f} ms")