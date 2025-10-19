// json_swig.cpp
#include "json_swig.h"
#include <cstdlib>
#include <ctime>

std::string generate_random_string(int length) {
    static bool seeded = false;
    if (!seeded) {
        std::srand(std::time(nullptr));
        seeded = true;
    }
    
    const char* characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    int num_chars = 62;
    
    std::string result;
    result.reserve(length);
    
    for (int i = 0; i < length; i++) {
        result += characters[std::rand() % num_chars];
    }
    
    return result;
}