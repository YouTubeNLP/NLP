import gensim
from nltk.stem import WordNetLemmatizer, SnowballStemmer
import numpy as np
import nltk
from youtube_transcript_api import YouTubeTranscriptApi
from model import lemmatize_stemming, preprocess, filename, dictionary

# load model
import joblib
lda_model = joblib.load(filename)

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