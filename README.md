# YouTubeNLP - NLP Team
Owned by the NLP Team.

### File Descriptions + Execution Instructions:
* segmentation.py: script for sentence segmentation.
``` 
python segmentation.py -i <youtube-video-id> -f <output-file-name-without-txt-extension>
``` 
* ner.py: script for named entity recognition.
``` 
python ner.py -i <youtube-video-id>
``` 


## To Do list : ##

Phase 1:

- [ ] Aggregate sentiment analysis 
- [x] Sentiment analysis sentences 
- [x] Most engaged comments - measure using likes & replies 
- [ ] Emotion analysis score - torchmoji and GPT3
- [ ] Named entity recognition from video - Add scripts using BERT and GPT3
- [ ] NER for targed Entity 
- [ ] LDA for Topic Modelling, also provide faster alternatives to LDA: compact BERT model + GPT3
- [x] Word Cloud 

Phase 2: 

- [ ] Adjective Aggregation: Run NER, aggregated adjectives using POS tagging for each sentence named entity appears in. -> Coref resolution might be necessary to get good results, especially for comments
- [ ] Recommendation follower-> Give the social researcher the ability to specifiy a depth and branching factor (use @shahjaidev 's script (version that persists session when making scraping requests): https://github.com/shahjaidev/NLP_Radicalization_detection/blob/master/smart_autoplay_sequence_%20session.py 

