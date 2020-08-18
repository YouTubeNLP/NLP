#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 18:40:12 2020

@author: jaisi8631
"""

# import libraries
from youtube_transcript_api import YouTubeTranscriptApi
import argparse
import spacy
from spacy import displacy
from nerd import ner
      

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
      

# function to apply ner using spacy library
def spacy_ner(document):
    nlp = spacy.load('en_core_web_lg') 
    doc = nlp(document)
    results = [(ent.text, ent.label_) for ent in doc.ents]
    return results


# function to apply ner using nerd library
def nerd_ner(document):
    doc = ner.name(document, language='en_core_web_lg')
    results = [(ent.text, ent.label_) for ent in doc]
    return results


# function to save transcript
def save_file(document_name, transcript):
    file_name = args['file'] + '-' + document_name +'.txt'
    f = open(file_name, 'w+')
    for line in transcript:
        f.write(line + '\n')
    f.close()

# main method
if __name__=="__main__":
    
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--id", type = str, default = 'H4opOnCXJ28',
                help = "Video ID for YouTube video.")
    ap.add_argument("-f", "--file", type = str, default = 'ner.txt',
                help = "File to output NER results to.")
    args = vars(ap.parse_args())

    video_id = args['id']
    video_transcript = get_transcript(video_id)
    video_transcript = video_transcript.lower()
    
    ner_spacy = spacy_ner(video_transcript)
    ner_nerd = nerd_ner(video_transcript)