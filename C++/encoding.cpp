#include <set>
#include <iostream>
#include <string>
#include <vector>

#include "utils.hpp"

int main() {
    using std::string;
    using std::vector;

    vector<vector<string>> data = readLexicon("portilexicon-ud.tsv");
    std::set<string> unique_chars;

    for (auto line : data) {
        vector<string> chars;

        vectorizeWord(line[0], chars);
        for (auto c : chars) {
            unique_chars.insert(c);
        }
    }

    vector<string> vec(unique_chars.begin(), unique_chars.end());
    writeEncoding("encoding.txt", vec);

    return 0;
}