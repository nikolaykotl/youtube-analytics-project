import json

import os
from googleapiclient.discovery import build

class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.title = Channel.info_channel(self.__channel_id)['snippet']['title']
        self.description = Channel.info_channel(self.__channel_id)['snippet']['description']
        self.url = f'https://www.youtube.com/channel/{self.__channel_id}'
        self.subscriber_count = Channel.info_channel(self.__channel_id)['statistics']['subscriberCount']
        self.video_count = Channel.info_channel(self.__channel_id)['statistics']['videoCount']
        self.view_count = Channel.info_channel(self.__channel_id)['statistics']['viewCount']

    def print_info(self) -> None:
        api_key: str = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        info = json.dumps(channel, indent=2, ensure_ascii=False)
        return print(f'{info}')

    @staticmethod
    def info_channel(channel_id):
        api_key: str = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel_info = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()['items'][0]
        return channel_info

    @property
    def channel_id(self):
        self.__channel_id

    @classmethod
    def get_service(cls):
        api_key: str = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def to_json(self, file):
        api_key: str = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        info = json.dumps(channel, indent=2, ensure_ascii=False)
        with open ('moscowpython.json', 'w', encoding= 'utf8') as json_file:
            json_file.write(info)

    def __str__(self):
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __gt__(self, other):
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other):
        return int(self.subscriber_count) >= int(other.subscriber_count)
