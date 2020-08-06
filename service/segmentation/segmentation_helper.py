# import libraries
from youtube_transcript_api import YouTubeTranscriptApi
from deepsegment import finetune, train, generate_data, DeepSegment
import spacy
import en_core_web_sm
import nltk

# function to get lines
def get_segments(video_id):
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
            
        return segments

    except:
          print("An exception occurred")
          return(None)


# function to segment sentences using nltk library
def nltk_segmentation(document):
    nltk.download('punkt')
    seg_transcript = nltk.sent_tokenize(document)
    return seg_transcript


# function to segment sentences using classic deep segment model
def deepseg_segmentation(document):
    segmenter = DeepSegment('en')
    seg_transcript = segmenter.segment(document)
    return seg_transcript


# INCOMPLETE - REQUIRES MANUAL DATA LABELLING
# function to segment sentences using finetuned deep segment
def deepseg_segmentation_finetuned(document):    
    # download sample data
    lines = []
    videos = ['4ZNWYqDU948', 'Oixpc0o86y8', '0a5PiMygzAM', 
              'Cv4hsmfgRuI', 'HFntXYyDJtg']
    
    for v in videos:
        t = get_segments(v)
        lines = lines + t
    # the list 'lines' should have segmented sentences as each member
    # to do so, we must manually  modify the lines list
    
    # generate sample data
    batch = int(0.5 * len(lines))
    x, y = generate_data(lines[:batch])
    vx, vy = generate_data(lines[batch:])
    
    # finetune and segment
    finetune('en', x, y, vx, vy, name = 'YoutubeSeg')
    segmenter = DeepSegment('en', checkpoint_name = 'YoutubeSeg')

    seg_transcript = segmenter.segment_long(sent = document)
    return seg_transcript 


# function to segment sentences using nltk library
def spacy_segmentation(document):
    nlp = en_core_web_sm.load()
    doc = nlp(document)
    seg_transcript = []
    for sent in doc.sents:
        seg_transcript.append(sent.text)
    return seg_transcript