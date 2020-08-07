import googleapiclient.discovery

API_KEY = "AIzaSyDEyoZhTj3wh0B3r3evEmIxI-4g2Aa9-dE"
service = googleapiclient.discovery.build('youtube', 'v3', developerKey=API_KEY)

def build_initial_request(video_id):
    request=service.commentThreads().list(
                part= "snippet",
                videoId= video_id,
                )
    return request

def parse_page(result, all_comments):
    for item in result['items']:
        print(item['snippet']['topLevelComment']['snippet']['authorDisplayName'])
        print('---')
        comment_text =item['snippet']['topLevelComment']['snippet']['textDisplay']
        print(comment_text)
        #print(item['snippet']['topLevelComment']['snippet']['textOriginal'])
        all_comments.append(comment_text)
        print('====================')

def parse_result(result, all_comments):
    while result.get('nextPageToken', False):
        parse_page(result, all_comments)
        request=service.commentThreads().list(
            part= "snippet",
            videoId="bQxqIKTO2Ck",
            pageToken=result.get('nextPageToken')
        )
        result = request.execute()