# json_cy.pyx
# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False

cimport cython
import json
import random
import string
import time

# Note: Python's json module is already in C, so we focus on optimizing data generation
# and provide a streamlined interface

@cython.boundscheck(False)
@cython.wraparound(False)
def generate_random_string_cy(int length):
    """Cython-optimized random string generation."""
    cdef int i
    cdef list chars = []
    cdef str characters = string.ascii_letters + string.digits
    cdef int num_chars = len(characters)
    
    for i in range(length):
        chars.append(characters[random.randint(0, num_chars - 1)])
    
    return ''.join(chars)


def create_complex_data_cy(int num_records):
    """
    Cython-optimized creation of complex, nested Python dictionary/list structure for JSON testing.
    
    The structure simulates records with various data types (string, int, float, list, dict).
    """
    cdef int i, j, num_tags, num_history
    cdef list data_list = []
    cdef dict record
    cdef list tags, history
    cdef double current_time = time.time()
    
    for i in range(num_records):
        # Generate tags
        num_tags = random.randint(2, 5)
        tags = [generate_random_string_cy(5) for _ in range(num_tags)]
        
        # Generate history
        num_history = random.randint(1, 3)
        history = [
            {
                "timestamp": current_time - random.randint(100, 10000),
                "amount": round(random.uniform(-100, 100), 2)
            }
            for _ in range(num_history)
        ]
        
        record = {
            "id": i,
            "uuid": generate_random_string_cy(32),
            "isActive": random.choice([True, False]),
            "balance": round(random.uniform(10.0, 50000.0), 2),
            "tags": tags,
            "profile": {
                "age": random.randint(18, 65),
                "city": generate_random_string_cy(10),
                "isVerified": random.choice([True, False])
            },
            "history": history
        }
        data_list.append(record)
    
    return {
        "metadata": {
            "count": num_records,
            "timestamp": current_time
        },
        "records": data_list
    }


def json_dumps_cy(obj):
    """
    Wrapper around json.dumps - uses Python's C-optimized implementation.
    """
    return json.dumps(obj)


def json_loads_cy(str s):
    """
    Wrapper around json.loads - uses Python's C-optimized implementation.
    """
    return json.loads(s)