import nltk
from typing import List
import sys
import re

def download_nltk_resources():
    resources = {
        'punkt': 'tokenizers/punkt',
        'wordnet': 'corpora/wordnet', 
        'stopwords': 'corpora/stopwords',
        'averaged_perceptron_tagger': 'taggers/averaged_perceptron_tagger'
    }
    
    for resource, path in resources.items():
        try:
            nltk.data.find(path)
        except LookupError:
            print(f"Downloading {resource}...")
            nltk.download(resource, quiet=True)

download_nltk_resources()

def simple_tokenize(text: str) -> List[str]:
    text = re.sub(r'[^\w\s]', ' ', text)
    return [word.strip() for word in text.split() if word.strip()]

def tokenize(text: str) -> List[str]:
    try:
        return nltk.word_tokenize(text)
    except LookupError:
        print("Warning: Using simple tokenizer as fallback")
        return simple_tokenize(text)

def lemmatize(tokens: List[str]) -> List[str]:
    lemmatizer = nltk.WordNetLemmatizer()
    return [lemmatizer.lemmatize(token) for token in tokens]

def remove_stopwords(tokens: List[str], stop_words: set) -> List[str]:
    return [token for token in tokens if token.lower() not in stop_words]

def preprocess_text(text: str) -> List[str]:
    tokens = tokenize(text)
    tokens = lemmatize(tokens)
    stop_words = set(nltk.corpus.stopwords.words('english'))
    tokens = remove_stopwords(tokens, stop_words)
    return tokens