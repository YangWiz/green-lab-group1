import time
import random
import re
from regex_cy import regex_tokenize_cy, simple_tokenize_cy, fast_word_tokenize_cy

# --- Regular Expression Tokenization Implementation ---

# Complex pattern to simulate a "heavy" tokenization load, capturing:
# 1. Words (sequences of letters/numbers/apostrophes)
# 2. Whitespace
# 3. Punctuation (commas, periods, etc.)
# 4. URLs (simple pattern)
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
    # Using re.findall is a clean way to get all non-overlapping matches
    return pattern.findall(text)


# --- Tokenization Benchmarking Function ---

def benchmark_tokenizer(text_size_kb, num_runs=5):
    """
    Benchmarks the Cython-optimized tokenization process.
    
    Args:
        text_size_kb (int): The target size of the input text in kilobytes (KB).
        num_runs (int): The number of times to run the tokenization for averaging.
        
    Returns:
        dict: Results including average time.
    """
    total_time = 0
    
    # 1. Generate the test data (a large string of random characters)
    # 1 KB = 1024 bytes. We use a base string to make the regex meaningful.
    base_corpus = "The quick brown fox jumps over the lazy dog's fence. " * 10
    
    # Create the large text by repeating and adding some variation (punctuation/spaces)
    target_size_bytes = text_size_kb * 1024
    
    # Ensure the string is at least the target size, adding noise for realistic tokens
    data_text = base_corpus * (target_size_bytes // len(base_corpus) + 1)
    data_text = data_text[:target_size_bytes] 
    
    # Add random URLs and numbers to the text for complexity
    def add_complexity(text):
        return text.replace("fox", "12345.67 fox") + " https://example.com/page?id=1"
        
    data_text = add_complexity(data_text)
    
    # Warm-up run with a small fraction of the text
    regex_tokenize_cy(data_text[:1000], TOKENIZATION_PATTERN)
    
    for _ in range(num_runs):
        start_time = time.perf_counter()
        # Execute the tokenization (Cython version)
        tokens = regex_tokenize_cy(data_text, TOKENIZATION_PATTERN)
        end_time = time.perf_counter()
        
        total_time += (end_time - start_time)

    avg_time_ms = (total_time / num_runs) * 1000
    
    return {
        "algorithm": "Regex Heavy Tokenization (Cython)",
        "text_size_kb": text_size_kb,
        "token_count": len(tokens) if 'tokens' in locals() else 'N/A', # Report final token count
        "num_runs": num_runs,
        "avg_time_ms": avg_time_ms,
    }


# --- Execution ---

if __name__ == "__main__":
    
    print("--- Regular Expression Heavy Tokenization Benchmark Test Runs ---")
    print("Benchmarking complexity is dependent on text length (N) and regex pattern complexity.")
    print("-" * 60)
    
    # --- Tokenization Benchmark Test 1: Moderate Text Size ---
    text_size_kb_1 = 200 # 200 KB
    runs1 = 10
    
    print(f"\n--- Test 1: Text Size {text_size_kb_1} KB ---")
    results1 = benchmark_tokenizer(text_size_kb_1, runs1)
    
    print(f"Algorithm: {results1['algorithm']}")
    print(f"Text Size: {results1['text_size_kb']} KB")
    print(f"Approx. Tokens: {results1['token_count']:,}")
    print(f"Total Runs: {results1['num_runs']}")
    print(f"Average Execution Time: {results1['avg_time_ms']:.4f} ms")
    
    print("-" * 60)
    
    # --- Tokenization Benchmark Test 2: Larger Text Size ---
    text_size_kb_2 = 800 # 800 KB
    runs2 = 5
    
    print(f"\n--- Test 2: Text Size {text_size_kb_2} KB ---")
    results2 = benchmark_tokenizer(text_size_kb_2, runs2)
    
    print(f"Algorithm: {results2['algorithm']}")
    print(f"Text Size: {results2['text_size_kb']} KB")
    print(f"Approx. Tokens: {results2['token_count']:,}")
    print(f"Total Runs: {results2['num_runs']}")
    print(f"Average Execution Time: {results2['avg_time_ms']:.4f} ms")
    
    print("-" * 60)