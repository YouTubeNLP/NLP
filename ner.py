#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 18:40:12 2020

@author: jaisi8631
"""

# import libraries
import argparse
from service.transcript.transcript_helper import get_transcript, save_file
from service.ner.ner_helper import spacy_ner, nerd_ner

# main method
if __name__=="__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--id", type = str, default = '4ZNWYqDU948',
                help = "Video ID for YouTube video.")
    ap.add_argument("-f", "--file", type = str, default = 'transcript.txt',
                help = "File to output NER results to.")
    args = vars(ap.parse_args())

    video_id = args['id']
    video_transcript = get_transcript(video_id)
    
    ner_spacy = spacy_ner(video_transcript)
    ner_nerd = nerd_ner(video_transcript)