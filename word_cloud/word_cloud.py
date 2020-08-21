#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import libraries
from youtube_transcript_api import YouTubeTranscriptApi
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import json
import argparse


# function to get transcripts
def get_transcript(video_id):
    try:
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

    except:
          print("An exception occurred")
          return(None)


#function to get the word cloud
def word_cloud(document):
    stop_words = stopwords.words('english')
    tokenizer = RegexpTokenizer(r'\w+')
    word_tokens = list(tokenizer.tokenize(document))
    final_tokens = [w for w in word_tokens if not w in stop_words]
    most_frequent = Counter(final_tokens).most_common(40)
    return most_frequent


# function to save transcript
def save_file(document_name, transcript):
    file_name = args['file'] + '-' + document_name +'.txt'
    f = open(file_name, 'w+')
    for line in transcript:
        f.write(line + '\n')
    f.close()

if __name__=="__main__":
    
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--id", type = str, default = 'H4opOnCXJ28',
                help = "Video ID for YouTube video.")
    ap.add_argument("-f", "--file", type = str, default = 'word_cloud.txt',
                help = "File to output word cloud results to.")
    args = vars(ap.parse_args())

    video_id = args['id']
    video_transcript = get_transcript(video_id)
    video_transcript = video_transcript.lower()
    cloud=word_cloud(video_transcript)