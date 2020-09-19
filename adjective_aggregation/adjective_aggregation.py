from youtube_transcript_api import YouTubeTranscriptApi
import argparse
import spacy
import stanza

# stanza.download('en')   # This downloads the English models for the neural pipeline
nlp = stanza.Pipeline(processors = 'tokenize, mwt, lemma, pos, depparse', verbose = False) # This sets up a neural pipeline in English

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

# function to get ner
def spacy_ner(document):
    nlp = spacy.load('en_core_web_lg') 
    doc = nlp(document)
    results = {ent.text : [] for ent in doc.ents}
    return results

#function to get adjectives of entities
def adjective_aggregation(video_transcript):
    doc = nlp(video_transcript)
    result = spacy_ner(video_transcript)
    for i in range(len(doc.sentences)):
        for element in doc.sentences[i].dependencies:
            first = element[0]
            relation = element[1]
            second = element[2]
            if relation == 'root':
                continue
            if first.upos == 'ADJ' and second.text in result:
                result[second.text].append(first.text)
            elif second.upos == 'ADJ' and first.text in result:
                result[first.text].append(second.text)
    result = {key : value for key, value in result.items() if value}
    return result

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
    ap.add_argument("-f", "--file", type = str, default = 'adj_agg.txt',
                help = "File to output adjective aggregation results to.")
    args = vars(ap.parse_args())

    video_id = args['id']
    video_transcript = get_transcript(video_id)
    video_transcript = video_transcript.lower()
    result = adjective_aggregation(video_transcript)
    
    print(result)