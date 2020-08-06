from youtube_transcript_api import YouTubeTranscriptApi

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

# function to save transcript
def save_file(document_name, transcript):
    file_name = args['file'] + '-' + document_name +'.txt'
    f = open(file_name, 'w+')
    for line in transcript:
        f.write(line + '\n')
    f.close()