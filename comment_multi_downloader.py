import requests
import json
import datetime
import re

URL = 'https://www.googleapis.com/youtube/v3/'
# ここにAPI KEYを入力
API_KEY = 'ここにAPI KEYを入力'
# ここにVideo IDを入力
VIDEO_ID = 'ypc4LHr_0e0'
MAX_RESULT = 999
json_open = open('youtube_url/url.json','r', encoding='utf-8')
json_load = json.load(json_open)

file_name = "comment_list/" + VIDEO_ID + ".csv"
file = open(file_name, "w", encoding='utf-8')

def print_video_comment(no, video_id, next_page_token):
    params = {
        'key': API_KEY,
        'part': 'snippet',
        'videoId': video_id,
        'order': 'relevance',
        'textFormat': 'plaintext',
        'maxResults': MAX_RESULT,
    }
    if next_page_token is not None:
        params['pageToken'] = next_page_token
    response = requests.get(URL + 'commentThreads', params=params)
    resource = response.json()


    for comment_info in resource['items']:
        # コメント
        text = comment_info['snippet']['topLevelComment']['snippet']['textDisplay']
        # グッド数
        like_cnt = comment_info['snippet']['topLevelComment']['snippet']['likeCount']
        # 返信数
        reply_cnt = comment_info['snippet']['totalReplyCount']
        # ユーザー名
        user_name = comment_info['snippet']['topLevelComment']['snippet']['authorDisplayName']
        # Id
        parentId = comment_info['snippet']['topLevelComment']['id']
        file.write('{:0=4}\t{}\t{}\t{}\t{}\n'.format(no, text.replace('\n', ' '), like_cnt, user_name, reply_cnt))
        if reply_cnt > 0:
            cno = 1
            print_video_reply(no, cno, video_id, next_page_token, parentId)
        no = no + 1

    if 'nextPageToken' in resource:
        print_video_comment(no, video_id, resource["nextPageToken"])


def print_video_reply(no, cno, video_id, next_page_token, id):
    params = {
        'key': API_KEY,
        'part': 'snippet',
        'videoId': video_id,
        'textFormat': 'plaintext',
        'maxResults': 50,
        'parentId': id,
    }

    if next_page_token is not None:
        params['pageToken'] = next_page_token
    response = requests.get(URL + 'comments', params=params)
    resource = response.json()

    for comment_info in resource['items']:
        # コメント
        text = comment_info['snippet']['textDisplay']
        # グッド数
        like_cnt = comment_info['snippet']['likeCount']
        # ユーザー名
        user_name = comment_info['snippet']['authorDisplayName']

        file.write('{:0=4}-{:0=3}\t{}\t{}\t{}\n'.format(no, cno,text.replace('\n', ' '), like_cnt, user_name))
        cno = cno + 1

    if 'nextPageToken' in resource:
        print_video_reply(no, cno, video_id, resource["nextPageToken"], id)


# 表配信コメントを全取得する
for video_list in json_load["items"]:
    
    print(video_list)
    video_id = video_list['id']['videoId']
    title = video_list['snippet']['title']
    date = str(video_list['snippet']['publishedAt'])
    date_str = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
    date_num = str(date_str.strftime('%Y%m%d%H%M%S'))
    no = 1
    print('[Exec DL Comment.] {}, {}, {}'.format(video_id, title, date_num))
    file_name = "comment_list/" + date_num + "_" + re.sub(r'[\\/:*?"<>|]+','',title) + ".csv"
    print(file_name)
    file = open(file_name, "w", encoding='utf-8')
        print_video_comment(no, video_id, None)
