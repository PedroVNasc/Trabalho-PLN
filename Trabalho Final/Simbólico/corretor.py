import csv
from typing import TypedDict
import requests
from tqdm import tqdm


class WordData(TypedDict):
    raiz: set[str]
    grammar_class: set[str]
    morphemes: set[str]


class Node():
    def __init__(self, head: str, data: dict | None = None, prox: dict[str, 'Node'] | None = None):
        self.head = head
        self.data = data
        self.prox = {} if prox is None else prox


class ReGra():
    def __init__(self):
        self.nodes: dict[str, Node] = {}

    def dive(self, current_node: Node, word: str, depth: int):
        # Palavra não existe ou palavra encontrada
        if depth >= len(word) or word[depth] not in current_node.prox.keys():
            return current_node

        # Continua a recursão
        return self.dive(current_node.prox[word[depth]], word, depth + 1)

    def get_parent(self, word: str) -> Node | None:
        if word[0] not in self.nodes.keys():
            return None

        return self.dive(self.nodes[word[0]], word, 1)

    def __getitem__(self, word: str):
        if word[0] not in self.nodes.keys():
            return None

        node = self.dive(self.nodes[word[0]], word, 1)

        if node.head != word:
            return None

        return node.data

    def __setitem__(self, idx: str, value: WordData):
        parent = self.get_parent(idx)

        # Se o conjunto está vazio ou uma letra base não existe
        if parent is None:
            if len(idx) == 1:
                self.nodes[idx] = Node(head=idx, data=value)
                return

            parent = Node(head=idx[0])
            self.nodes[idx[0]] = parent

            for i in range(1, len(idx) - 1):
                parent.prox[idx[i]] = Node(head=idx[:i + 1])
                parent = parent.prox[idx[i]]

            parent.prox[idx[-1]] = Node(head=idx, data=value)
            return

        # Se a palavra existe, atualiza os dados
        if parent.head == idx:
            if parent.data is None:
                parent.data = value

            else:
                parent.data['raiz'] = parent.data['raiz'].union(value['raiz'])
                parent.data['grammar_class'] = parent.data['grammar_class'].union(
                    value['grammar_class'])
                parent.data['morphemes'] = parent.data['morphemes'].union(
                    value['morphemes'])

            return

        # Se a palavra não existe, mas é filha de uma que existe
        # cria o nó dela
        if len(parent.head) + 1 == len(idx):
            parent.prox[idx[-1]] = Node(head=idx, data=value)

        # Se a palavra não existe, e não é filha de uma que existe
        # cria um caminho de nós até ela
        else:
            for i in range(len(parent.head), len(idx) - 1):
                parent.prox[idx[i]] = Node(head=idx[:i + 1])
                parent = parent.prox[idx[i]]

            parent.prox[idx[-1]] = Node(head=idx, data=value)

    def __repr__(self) -> str:
        string = ''
        for node in self.nodes.values():
            string += self.build_tree(node)

        return string

    def build_tree(self, current: Node, depth: int = 0):
        string = f"{'-' * depth} {current.head}{' OK' if current.data is not None else ''}\n"

        for node in current.prox.values():
            string += self.build_tree(node, depth + 1)

        return string

    def get_children(self, current: Node, max_depth: int = 10, depth: int = 0) -> list[str]:
        if depth >= max_depth:
            return []

        children = []

        for node in current.prox.values():
            if node.data is not None:
                children.append(node.head)

            children += self.get_children(node,
                                          max_depth=max_depth, depth=depth + 1)

        return children


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


class WSException(Exception):
    'Webservice Exception'

    def __init__(self, errordata):
        "errordata is a dict returned by the webservice with details about the error"
        super().__init__(self)
        assert isinstance(errordata, dict)
        self.message = errordata["message"]
        # see https://json-rpc.readthedocs.io/en/latest/exceptions.html for more info
        # about JSON-RPC error codes
        if -32099 <= errordata["code"] <= -32000:  # Server Error
            if errordata["data"]["type"] == "WebServiceException":
                self.message += f": {errordata['data']['message']}"
            else:
                self.message += f": {errordata['data']!r}"

    def __str__(self):
        return self.message


class Corretor():
    def __init__(self, dictionary_path: str, key: str = '', symbols: dict = {}):
        self.dictionary = self.__load_dicionary__(dictionary_path)
        self.LXPARSER_WS_API_KEY = key
        self.symbol_corvertion = symbols

    def setup_key(self, key: str):
        self.LXPARSER_WS_API_KEY = key

    def setup_symbols(self, symbols: dict):
        self.symbol_corvertion = symbols

    def __lxparse__(self, text: str):
        '''
        Arguments
            text: a string with a maximum of 2000 characters, Portuguese text, with
                the input to be processed
            format: either 'parentheses', 'table' or 'JSON'

        Returns a string or JSON object with the output according to specification in
        https://portulanclarin.net/workbench/lx-parser/

        Raises a WSException if an error occurs.
        '''

        request_data = {
            'method': 'parse',
            'jsonrpc': '2.0',
            'id': 0,
            'params': {
                'text': text,
                'format': 'table',
                'key': self.LXPARSER_WS_API_KEY,
            },
        }

        request = requests.post(
            'https://portulanclarin.net/workbench/lx-parser/api/', json=request_data)
        response_data = request.json()

        if "error" in response_data:
            raise WSException(response_data["error"])

        result = response_data["result"].split('\n')

        # Converte para uma lista de tuplas
        lx_parsed = []
        for r in result:
            r = r.split('\t')
            r[1] = r[1].replace(')', '').split('(')[-1].replace('*', '')

            if len(r) > 1 and r[1] != 'PNT':
                lx_parsed.append((r[0], self.symbol_corvertion[r[1]]))

        return lx_parsed

    def __load_dicionary__(self, path: str):
        dictionary = ReGra()

        with open(path) as dic:
            rd = csv.reader(dic, delimiter='\t', quotechar='"')
            qtd_lines = sum(1 for _ in rd)
            dic.seek(0)

            progress = tqdm(total=qtd_lines, desc="Carregando dicionário")

            for row in rd:
                word = row[0]
                raiz = [row[1]]
                grammar_class = [row[2]]
                morphemes = [x for x in row[3].split('|') if x]

                dictionary[word] = WordData(
                    raiz=set(raiz), grammar_class=set(grammar_class), morphemes=set(morphemes))

                progress.update(1)

            progress.close()

        return dictionary

    def __aligning__(self, dict_parsed, lx_parsed):
        if len(dict_parsed) != len(lx_parsed):
            print(
                f"Lengths don't match: {len(dict_parsed)} != {len(lx_parsed)}")
            return []

        aligned_classes = []

        for i in range(len(dict_parsed)):
            if dict_parsed[i][0].lower() != lx_parsed[i][0].lower():
                print(
                    f"Words don't match: {dict_parsed[i][0]} != {lx_parsed[i][0]}")
                return []

            word = lx_parsed[i][0]
            classes = dict_parsed[i][1].intersection(set(lx_parsed[i][1]))

            if len(classes) == 0:
                # Para o caso de ser um nome
                if 'Unknown' in dict_parsed[i][1] and 'NOUN' in lx_parsed[i][1]:
                    classes = set(lx_parsed[i][1])

                else:
                    classes = set(['ERROR', lx_parsed[i][1][0]])

            aligned_classes.append([word, classes])

        return aligned_classes

    def __parsing__(self, phrase: str):
        phrase = clean_text(phrase)

        result = {}
        for word in phrase.split():
            result[word] = self.dictionary[word]

            if result[word] is None:
                result[word] = {'raiz': set(['Unknown']), 'grammar_class': set(
                    ['Unknown']), 'morphemes': set(['Unknown'])}

        # print(result.items())
        return [[x[0], x[1]['grammar_class']] for x in result.items()]

    def __get_corrections__(self, word: str, grammar_class: str):
        word = clean_text(word)
        p = self.dictionary.get_parent(word)

        # Procura paralavras com 2 até dois caracteres a mais ou a menos
        if len(p.head) > 2:
            p = self.dictionary.get_parent(p.head[:-2])

        children = self.dictionary.get_children(p, max_depth=4.0)

        corrections = []
        for c in children:
            if grammar_class == 'ANY' or grammar_class in self.dictionary[c]['grammar_class']:
                corrections.append(c)

        corrections.sort(key=lambda x: levenshtein_distance(word, x))
        return corrections[:10]

    def corrigir_texto(self, texto: str):
        dict_parsed = self.__parsing__(texto)
        lx_parsed = self.__lxparse__(texto)
        aligned_classes = self.__aligning__(dict_parsed, lx_parsed)

        corrections = {}
        for word in aligned_classes:
            if 'ERROR' in word[1]:
                corrections[word[0]] = self.__get_corrections__(
                    word[0], list(word[1] - {'ERROR'})[0])

                if corrections[word[0]] == []:
                    corrections[word[0]] = self.__get_corrections__(
                        word[0], 'ANY')

                print(list(word[1] - {'ERROR'})[0])
                print(corrections[word[0]])

            else:
                corrections[word[0]] = None

        return corrections
