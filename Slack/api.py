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
        self._basic_headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        self._basic_params = {
            'token': self.token
        }

    def get_channel_list_json(self):
        res = requests.get(Slack.constant.CHANNEL_LIST_URL, headers=self._basic_headers, params=self._basic_params)
        return res.json()['channels']

    def get_channel_id(self, channel_name):
        channel_list = json_normalize(self.get_channel_list_json())
        get_channel_id = list(channel_list.loc[channel_list['name'] == channel_name, 'id'])[0]
        return get_channel_id

    def get_all_chat_data_in_channel(self, channel_id):
        params = self._basic_params
        params['channel'] = channel_id
        res = requests.get(Slack.constant.CHANNEL_HISTORY_URL, headers=self._basic_headers, params=params)
        chat_data = json_normalize(res.json()['messages'])
        return chat_data

    def get_timestamp_of_chat_data(self, channel_id, text):
        chat_data = self.get_all_chat_data_in_channel(channel_id)
        chat_data['text'] = chat_data['text'].apply(lambda x: x.replace('\xa0', ' '))
        ts = chat_data.loc[chat_data['text'] == text, 'ts'].to_list()[0]
        return ts

    def post_message(self, channel_id, msg):
        data = self._basic_params
        data['channel'] = channel_id
        data['text'] = msg
        res = requests.post(Slack.constant.CHAT_POST_MESSAGE_URL, headers=self._basic_headers, data=data)
        return res
