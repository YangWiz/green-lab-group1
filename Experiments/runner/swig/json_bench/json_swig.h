// json_swig.h
#ifndef JSON_SWIG_H
#define JSON_SWIG_H

#include <string>

// Generate a random alphanumeric string
std::string generate_random_string(int length);

// Note: Actual JSON encoding/decoding should still use Python's json module
// as it's already highly optimized in C. This SWIG module only provides
// helper functions for data generation.

#endif // JSON_SWIG_H