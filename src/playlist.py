from googleapiclient.discovery import build

import os
import isodate
import datetime

class PlayList():

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        playlist_response = build('youtube', 'v3', developerKey=os.getenv('API_KEY')).playlists().list(part='snippet,contentDetails',id=self.playlist_id).execute()

        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"
        self.title = playlist_response['items'][0]['snippet']['title']

    @property
    def total_duration(self):
        playlist_videos = build('youtube', 'v3', developerKey=os.getenv('API_KEY')).playlistItems().list(playlistId=self.playlist_id,
                                               part='contentDetails',
                                               maxResults=50,
                                               ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        video_response = build('youtube', 'v3', developerKey=os.getenv('API_KEY')).videos().list(part='contentDetails,statistics',
                                       id=','.join(video_ids)
                                       ).execute()

        sec = 0.0
        for video in video_response['items']:
         # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            sec += duration.total_seconds()
        time = datetime.timedelta(seconds = sec)
        return time

    def __str__(self, time):
            return f'{time}'


    def show_best_video(self):
        playlist_videos = build('youtube', 'v3', developerKey=os.getenv('API_KEY')).playlistItems().list(playlistId=self.playlist_id,
                                               part='contentDetails',
                                               maxResults=50,
                                               ).execute()


        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        video_response = build('youtube', 'v3', developerKey=os.getenv('API_KEY')).videos().list(part='contentDetails,statistics',
                                       id=','.join(video_ids)
                                       ).execute()

        like = 0
        count = 0

        for video in video_response:
           likeCount = int(video_response['items'][count]['statistics']['likeCount'])

           if likeCount > like:
               like = likeCount
               url = "https://youtu.be/"+ video_response['items'][count]['id']
           count += 1
        return url



