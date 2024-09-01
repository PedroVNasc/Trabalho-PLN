#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <unordered_map>
#include <vector>

#include "utf8.h"
#include "treemap.hpp"
#include "utils.hpp"

size_t levenshteinDistance(std::string word1, std::string word2);

int main() {
    using std::string;
    using std::vector;

    vector<vector<string>> raw = readLexicon("portilexicon-ud.tsv");
    vector<std::tuple<std::uint8_t, string>> encoding = readEncoding("encoding.txt");

    Treemap treemap(encoding);
    treemap.setup_tree(raw);

    string res = treemap.get_word("teste");

    std::cout << res << std::endl;

    return 0;
}

size_t levenshteinDistance(std::string word1, std::string word2) {
    size_t matrix_len = std::max(word1.length(), word2.length());
    std::vector<std::vector<int16_t>> matrix(
        matrix_len, std::vector<int16_t>(matrix_len, 0)
    );

    matrix[0][0] = word1[0] == word2[0] ? 0 : 1;
    for (int i = 1; i < matrix_len; i++) {
        matrix[0][i] = i + matrix[0][0];
        matrix[i][0] = i + matrix[0][0];
    }

    for (int i = 1; i < matrix_len; i++) {
        for (int j = 1; j < matrix_len; j++) {
            matrix[i][j] = std::min(
                matrix[i - 1][j - 1],
                std::min(matrix[i][j - 1], matrix[i - 1][j])
            );

            if (i >= word1.length() || j >= word2.length() ||
                word1[i] != word2[j])
                matrix[i][j] += 1;
        }
    }

    return matrix[matrix_len - 1][matrix_len - 1];
}