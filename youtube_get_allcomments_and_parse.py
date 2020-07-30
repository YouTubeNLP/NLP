import googleapiclient.discovery

API_KEY = "AIzaSyDEyoZhTj3wh0B3r3evEmIxI-4g2Aa9-dE"
service = googleapiclient.discovery.build('youtube', 'v3', developerKey=API_KEY)

all_comments=list()
def build_initial_request(video_id):
    request=service.commentThreads().list(
                part= "snippet",
                videoId= video_id,
                )
    return request

def parse_page(result):
    for item in result['items']:
        print(item['snippet']['topLevelComment']['snippet']['authorDisplayName'])
        print('---')
        comment_text =item['snippet']['topLevelComment']['snippet']['textDisplay']
        print(comment_text)
        #print(item['snippet']['topLevelComment']['snippet']['textOriginal'])
        all_comments.append(comment_text)
        print('====================')

def parse_result(result):
    while result.get('nextPageToken', False):
        parse_page(result)
        request=service.commentThreads().list(
            part= "snippet",
            videoId="bQxqIKTO2Ck",
            pageToken=result.get('nextPageToken')
        )
        result = request.execute()

def main():
    request = build_initial_request("_0JZbsJdFIU")
    result= request.execute()
    parse_result(result)

    print(all_comments)
    print(len(all_comments))

main()



