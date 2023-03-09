import os
import re

import nltk
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from pymorphy2 import MorphAnalyzer

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('snowball_data')
nltk.download('perluniprops')
nltk.download('universal_tagset')
nltk.download('stopwords')
nltk.download('nonbreaking_prefixes')
nltk.download('wordnet')
STOPWORDS = stopwords.words('english')


def get_tokens(s: str) -> list:
    tokenizer = RegexpTokenizer('[A-Za-z]+')
    clean_words = tokenizer.tokenize(s)
    clean_words = [word.lower() for word in clean_words if word != '']
    clean_words = [word for word in clean_words if word not in STOPWORDS]
    return clean_words


def get_lemmas(tokens: set) -> dict:
    pymorphy2_analyzer = MorphAnalyzer()
    lemmas = {}
    for token in tokens:
        if re.match(r'[A-Za-z]', token):
            lemma = pymorphy2_analyzer.parse(token)[0].normal_form
            if lemmas.get(lemma):
                lemmas[lemma].append(token)
            else:
                lemmas[lemma] = [token]
    return lemmas


if __name__ == '__main__':
    filename_template = '../data/site_%s.html'
    tokens = set()
    for i in range(1, 101):
        site_filename = os.path.abspath('../data/site_%s.html')
        with open(filename_template % i, 'r') as f:
            text = f.read()
            soup = BeautifulSoup(text, 'html.parser')
            text = ' '.join(soup.stripped_strings)
            tokens.update(get_tokens(text))

    lemmas = get_lemmas(tokens)

    with open('../tokens.txt', 'w') as f:
        f.write('\n'.join(tokens))

    with open('../lemmas.txt', 'w') as f:
        for lemma, tokens in lemmas.items():
            f.write(f'{lemma} ' + ' '.join(tokens) + '\n')
