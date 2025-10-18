import time
import json
import random
import string
import math

# --- JSON Data Generation ---

def generate_random_string(length):
    """Generates a random alphanumeric string."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

def create_complex_data(num_records):
    """
    Creates a complex, nested Python dictionary/list structure for JSON testing.
    
    The structure simulates records with various data types (string, int, float, list, dict).
    Complexity is roughly O(N * D) where N is records and D is max depth.
    """
    data_list = []
    
    for i in range(num_records):
        record = {
            "id": i,
            "uuid": generate_random_string(32),
            "isActive": random.choice([True, False]),
            "balance": round(random.uniform(10.0, 50000.0), 2),
            "tags": [generate_random_string(5) for _ in range(random.randint(2, 5))],
            "profile": {
                "age": random.randint(18, 65),
                "city": generate_random_string(10),
                "isVerified": random.choice([True, False])
            },
            "history": [
                {"timestamp": time.time() - random.randint(100, 10000), "amount": round(random.uniform(-100, 100), 2)}
                for _ in range(random.randint(1, 3))
            ]
        }
        data_list.append(record)
        
    return {"metadata": {"count": num_records, "timestamp": time.time()}, "records": data_list}

# --- JSON Benchmarking Function ---

def benchmark_json_io(num_records, num_runs=5):
    """
    Benchmarks JSON encoding (dumps) and decoding (loads) performance.
    
    Args:
        num_records (int): The number of records to generate for the complex data structure.
        num_runs (int): The number of times to run the full IO cycle for averaging.
        
    Returns:
        dict: Results including average time for dumps, loads, and total.
    """
    # 1. Generate the initial complex Python object once
    py_data = create_complex_data(num_records)
    
    # Warm-up run
    warmup_json = json.dumps(py_data)
    json.loads(warmup_json)
    
    total_dump_time = 0
    total_load_time = 0
    
    for _ in range(num_runs):
        
        # --- Encode (dumps) ---
        start_dump = time.perf_counter()
        json_string = json.dumps(py_data)
        end_dump = time.perf_counter()
        total_dump_time += (end_dump - start_dump)
        
        # --- Decode (loads) ---
        start_load = time.perf_counter()
        json.loads(json_string)
        end_load = time.perf_counter()
        total_load_time += (end_load - start_load)

    avg_dump_time_ms = (total_dump_time / num_runs) * 1000
    avg_load_time_ms = (total_load_time / num_runs) * 1000
    avg_total_time_ms = avg_dump_time_ms + avg_load_time_ms
    
    # Get size information from one run
    json_size_kb = len(json_string.encode('utf-8')) / 1024
    
    return {
        "algorithm": "JSON Encode/Decode (dumps/loads)",
        "num_records": num_records,
        "json_size_kb": json_size_kb,
        "num_runs": num_runs,
        "avg_dump_ms": avg_dump_time_ms,
        "avg_load_ms": avg_load_time_ms,
        "avg_total_ms": avg_total_time_ms,
    }


# --- Execution ---

if __name__ == "__main__":
    
    print("--- JSON Encode/Decode Microbenchmark Test Runs ---")
    print("Benchmarking performance of Python's built-in 'json' module.")
    print("-" * 70)
    
    # --- JSON Benchmark Test 1: Moderate Data Size ---
    num_records_1 = 5000
    runs1 = 10
    
    print(f"\n--- Test 1: {num_records_1:,} Complex Records ---")
    results1 = benchmark_json_io(num_records_1, runs1)
    
    print(f"Algorithm: {results1['algorithm']}")
    print(f"Records Processed: {results1['num_records']:,}")
    print(f"Approx. JSON Size: {results1['json_size_kb']:.2f} KB")
    print(f"Total Runs: {results1['num_runs']}")
    print(f"  Avg. Encode (dumps) Time: {results1['avg_dump_ms']:.4f} ms")
    print(f"  Avg. Decode (loads) Time: {results1['avg_load_ms']:.4f} ms")
    print(f"  Avg. Total I/O Time:      {results1['avg_total_ms']:.4f} ms")
    
    print("-" * 70)
    
    # --- JSON Benchmark Test 2: Larger Data Size ---
    num_records_2 = 20000
    runs2 = 5
    
    print(f"\n--- Test 2: {num_records_2:,} Complex Records ---")
    results2 = benchmark_json_io(num_records_2, runs2)
    
    print(f"Algorithm: {results2['algorithm']}")
    print(f"Records Processed: {results2['num_records']:,}")
    print(f"Approx. JSON Size: {results2['json_size_kb']:.2f} KB")
    print(f"Total Runs: {results2['num_runs']}")
    print(f"  Avg. Encode (dumps) Time: {results2['avg_dump_ms']:.4f} ms")
    print(f"  Avg. Decode (loads) Time: {results2['avg_load_ms']:.4f} ms")
    print(f"  Avg. Total I/O Time:      {results2['avg_total_ms']:.4f} ms")
    
    print("-" * 70)
