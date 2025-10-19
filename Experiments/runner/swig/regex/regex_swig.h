// regex_swig.h
#ifndef REGEX_SWIG_H
#define REGEX_SWIG_H

#include <string>
#include <vector>

// Simple tokenizer that splits on whitespace and punctuation
std::vector<std::string> simple_tokenize(const std::string& text);

// Fast word tokenizer - extracts only words (alphanumeric sequences)
std::vector<std::string> fast_word_tokenize(const std::string& text);

// Character-level tokenizer with punctuation handling
std::vector<std::string> char_tokenize(const std::string& text);

#endif // REGEX_SWIG_H