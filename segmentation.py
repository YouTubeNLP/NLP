#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 11:24:01 2020

@author: jaisi8631
"""

# import libraries
import argparse
from service.transcript.transcript_helper import get_transcript, save_file
from service.segmentation.segmentation_helper import nltk_segmentation, deepseg_segmentation, spacy_segmentation, deepseg_segmentation_finetuned

# main method
if __name__=="__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--id", type = str, default = '4ZNWYqDU948',
                help = "Video ID for YouTube video.")
    ap.add_argument("-f", "--file", type = str, default = 'transcript.txt',
                help = "File to output transcript lines to.")
    args = vars(ap.parse_args())

    video_id = args['id']
    video_transcript = get_transcript(video_id)
    
    video_segments_nltk = nltk_segmentation(video_transcript)
    video_segments_deepseg = deepseg_segmentation(video_transcript)
    # video_segments_deepseg_finetuned = deepseg_segmentation_finetuned(video_transcript)
    video_segments_spacy = spacy_segmentation(video_transcript)

    save_file('nltk', video_segments_nltk)
    save_file('deepseg', video_segments_deepseg)
    save_file('spacy', video_segments_spacy)

