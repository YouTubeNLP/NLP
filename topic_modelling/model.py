import pandas as pd
import gensim
from nltk.stem import WordNetLemmatizer, SnowballStemmer
import numpy as np
np.random.seed(2018)
import nltk
from youtube_transcript_api import YouTubeTranscriptApi

# Preprocessing for ABC News Dataset
data = pd.read_csv('abcnews-date-text.csv', error_bad_lines=False);
data_text = data[['headline_text']]
data_text['index'] = data_text.index
documents = data_text


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

processed_docs = documents['headline_text'].map(preprocess)

dictionary = gensim.corpora.Dictionary(processed_docs)
count = 0

dictionary.filter_extremes(no_below=15, no_above=0.5, keep_n=100000)
bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]

# LDA with BOW
lda_model = gensim.models.LdaModel(bow_corpus, num_topics=10, id2word=dictionary)
# for idx, topic in lda_model.print_topics(-1):
#     print('Topic: {} \nWords: {}'.format(idx, topic))

# from gensim import corpora, models
# tfidf = models.TfidfModel(bow_corpus)
# corpus_tfidf = tfidf[bow_corpus]
# from pprint import pprint
# for doc in corpus_tfidf:
#     pprint(doc)
#     break

# LDA with TF-IDF
# lda_model_tfidf = gensim.models.LdaMulticore(corpus_tfidf, num_topics=10, id2word=dictionary, passes=2, workers=4)
# for idx, topic in lda_model_tfidf.print_topics(-1):
#     print('Topic: {} Word: {}'.format(idx, topic))

# Persisting the model
from tempfile import mkdtemp
savedir = mkdtemp()
import os
filename = os.path.join(savedir, 'ldamodel.joblib')

import joblib
joblib.dump(lda_model, filename)

print('Model trained and saved successfully')




