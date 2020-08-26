import argparse
import os
import json
import pandas as pd
import googleapiclient.discovery

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

    with open(file_name, 'w') as f:
        json.dump(response, f)

    return comment_df


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--id", type = str, default = 'H4opOnCXJ28',
                help = "Video ID for YouTube video.")
    ap.add_argument("-o", "--output", type = str, default = 'comments.json',
                help = "File to output response json results to.")
    ap.add_argument("-n", "--number", type = int, default = 20,
                help = "Number of comments to scrape")
    args = vars(ap.parse_args())

    video_id = args['id']
    max_num = args['number']
    save_path = args['output']


    response_df = comment_scraper(video_id= video_id,max_comments=max_num,file_name=save_path)

    print(response_df)

    


#for item in data.get('items'):
#    print('Comment : ',item.get('snippet').get('topLevelComment').get('snippet')['textDisplay'])
#    print('Likes : ', item.get('snippet').get('topLevelComment').get('snippet')['likeCount'])
#    print('Replies : ',item.get('snippet')['totalReplyCount'])
#    print('-----------------------------------------------------------------------------------')


