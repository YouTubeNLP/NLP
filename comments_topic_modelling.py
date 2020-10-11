from apiclient.discovery import build 
import re 
import nltk 
import numpy as np 
import pandas as pd
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
import spacy
from nltk.corpus import stopwords
nltk.download('stopwords')

def get_videos(query):
    videos_list = []
    videos = youtube.search().list(part='id',
                            q=query,
                            order = 'relevance',
                            type='video',
                            maxResults=50).execute()
  
    for i in range(50):
    #storing the results in a list
    #5o is the maxResults value
        videos_list.append(videos['items'][i]['id']['videoId'])
  
    i = 0 #number of pages to navigate through
  #the following lines is to navigate through multiple pages
    while 'nextPageToken' in videos and i < 20:
        videos = youtube.search().list(part='id',
                            q=query,
                            order = 'relevance', 
                            type='video',
                            maxResults=50,
                            pageToken = videos['nextPageToken']).execute()
    
        for j in range(50):
            try:
          #stroing the results in a list
          #for error handling in case of index is out of range
                videos_list.append(videos['items'][j]['id']['videoId'])
            except:
                break
        i = i+1 
    return videos_list

def get_comments(videosId_list):
    comment_list = []  
    for i in videosId_list:
        try:
            comments = youtube.commentThreads().list(
                        part = 'snippet',
                        videoId = str(i),
                        maxResults = 100, 
                        order = 'relevance', 
                        textFormat = 'plainText',
                        ).execute()
        except:
            continue
    
        for j in range(99):
            try:
                comment_list.append(comments['items'][j]['snippet']['topLevelComment']['snippet']['textDisplay'])
            except:
                continue
    return comment_list

def prepare_data(data): 
    data = [re.sub('\S*@\S*\s?', '', sent) for sent in data]
    data = [re.sub('\s+', ' ', sent) for sent in data]
    data = [re.sub("\'", "", sent) for sent in data]
    return data

def store_in_file(comments):
    with open('youtube_comments.txt', 'w') as f:
        for comment in comments:
            f.write("%s\n" % comment)  

def tokenization(sentences):
    for sent in sentences:
        yield(gensim.utils.simple_preprocess(str(sent), deacc=True))

def remove_stopwords(texts):
    stop_words = stopwords.words('english')
    stop_words.extend(['hello', '.com', 'also','this', 'there', 'really' , 'still'])
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]

def make_bigrams(texts, data_words):
    bigram = gensim.models.Phrases(data_words, min_count=1, threshold=10)
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    return [bigram_mod[doc] for doc in texts]

def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    texts_out = []
    nlp = spacy.load('en', disable=['parser', 'ner'])
    for sent in texts:
        doc = nlp(" ".join(sent)) 
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out

def word2id(data_lemmatized):
    id2word = corpora.Dictionary(data_lemmatized)
    texts = data_lemmatized
    corpus = [id2word.doc2bow(text) for text in texts]
    return corpus, id2word
  
def build_LDA(topics_num, corpus, id2word):
    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                           id2word=id2word,
                                           num_topics=topics_num, 
                                           random_state=100,
                                           update_every=1,
                                           chunksize=100,
                                           passes=10,
                                           alpha='auto',
                                           per_word_topics=True)
  
    print(lda_model.print_topics())

if __name__== "__main__":
    api_key = "YOUR_API_KEY"
    youtube = build('youtube', 'v3', developerKey=api_key)
    videos_list = get_videos('politics')
    comments_list = get_comments(videos_list)
    store_in_file(comments_list)
    comments = prepare_data(comments_list)
    data_tokenized = list(sent_to_words(comments))
    data_words_nostops = remove_stopwords(data_tokenized)
    data_words_bigrams = make_bigrams(data_words_nostops,data_tokenized)
    data_lemmatized = lemmatization(data_words_bigrams, allowed_postags=['NOUN', 'ADJ','VERB', 'ADV'])
    corpus, id2word = word2id(data_lemmatized)
    build_LDA(5,corpus,id2word)