import json
import requests
from pandas import json_normalize

import Slack.constant


def slack_token_from_file(token_file_name):
    with open(token_file_name, 'r') as json_file:
        slack_dict = json.load(json_file)

    return slack_dict['token']


class SlackAPI:
    def __init__(self):
        self.token = slack_token_from_file(Slack.constant.TOKEN_FILE_NAME)
        self._basic_params = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'token': self.token
        }

    def channel_list_json(self):
        params = self._basic_params
        res = requests.get(Slack.constant.CHANNEL_LIST_URL, params=params)
        channel_list = json_normalize(res.json()['channels'])
        return channel_list

    def channel_id(self, channel_name):
        channel_list = self.channel_list_json()
        channel_id = list(channel_list.loc[channel_list['name'] == channel_name, 'id'])[0]
        return channel_id

    def all_chat_data_in_channel(self, channel_id):
        params = self._basic_params
        params['channel'] = channel_id
        res = requests.get(Slack.constant.CHANNEL_HISTORY_URL, params=params)
        chat_data = json_normalize(res.json()['messages'])
        return chat_data

    def timestamp_of_chat_data(self, channel_id, text):
        chat_data = self.all_chat_data_in_channel(channel_id)
        chat_data['text'] = chat_data['text'].apply(lambda x: x.replace('\xa0', ' '))
        ts = chat_data.loc[chat_data['text'] == text, 'ts'].to_list()[0]
        return ts
