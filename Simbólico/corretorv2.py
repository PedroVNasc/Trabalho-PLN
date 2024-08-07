from typing import TypedDict


class WordData(TypedDict):
    root: set[str]
    tag: set[str]
    features: set[str]


class Node():
    def __init__(self, prox: list[str] = [], prev: list[str] = []):
        self.prox = prox
        self.prev = prev


class TreeDict():
    def __init__(self):
        self.first_layer: dict[str, Node] = {}
        self.middle_layers: list[dict[str, Node]] = []
        self.last_layer: dict[str, Node] = {}
        
        self.words: dict[str, WordData] = {}

    def __getitem__(self, word: str):
        if word in self.words.keys():
            return self.words[word]
        else:
            None

    def __setitem__(self, idx: str, value: WordData):
        # First layer and last layer must be set manually
        if idx[0] not in self.first_layer: # Creates new node
            self.first_layer[idx[0]] = Node(prox=[idx[1]])
            
        elif idx[1] not in self.first_layer[idx[0]].prox: # Adds new transition
            self.first_layer[idx[0]].prox.append(idx[1])
        
        # Intertwine the middle layers
        for i in range(1, len(idx) - 1):
            if idx[i] not in self.middle_layers[i - 1]:
                self.middle_layers[i - 1][idx[i]] = Node(prox=[idx[i + 1]], prev=[idx[i - 1]])
                
            else: 
                if idx[i + 1] not in self.middle_layers[i - 1][idx[i]].prox:
                    self.middle_layers[i - 1][idx[i]].prox.append(idx[i + 1])
                    
                if idx[i - 1] not in self.middle_layers[i - 1][idx[i]].prev:
                    self.middle_layers[i - 1][idx[i]].prev.append(idx[i - 1])
        
        # Last layer
        if idx[-1] not in self.last_layer:
            self.last_layer[idx[-1]] = Node(prev=[idx[-2]])
            
        elif idx[-2] not in self.last_layer[idx[-1]].prev:
            self.last_layer[idx[-1]].prev.append(idx[-2])
            
        # Add the word to the hashmap or updates it
        if idx not in self.words:
            self.words[idx] = value
        else:
            self.words[idx].root = self.words[idx].root.union(value.root)
            self.words[idx].tag = self.words[idx].tag.union(value.tag)
            self.words[idx].features = self.words[idx].features.union(value.features)
                        
    # def __repr__(self) -> str:
    #     string = ''
    #     for node in self.nodes.values():
    #         string += self.build_tree(node)

    #     return string

    # def build_tree(self, current: Node, depth: int = 0):
    #     string = f"{'-' * depth} {current.head}{' OK' if current.data is not None else ''}\n"

    #     for node in current.prox.values():
    #         string += self.build_tree(node, depth + 1)

    #     return string

    # def get_children(self, current: Node, max_depth: int = 10, depth: int = 0) -> list[str]:
    #     if depth >= max_depth:
    #         return []

    #     children = []

    #     for node in current.prox.values():
    #         if node.data is not None:
    #             children.append(node.head)

    #         children += self.get_children(node,
    #                                       max_depth=max_depth, depth=depth + 1)

    #     return children


def levenshtein_distance(word1, word2):
    len1 = len(word1)
    len2 = len(word2)

    matrix_len = max(len1, len2) + 1
    matrix = [[0 for _ in range(matrix_len)] for _ in range(matrix_len)]

    for i in range(matrix_len):
        matrix[i][0] = i
        matrix[0][i] = i

    for i in range(1, matrix_len):
        for j in range(1, matrix_len):
            matrix[i][j] = min(matrix[i - 1][j], matrix[i]
                               [j - 1], matrix[i - 1][j - 1])

            if i > len1:
                matrix[i][j] += 1
            elif j > len2:
                matrix[i][j] += 1
            elif word1[i - 1] != word2[j - 1]:
                matrix[i][j] += 1

    return matrix[matrix_len - 1][matrix_len - 1]


def clean_text(text: str):
    return text.lower().replace(',', '').replace('.', '').replace(
        '!', '').replace('?', '').replace(';', '')


# class WSException(Exception):
#     'Webservice Exception'

#     def __init__(self, errordata):
#         "errordata is a dict returned by the webservice with details about the error"
#         super().__init__(self)
#         assert isinstance(errordata, dict)
#         self.message = errordata["message"]
#         # see https://json-rpc.readthedocs.io/en/latest/exceptions.html for more info
#         # about JSON-RPC error codes
#         if -32099 <= errordata["code"] <= -32000:  # Server Error
#             if errordata["data"]["type"] == "WebServiceException":
#                 self.message += f": {errordata['data']['message']}"
#             else:
#                 self.message += f": {errordata['data']!r}"

#     def __str__(self):
#         return self.message


# class Corretor():
#     def __init__(self, dictionary_path: str, key: str = '', symbols: dict = {}):
#         self.dictionary = self.__load_dicionary__(dictionary_path)
#         self.LXPARSER_WS_API_KEY = key
#         self.symbol_convertion = symbols

#     def setup_key(self, key: str):
#         self.LXPARSER_WS_API_KEY = key

#     def setup_symbols(self, symbols: dict):
#         self.symbol_convertion = symbols

#     def __lxparse__(self, text: str):
#         '''
#         Arguments
#             text: a string with a maximum of 2000 characters, Portuguese text, with
#                 the input to be processed
#             format: either 'parentheses', 'table' or 'JSON'

#         Returns a string or JSON object with the output according to specification in
#         https://portulanclarin.net/workbench/lx-parser/

#         Raises a WSException if an error occurs.
#         '''

#         request_data = {
#             'method': 'parse',
#             'jsonrpc': '2.0',
#             'id': 0,
#             'params': {
#                 'text': text,
#                 'format': 'parentheses',
#                 'key': self.LXPARSER_WS_API_KEY,
#             },
#         }

#         request = requests.post(
#             'https://portulanclarin.net/workbench/lx-parser/api/', json=request_data)
#         response_data = request.json()

#         if "error" in response_data:
#             raise WSException(response_data["error"])

#         tree = Tree.fromstring(response_data["result"])

#         # Converte para uma lista de tuplas
#         word_pos = tree.pos()

#         result = [[x[0], self.symbol_convertion[x[1]]] for x in word_pos if x[1] in self.symbol_convertion]
        
#         lx_parsed = []
#         for x in result:
#             if x[0][-1] == '_':
#                 x[0] = x[0][:-1]

#             if x[0].isalpha():
#                 lx_parsed.append(x)

#         return lx_parsed, tree

#     def __load_dicionary__(self, path: str):
#         dictionary = ReGra()

#         with open(path) as dic:
#             rd = csv.reader(dic, delimiter='\t', quotechar='"')
#             qtd_lines = sum(1 for _ in rd)
#             dic.seek(0)

#             progress = tqdm(total=qtd_lines, desc="Carregando dicionário")

#             for row in rd:
#                 word = row[0]
#                 raiz = [row[1]]
#                 tag = [row[2]]
#                 features = [x for x in row[3].split('|') if x]

#                 dictionary[word] = WordData(
#                     raiz=set(raiz), tag=set(tag), features=set(features))

#                 progress.update(1)

#             progress.close()

#         return dictionary

#     def __aligning__(self, dict_parsed, lx_parsed):
#         if len(dict_parsed) != len(lx_parsed):
#             print(
#                 f"Lengths don't match: {len(dict_parsed)} != {len(lx_parsed)}")
#             return []

#         aligned_classes = []

#         for i in range(len(dict_parsed)):
#             if dict_parsed[i][0].lower() != lx_parsed[i][0].lower():
#                 print(
#                     f"Words don't match: {dict_parsed[i][0]} != {lx_parsed[i][0]}")
#                 return []

#             word = lx_parsed[i][0]
#             classes = dict_parsed[i][1].intersection(set(lx_parsed[i][1]))

#             if len(classes) == 0:
#                 if 'Unknown' in dict_parsed[i][1]:
#                     classes = set(['ERROR', lx_parsed[i][1][0]])

#                 else:
#                     classes = dict_parsed[i][1]

#             aligned_classes.append([word, classes])

#         return aligned_classes

#     def __parsing__(self, phrase: str):
#         result = []
#         for word in phrase.split():
#             entry = self.dictionary[word]

#             if entry is None:
#                 entry = {'raiz': set(['Unknown']), 'tag': set(
#                     ['Unknown']), 'features': set(['Unknown'])}
                
#             result.append((word, entry))

#         return [[x[0], x[1]['tag']] for x in result]

#     def __get_corrections__(self, word: str, tag: str):
#         word = clean_text(word)
#         p = self.dictionary.get_parent(word)

#         # Procura paralavras com 2 até dois caracteres a mais ou a menos
#         if len(p.head) > 2:
#             p = self.dictionary.get_parent(p.head[:-2])

#         max_depth = max(len(word) - len(p.head) + 2, 4.0)

#         children = self.dictionary.get_children(p, max_depth=max_depth)

#         corrections = []
#         for c in children:
#             if tag == 'ANY' or tag in self.dictionary[c]['tag']:
#                 corrections.append(c)

#         corrections.sort(key=lambda x: levenshtein_distance(word, x))

#         return corrections[:10]

#     def __extract_details__(self, details: set[str]):
#         details_dict = {}

#         for x in details:
#             if x == '_':
#                 continue

#             char, value = x.split('=')
#             if char in details_dict:
#                 details_dict[char].append(value)
#             else:
#                 details_dict[char] = [value]

#         return details_dict

#     def __prune_corrections__(self, corrections, tree: Tree):
#         # Extrai os detalhes
#         details = set()
#         for x in tree.leaves():
#             d = self.dictionary[x]

#             if d is not None:
#                 details = details.union(d['features'])

#         # Condensa as palavras que têm a mesma raiz
#         same_root = {}
#         for x in corrections:
#             roots = self.dictionary[x]['raiz']

#             for root in roots:
#                 if root in same_root:
#                     same_root[root].append(x)
#                 else:
#                     same_root[root] = [x]

#         # Seleciona as palavras que possuem maior similaridade com o resto da frase
#         characteristics = self.__extract_details__(details)
#         pruned_corrections = []
#         for _, similar_words in same_root.items():
#             if len(similar_words) == 1:
#                 pruned_corrections.append(similar_words[0])
#                 continue

#             score = {}
#             best_combination = 0
#             for word in similar_words:
#                 score[word] = 0
#                 word_details = self.__extract_details__(
#                     self.dictionary[word]['features'])

#                 for char, values in word_details.items():
#                     if values[0] in characteristics[char]:
#                         score[word] += 1

#                 if best_combination < score[word]:
#                     best_combination = score[word]

#             for word in similar_words:
#                 if score[word] == best_combination:
#                     pruned_corrections.append(word)

#         return pruned_corrections

#     def corrigir_texto(self, texto: str):
#         lx_parsed, tree = self.__lxparse__(texto)
#         dict_parsed = self.__parsing__(' '.join([x[0].lower() for x in lx_parsed]))
#         aligned_classes = self.__aligning__(dict_parsed, lx_parsed)

#         corrections = {}
#         for word in aligned_classes:
#             if 'ERROR' in word[1]:
#                 subs = self.__get_corrections__(
#                     word[0], list(word[1] - {'ERROR'})[0])

#                 if subs == []:
#                     subs = self.__get_corrections__(word[0], 'ANY')

#                 corrections[word[0]] = self.__prune_corrections__(
#                     subs, tree)

#             else:
#                 corrections[word[0]] = None

#         return corrections
