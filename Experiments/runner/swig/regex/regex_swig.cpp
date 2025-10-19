// regex_swig.cpp
#include "regex_swig.h"
#include <cctype>
#include <sstream>

// Helper function to check if character is alphanumeric
inline bool is_alnum(char c) {
    return (c >= '0' && c <= '9') || 
           (c >= 'A' && c <= 'Z') || 
           (c >= 'a' && c <= 'z');
}

// Helper function to check if character is whitespace
inline bool is_whitespace(char c) {
    return c == ' ' || c == '\t' || c == '\n' || c == '\r';
}

// Helper function to check if character is punctuation
inline bool is_punctuation(char c) {
    return (c >= '!' && c <= '/') || 
           (c >= ':' && c <= '@') || 
           (c >= '[' && c <= '`') || 
           (c >= '{' && c <= '~');
}

std::vector<std::string> simple_tokenize(const std::string& text) {
    std::vector<std::string> tokens;
    size_t length = text.length();
    size_t start = 0;
    bool in_word = false;
    
    for (size_t i = 0; i < length; i++) {
        char c = text[i];
        
        // Check if alphanumeric or apostrophe (for contractions)
        if (is_alnum(c) || c == '\'') {
            if (!in_word) {
                start = i;
                in_word = true;
            }
        } else {
            if (in_word) {
                // End of word
                tokens.push_back(text.substr(start, i - start));
                in_word = false;
            }
            
            // Handle whitespace and punctuation
            if (is_whitespace(c)) {
                // Optionally add whitespace token (commented out for performance)
                // tokens.push_back(text.substr(i, 1));
            } else if (is_punctuation(c)) {
                tokens.push_back(text.substr(i, 1));
            }
        }
    }
    
    // Handle last word if text ends with alphanumeric
    if (in_word) {
        tokens.push_back(text.substr(start, length - start));
    }
    
    return tokens;
}

std::vector<std::string> fast_word_tokenize(const std::string& text) {
    std::vector<std::string> tokens;
    size_t length = text.length();
    size_t start = 0;
    bool in_word = false;
    
    for (size_t i = 0; i < length; i++) {
        char c = text[i];
        
        if (is_alnum(c)) {
            if (!in_word) {
                start = i;
                in_word = true;
            }
        } else {
            if (in_word) {
                tokens.push_back(text.substr(start, i - start));
                in_word = false;
            }
        }
    }
    
    // Handle last word
    if (in_word) {
        tokens.push_back(text.substr(start, length - start));
    }
    
    return tokens;
}

std::vector<std::string> char_tokenize(const std::string& text) {
    std::vector<std::string> tokens;
    size_t length = text.length();
    
    if (length == 0) {
        return tokens;
    }
    
    size_t start = 0;
    bool in_word = false;
    bool in_punct = false;
    bool in_space = false;
    
    for (size_t i = 0; i < length; i++) {
        char c = text[i];
        
        if (is_alnum(c) || c == '\'') {
            if (!in_word) {
                // Flush previous token if any
                if (in_punct || in_space) {
                    tokens.push_back(text.substr(start, i - start));
                }
                start = i;
                in_word = true;
                in_punct = false;
                in_space = false;
            }
        } else if (is_whitespace(c)) {
            if (!in_space) {
                // Flush previous token
                if (in_word || in_punct) {
                    tokens.push_back(text.substr(start, i - start));
                }
                start = i;
                in_space = true;
                in_word = false;
                in_punct = false;
            }
        } else if (is_punctuation(c)) {
            if (!in_punct) {
                // Flush previous token
                if (in_word || in_space) {
                    tokens.push_back(text.substr(start, i - start));
                }
                start = i;
                in_punct = true;
                in_word = false;
                in_space = false;
            }
        }
    }
    
    // Flush last token
    if (in_word || in_punct || in_space) {
        tokens.push_back(text.substr(start, length - start));
    }
    
    return tokens;
}