# YouTubeNLP - NLP Team
Owned by the NLP Team.


### Requirements:
* youtube_transcript_api
* nltk
* argparse
* deepsegment
* spacy
* en_core_web_sm
* nerd

### File Descriptions + Execution Instructions:
* segmentation.py: script for sentence segmentation.
``` 
python segmentation.py -i <youtube-video-id> -f <output-file-name-without-txt-extension>
``` 
* ner.py: script for named entity recognition.
``` 
python ner.py -i <youtube-video-id>
``` 
