#ifndef TREEMAP_REGRA_TEST
#define TREEMAP_REGRA_TEST

#include <string>
#include <unordered_map>
#include <vector>

struct node {
    std::string value;
    std::unordered_map<std::string, node> next;
    // std::unordered_map<wchar_t, node> prev;
};

void insertWord(
    std::unordered_map<std::string, node> &map, std::vector<std::string> word,
    int index
);

void vectorizeWord(std::string word, std::vector<std::string> &characters);

#endif