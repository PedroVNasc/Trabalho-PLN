#include "utf8.h"
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <unordered_map>
#include <vector>

#include "treemap.hpp"

size_t levenshteinDistance(std::string word1, std::string word2);

int main() {
    std::ifstream file("portilexicon-ud.tsv");
    std::string str, segment;
    std::vector<std::vector<std::string>> raw;

    // int i = 0;
    while (std::getline(file, str)) {
        std::stringstream stream(str);
        std::vector<std::string> seglist;

        while (std::getline(stream, segment, '\t')) {
            seglist.push_back(segment);
        }

        // i++;
        raw.push_back(seglist);
    }

    file.close();

    std::unordered_map<std::string, node> map;
    for (std::vector<std::string> data : raw) {
        std::vector<std::string> word;

        vectorizeWord(data[0], word);
        insertWord(map, word, 0);
    }

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

// std::unordered_map<std::string, node> createMap() {
// }