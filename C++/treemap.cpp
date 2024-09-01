#include <algorithm>

#include "treemap.hpp"
#include "utf8.h"

void Treemap::search_dive(
    std::map<uint8_t, encoded_node> &map, const vector<uint8_t> &word,
    vector<uint8_t> &result, int index = 0
) {
    if (index >= word.size()) return;

    if (map.find(word[index]) == map.end()) {
        result.push_back(0);
    }

    else {
        result.push_back(map[word[index]].value);
    }
};

void Treemap::insert_dive(
    std::map<uint8_t, encoded_node> &map, vector<uint8_t> &word, int index = 0
) {
    if (index >= word.size()) return;

    if (map.find(word[index]) == map.end()) {
        // std::cout << "Adding " << word[index] << std::endl;

        encoded_node new_node;
        std::map<uint8_t, encoded_node> new_map;

        new_node.next = new_map;
        new_node.value = word[index];

        map[word[index]] = new_node;
    }

    this->insert_dive(map[word[index]].next, word, index + 1);
}

vector<string> Treemap::vectorize_word(const string word) {
    vector<string> characters;
    auto it = word.begin();
    while (it != word.end()) {
        std::string c;
        utf8::append(utf8::next(it, word.end()), c);
        characters.push_back(c);
    }

    return characters;
};

uint8_t Treemap::encode_char(const string c) {
    for (auto t : this->encoding) {
        if (std::get<1>(t) == c) return std::get<0>(t);
    }

    return 0;
};

string Treemap::decode_char(const uint8_t c) {
    for (auto t : this->encoding) {
        if (std::get<0>(t) == c) return std::get<1>(t);
    }

    return "\\";
};

vector<uint8_t> Treemap::encode_word(string &word) {
    vector<string> characters = this->vectorize_word(word);
    vector<uint8_t> encoded_word;
    for (auto c : characters) {
        encoded_word.push_back(this->encode_char(c));
    }

    return encoded_word;
}

string Treemap::decode_word(vector<uint8_t> &encoded_word) {
    string word;

    for (auto e : encoded_word) {
        word += this->decode_char(e);
    }

    return word;
}

Treemap::Treemap(const vector<std::tuple<uint8_t, string>> &encoding) {
    this->encoding = encoding;
};

void Treemap::insert_word(string &word) {
    vector<uint8_t> encoded_word;
    for (auto c : vectorize_word(word)) {
        encoded_word.push_back(encode_char(c));
    }

    this->insert_dive(this->root, encoded_word);
};

string Treemap::get_word(string word) {
    string result;

    vector<uint8_t> encoded_word = encode_word(word);
    vector<uint8_t> result_encoded = encode_word(word);

    this->search_dive(this->root, encoded_word, result_encoded);

    for (auto c : result_encoded) {
        result += this->decode_char(c);
    }

    return result;
};

void Treemap::setup_tree(const vector<vector<string>> &data) {
    for (auto line : data) {
        this->insert_word(line[0]);
    }
};