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

lemmatizer = WordNetLemmatizer()
stemmer = SnowballStemmer("english")

def lemmatize_stemming(text):
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

# Testing ABC News LDA model on video transcript
VIDEO_ID = '7AxO7Cg29mU'

def retrieve_transcript(video_id):
    output = YouTubeTranscriptApi.get_transcript(video_id)
    segments = []
    for e in output:
        line = e['text']
        line = line.replace('\n', '')
        line = line.replace('>', '')
        line = line.replace('--', '')
        line = line.replace('♪', '')
        segments.append(line)

    transcript = " ".join(segments)
    return transcript

bow_vector = dictionary.doc2bow(preprocess(retrieve_transcript(VIDEO_ID)))

for index, score in sorted(lda_model[bow_vector], key=lambda tup: -1 * tup[1]):
    print("Score: {}\t Topic: {}".format(score, lda_model.print_topic(index, 5)))

