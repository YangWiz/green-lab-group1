import time
import random
import re
import regex_swig

# --- Regular Expression Tokenization Implementation ---

# Complex pattern to simulate a "heavy" tokenization load
TOKENIZATION_PATTERN = re.compile(
    r"\b\w+(?:'\w+)?\b"  # Captures words, including contractions like "don't"
    r"|[\.\,\;\:\?\!]+"   # Captures common punctuation sequences
    r"|\s+"              # Captures whitespace sequences
    r"|(?:https?:\/\/)?(?:www\.)?\S+\.\S+" # Captures simple URLs
)

def regex_tokenize(text, pattern=TOKENIZATION_PATTERN):
    """
    Performs heavy tokenization using a complex regular expression.
    
    Args:
        text (str): The input string to tokenize.
        pattern (re.Pattern): The compiled regex pattern.
        
    Returns:
        list: A list of matched tokens.
    """
    return pattern.findall(text)


# --- Tokenization Benchmarking Function ---

def benchmark_tokenizer(text_size_kb, num_runs=5, method='swig'):
    """
    Benchmarks the tokenization process.
    
    Args:
        text_size_kb (int): The target size of the input text in kilobytes (KB).
        num_runs (int): The number of times to run the tokenization for averaging.
        method (str): 'swig' for SWIG implementation, 'regex' for Python regex
        
    Returns:
        dict: Results including average time.
    """
    total_time = 0
    
    # 1. Generate the test data
    base_corpus = "The quick brown fox jumps over the lazy dog's fence. " * 10
    
    target_size_bytes = text_size_kb * 1024
    data_text = base_corpus * (target_size_bytes // len(base_corpus) + 1)
    data_text = data_text[:target_size_bytes] 
    
    # Add complexity
    def add_complexity(text):
        return text.replace("fox", "12345.67 fox") + " https://example.com/page?id=1"
        
    data_text = add_complexity(data_text)
    
    # Warm-up run
    if method == 'swig':
        regex_swig.simple_tokenize(data_text[:1000])
    else:
        regex_tokenize(data_text[:1000])
    
    for _ in range(num_runs):
        start_time = time.perf_counter()
        
        # Execute the tokenization
        if method == 'swig':
            tokens = regex_swig.simple_tokenize(data_text)
        elif method == 'fast_swig':
            tokens = regex_swig.fast_word_tokenize(data_text)
        elif method == 'char_swig':
            tokens = regex_swig.char_tokenize(data_text)
        else:
            tokens = regex_tokenize(data_text)
        
        end_time = time.perf_counter()
        total_time += (end_time - start_time)

    avg_time_ms = (total_time / num_runs) * 1000
    
    method_name = {
        'swig': 'Simple Tokenize (SWIG)',
        'fast_swig': 'Fast Word Tokenize (SWIG)',
        'char_swig': 'Character Tokenize (SWIG)',
        'regex': 'Regex (Python re.findall)'
    }.get(method, method)
    
    return {
        "algorithm": f"Tokenization - {method_name}",
        "text_size_kb": text_size_kb,
        "token_count": len(tokens) if 'tokens' in locals() else 'N/A',
        "num_runs": num_runs,
        "avg_time_ms": avg_time_ms,
    }


# --- Execution ---

if __name__ == "__main__":
    
    print("--- Tokenization Benchmark Test Runs (SWIG) ---")
    print("Benchmarking complexity is dependent on text length (N).")
    print("-" * 60)
    
    # --- Tokenization Benchmark Test 1: Moderate Text Size ---
    text_size_kb_1 = 200 # 200 KB
    runs1 = 10
    
    print(f"\n--- Test 1: Text Size {text_size_kb_1} KB ---")
    
    # Test SWIG simple tokenizer
    results1_swig = benchmark_tokenizer(text_size_kb_1, runs1, method='swig')
    print(f"Algorithm: {results1_swig['algorithm']}")
    print(f"Text Size: {results1_swig['text_size_kb']} KB")
    print(f"Approx. Tokens: {results1_swig['token_count']:,}")
    print(f"Total Runs: {results1_swig['num_runs']}")
    print(f"Average Execution Time: {results1_swig['avg_time_ms']:.4f} ms")
    
    print()
    
    # Test SWIG fast word tokenizer
    results1_fast = benchmark_tokenizer(text_size_kb_1, runs1, method='fast_swig')
    print(f"Algorithm: {results1_fast['algorithm']}")
    print(f"Average Execution Time: {results1_fast['avg_time_ms']:.4f} ms")
    
    print("-" * 60)
    
    # --- Tokenization Benchmark Test 2: Larger Text Size ---
    text_size_kb_2 = 800 # 800 KB
    runs2 = 5
    
    print(f"\n--- Test 2: Text Size {text_size_kb_2} KB ---")
    
    # Test SWIG simple tokenizer
    results2_swig = benchmark_tokenizer(text_size_kb_2, runs2, method='swig')
    print(f"Algorithm: {results2_swig['algorithm']}")
    print(f"Text Size: {results2_swig['text_size_kb']} KB")
    print(f"Approx. Tokens: {results2_swig['token_count']:,}")
    print(f"Total Runs: {results2_swig['num_runs']}")
    print(f"Average Execution Time: {results2_swig['avg_time_ms']:.4f} ms")
    
    print()
    
    # Test SWIG fast word tokenizer
    results2_fast = benchmark_tokenizer(text_size_kb_2, runs2, method='fast_swig')
    print(f"Algorithm: {results2_fast['algorithm']}")
    print(f"Average Execution Time: {results2_fast['avg_time_ms']:.4f} ms")
    
    print("-" * 60)