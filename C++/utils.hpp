#ifndef REGRA_UTILS
#define REGRA_UTILS

#include <vector>
#include <string>
#include <tuple>

using std::string;
using std::vector;

vector<vector<string>> readLexicon(string path);
vector<std::tuple<std::uint8_t, string>> readEncoding(string path);

void writeEncoding(string path, vector<string>);

std::uint8_t encodeChar(vector<std::tuple<std::uint8_t, string>> &encoding, string character);
string decodeChar(vector<std::tuple<std::uint8_t, string>> &encoding, std::uint8_t character);

void vectorizeWord(string word, std::vector<string> &characters);
void vectorizeWord(vector<std::tuple<std::uint8_t, string>> &enconding, 
                    string word, std::vector<std::uint8_t> &characters);

#endif