import streamlit as st
import csv
from llama_cpp import Llama
from corretor import Corretor, WordData, ReGra, lxparse_symbols


@st.cache_resource
def load_dictionary():
    print('Loading dictionary...')
    dictionary = ReGra()

    with open('./portilexicon-ud.tsv') as dic:
        rd = csv.reader(dic, delimiter='\t', quotechar='"')

        for row in rd:
            word = row[0]
            raiz = [row[1]]
            tag = [row[2]]
            features = [x for x in row[3].split('|') if x]

            dictionary[word] = WordData(
                raiz=set(raiz), tag=set(tag), features=set(features))

    return dictionary


@st.cache_resource
def load_model():
    llm = Llama(
        model_path='./sabia-7b.Q4_0.gguf',
        seed=42,
        chat_format="llama-2",
    )

    return llm


@st.cache_data
def rewrite(question: str, context: str | None = None, full_output=False, seed=42):
    llm = load_model()

    context = [
        'Você é um assistente de linguagem natural especializado em correção gramatical. Sua tarefa é corrigir os erros gramaticais das perguntas abaixo mantendo o texto o mais próximo possível do original.',
        'Q: Onde que a gente pode compraar ingressos pro show?',
        'A: Onde que a gente pode comprar ingressos pro show?',
        'Q: Por que que o céu é azul?',
        'A: Por que o céu é azul?',
        'Q: Humn... Algu erradu. Pão naum eh gostosu',
        'A: Humn.. Algo errado. Pão não é gostoso',
        'Q: Voce viu a nova loja que abriru na esquina?',
        'A: Você viu a nova loja que abriu na esquina?',
    ] if context is None else context

    context.append('Q: ' + question)
    context.append('A:')

    input_text = '\n'.join(context)

    output = llm(
        input_text,
        max_tokens=32,
        stop=["Q:"],
        # seed=seed,
        echo=True,
    )

    return output['choices'][0]['text'].split(':')[-1] if not full_output else output


dictionary = load_dictionary()

corretor = Corretor(dictionary=dictionary,
                    key=st.secrets["lxparser_key"], symbols=lxparse_symbols)

if 'text_area_value' not in st.session_state:
    st.session_state.text_area_value = ''


def update_text_area_value():
    st.session_state.text_area_value = st.session_state.frase


# UI
st.title('Mecanolinguistas')
text = st.text_area('Input', key='frase',
                    value=st.session_state.text_area_value,
                    on_change=update_text_area_value)

left_button, right_button, _ = st.columns([0.2, 0.25, 1])

result = ''

with left_button:
    if st.button('Corrigir'):
        corrections = corretor.corrigir_texto(text)

        result = {}
        for key, value in corrections.items():
            if value is not None:
                print(key, value)
                result[key] = value

with right_button:
    if st.button('Reescrever'):
        result = rewrite(question=text)

st.write(result)
