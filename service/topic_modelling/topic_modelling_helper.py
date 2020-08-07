import nltk
import gensim
from nltk.stem import WordNetLemmatizer, SnowballStemmer

def lemmatize_stemming(text):
    lemmatizer = WordNetLemmatizer()
    stemmer = SnowballStemmer("english")
    token = lemmatizer.lemmatize(text, pos='v')
    stem_token = stemmer.stem(token)
    return stem_token

def preprocess(text):
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(lemmatize_stemming(token))
    return result