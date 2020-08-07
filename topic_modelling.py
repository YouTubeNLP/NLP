from service.topic_modelling.topic_modelling_helper import lemmatize_stemming, preprocess
from service.transcript.transcript_helper import get_transcript
from model import filename, dictionary

# load model
import joblib
lda_model = joblib.load(filename)

# Testing ABC News LDA model on video transcript
VIDEO_ID = '7AxO7Cg29mU'

bow_vector = dictionary.doc2bow(preprocess(get_transcript(VIDEO_ID)))

for index, score in sorted(lda_model[bow_vector], key=lambda tup: -1 * tup[1]):
    print("Score: {}\t Topic: {}".format(score, lda_model.print_topic(index, 5)))