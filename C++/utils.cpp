#include "utils.hpp"
#include "utf8.h"

#include <fstream>
#include <sstream>

vector<vector<string>> readLexicon(string path) {
    std::ifstream file(path);
    string line;
    vector<vector<string>> data;

    while(getline(file, line)) {
        std::stringstream stream(line);
        string word, root, classification, features;

        stream >> word >> root >> classification >> features;
        vector<string> vec{word, root, classification, features};

        data.push_back(vec);
    }

    file.close();

    return data;
}

vector<std::tuple<std::uint8_t, string>> readEncoding(string path) {
    std::ifstream file(path);
    string line;
    vector<std::tuple<std::uint8_t, string>> encoding;

    while (std::getline(file, line)) {
        std::stringstream stream(line);
        int id;
        string character;

        stream >> id >> character;
        encoding.push_back(std::make_tuple((std::uint8_t) id, character));
    }

    return encoding;
}

void writeEncoding(string path, vector<string> chars) {
    std::ofstream file(path, std::ios::trunc);

    for (size_t i = 0; i < chars.size(); i++) {
        file << i + 1 << ' ' << chars[i] << std::endl;
    }   

    file.close();
}

std::uint8_t encodeChar(vector<std::tuple<std::uint8_t, string>> &encoding, string character) {
    for (auto t : encoding) {
        if (std::get<1>(t) == character)
            return std::get<0>(t);
    }    

    return 0;
}

string decodeChar(vector<std::tuple<std::uint8_t, string>> &encoding, std::uint8_t character) {
    for (auto t : encoding) {
        if (std::get<0>(t) == character)
            return std::get<1>(t);
    } 

    return "/";
}

void vectorizeWord(std::string word, std::vector<std::string> &characters) {
    auto it = word.begin();
    while (it != word.end()) {
        std::string c;
        utf8::append(utf8::next(it, word.end()), c);
        characters.push_back(c);
    }
}

void vectorizeWord(vector<std::tuple<std::uint8_t, string>> &encoding, 
                    string word, std::vector<std::uint8_t> &characters) {
    
    auto it = word.begin();
    while (it != word.end()) {
        std::string c;
        utf8::append(utf8::next(it, word.end()), c);

        characters.push_back(encodeChar(encoding, c));
    }   
}