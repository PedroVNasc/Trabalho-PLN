#include "treemap.hpp"
#include "utf8.h"

void insertWord(
    std::unordered_map<std::string, node> &map, std::vector<std::string> word,
    int index
) {
    if (index >= word.size()) return;

    if (map.find(word[index]) == map.end()) {
        // std::cout << "Adding " << word[index] << std::endl;

        node new_node;
        std::unordered_map<std::string, node> new_map;

        new_node.next = new_map;
        new_node.value = word[index];

        map[word[index]] = new_node;
    }

    insertWord(map[word[index]].next, word, index + 1);
}

void vectorizeWord(std::string word, std::vector<std::string> &characters) {
    auto it = word.begin();
    while (it != word.end()) {
        std::string c;
        utf8::append(utf8::next(it, word.end()), c);
        characters.push_back(c);
    }
}
