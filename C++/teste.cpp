#include <iostream>
#include <string>
#include <vector>
#include "utf8.h"  // Include utf8cpp library

int main() {
    std::string utf8_str = u8"你好, 世界!";
    std::vector<std::string> utf8_chars;

    auto it = utf8_str.begin();
    while (it != utf8_str.end()) {
        std::string utf8_char;
        utf8::append(utf8::next(it, utf8_str.end()), std::back_inserter(utf8_char));
        utf8_chars.push_back(utf8_char);
    }

    // Output the UTF-8 characters
    for (const auto& ch : utf8_chars) {
        std::cout << ch << std::endl;
    }

    return 0;
}

