from youtube_transcript_api import YouTubeTranscriptApi
import argparse
import gensim 
from summarizer import Summarizer

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

#Need a minimum of 10 sentences in the transcript
def summarize_by_ratio(video_transcript):
    ratio = 0.3
    summary = gensim.summarization.summarize(video_transcript, ratio = ratio)
    return summary

def summarize_by_word_count(video_transcript):
    max_word_count = 30
    summary = gensim.summarization.summarize(video_transcript, word_count = max_word_count)
    return summary

def summarize_bert(video_transcript):
    model = Summarizer()
    return model(video_transcript)

if __name__=="__main__":
    
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--id", type = str, default = 'H4opOnCXJ28',
                help = "Video ID for YouTube video.")
    ap.add_argument("-f", "--file", type = str, default = 'summary.txt',
                help = "File to output summary to.")
    args = vars(ap.parse_args())

    video_id = args['id']
    video_transcript = get_transcript(video_id)
    summary = summarize_bert(video_transcript)
    print(summary)