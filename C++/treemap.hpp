#ifndef TREEMAP_REGRA_TEST
#define TREEMAP_REGRA_TEST

#include <map>
#include <string>
#include <unordered_map>
#include <vector>

#include "utils.hpp"

using std::string;
using std::vector;
using std::uint8_t;

// struct node {
//     string value;
//     std::unordered_map<string, node> next;
// };

struct encoded_node {
    uint8_t value;
    std::map<uint8_t, encoded_node> next;
};

class Treemap {
    std::map<uint8_t, encoded_node> root;
    vector<std::tuple<uint8_t, string>> encoding;

    void search_dive(
        std::map<uint8_t, encoded_node> &map, const vector<uint8_t> &word,
        vector<uint8_t> &result, int index
    );

    void insert_dive(
        std::map<uint8_t, encoded_node> &map, vector<uint8_t> &word, int index
    );

    vector<string> vectorize_word(const std::string word);

    uint8_t encode_char(const string c);
    string decode_char(const uint8_t c);

    vector<uint8_t> encode_word(string &word);
    string decode_word(vector<uint8_t> &decodeWord);

  public:
    Treemap(const vector<std::tuple<uint8_t, string>> &encoding);

    void insert_word(string &word);

    string get_word(string word);

    void setup_tree(const vector<vector<string>> &data);
};

#endif