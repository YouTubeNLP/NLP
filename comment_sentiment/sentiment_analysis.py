import argparse
import os
import json
import pandas as pd
import googleapiclient.discovery
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()

#Function to classify a sentence into one of the 3 sentiments : Positive, Negative or Neutral
def sentiment_scores(sentence):
	snt = analyser.polarity_scores(sentence)
	if snt['compound'] >= 0.05:
		return 'Positive'
	elif snt['compound'] <= -0.05:
		return 'Negative'
	else:
		return 'Neutral'

#Function takes in JSON response from Youtube V3 api and extracts comment text,likes and replies 
def json_parser(json_response):
	comments = []
	likes = []
	replies = []
	for item in json_response.get('items'):
		comments.append(item.get('snippet').get('topLevelComment').get('snippet')['textOriginal'])
		likes.append(item.get('snippet').get('topLevelComment').get('snippet')['likeCount'])    
		replies.append(item.get('snippet')['totalReplyCount'])

	assert len(comments) == len(likes) == len(replies),'Length not matching'

	df = pd.DataFrame()
	df['Comments'] = comments
	df['Likes'] = likes
	df['Replies'] = replies


	return df

#Function to scrape comments, their number likes and number replies using YouTube V3 API - NEEDS DEVELOPER_KEY 
def comment_scraper(video_id,max_comments,file_name):
	# Disable OAuthlib's HTTPS verification when running locally.
	# *DO NOT* leave this option enabled in production.
	os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

	api_service_name = "youtube"
	api_version = "v3"
	DEVELOPER_KEY = "AIzaSyDEyoZhTj3wh0B3r3evEmIxI-4g2Aa9-dE"

	youtube = googleapiclient.discovery.build(
		api_service_name, api_version, developerKey = DEVELOPER_KEY)

	request = youtube.commentThreads().list(
		part="snippet,replies",
		maxResults=max_comments,
		order="relevance",
		videoId=video_id
	)
	response = request.execute()

	comment_df = json_parser(response)
	comment_df['Sentiment'] = comment_df['Comments'].apply(lambda x : sentiment_scores(x))

	with open(file_name, 'w') as f:
		json.dump(response, f)

	return comment_df


if __name__ == "__main__":
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--id", type = str, default = 'H4opOnCXJ28',
				help = "Video ID for YouTube video.")
	ap.add_argument("-o", "--output", type = str, default = 'comment_sentiment.txt',
				help = "File to output response json results to.")
	ap.add_argument("-n", "--number", type = int, default = 10,
				help = "Number of comments to scrape")
	args = vars(ap.parse_args())

	video_id = args['id']
	max_num = args['number']
	save_path = args['output']


	comment_df = comment_scraper(video_id= video_id,max_comments=max_num,file_name=save_path)

	#print(comment_df)

	neutral_comms = comment_df[comment_df['Sentiment'] == 'Neutral']['Comments']
	negative_comms = comment_df[comment_df['Sentiment'] == 'Negative']['Comments']
	positive_comments = comment_df[comment_df['Sentiment'] == 'Positive']['Comments']

	final_json = dict({"positive" : positive_comments.tolist(), "negative" : negative_comms.tolist(), "neutral" : neutral_comms.tolist() })
	
	#final_json = json.dumps(final_json,indent=4)
	print(json.dumps(final_json,indent=4)) #The final json file which contains comments categorized into json/dict with positive,negative and neutral keys

	with open(save_path, "w") as f:
		json.dump(final_json,f,indent=4)