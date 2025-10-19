"""
cython.py
This script is called directly by RunnerConfig to run all Cython benchmarks.
Each benchmark lives under experiments/runner/cython/<benchmark_name>/main.py
"""

import subprocess
import sys
import time
from pathlib import Path

ROOT_DIR = Path(__file__).parent
CYTHON_DIR = ROOT_DIR / "cython"


def run_single_benchmark(benchmark_dir: Path):
    """Run a single Cython benchmark's main.py file."""
    main_file = benchmark_dir / "main.py"
    if not main_file.exists():
        print(f"Skipping {benchmark_dir.name}: no main.py found.")
        return None

    print(f"Running benchmark: {benchmark_dir.name}")
    start = time.time()

    # Execute the main.py of that benchmark
    proc = subprocess.Popen(
        [sys.executable, str(main_file)],
        cwd=benchmark_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = proc.communicate()
    end = time.time()

    if proc.returncode != 0:
        print(f"[ERROR] {benchmark_dir.name} failed:\n{stderr}")
        return None

    print(stdout.strip())
    print(f"{benchmark_dir.name} finished in {end - start:.3f}s\n")
    return end - start


def main():
    """Run all sub-benchmarks under the cython directory."""
    print("Starting Cython benchmarks...")

    benchmark_dirs = [p for p in CYTHON_DIR.iterdir() if p.is_dir()]
    results = {}

    for bench in benchmark_dirs:
        duration = run_single_benchmark(bench)
        if duration is not None:
            results[bench.name] = duration

    print("All Cython benchmarks complete.")
    print("Summary:")
    for name, dur in results.items():
        print(f"  {name}: {dur:.3f}s")


if __name__ == "__main__":
    main()
