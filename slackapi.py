import json
import requests
from pandas import json_normalize

SLACK_API_URL = 'https://slack.com/api'
CONVERSATIONS_URL = SLACK_API_URL + '/conversations'
CHANNEL_LIST_URL = CONVERSATIONS_URL + '.list'
CHANNEL_HISTORY_URL = CONVERSATIONS_URL + '.history'
TOKEN_FILE_NAME = './token.json'
SLACK_TOKEN = ''


def init_slack_api():
    global SLACK_TOKEN
    SLACK_TOKEN = slack_token_from_file(TOKEN_FILE_NAME)


def slack_token_from_file(token_file_name):
    with open(token_file_name, 'r') as json_file:
        slack_dict = json.load(json_file)

    return slack_dict['token']


def basic_params():
    return {
        'Content-Type': 'application/x-www-form-urlencoded',
        'token': SLACK_TOKEN
    }


def channel_list_json():
    params = basic_params()
    res = requests.get(CHANNEL_LIST_URL, params=params)
    channel_list = json_normalize(res.json()['channels'])
    return channel_list


def channel_id(channel_name):
    channel_list = channel_list_json()
    channel_id = list(channel_list.loc[channel_list['name'] == channel_name, 'id'])[0]
    return channel_id


def all_chat_data_in_channel(channel_id):
    params = basic_params()
    params['channel'] = channel_id
    res = requests.get(CHANNEL_HISTORY_URL, params=params)
    chat_data = json_normalize(res.json()['messages'])
    return chat_data


def timestamp_of_chat_data(channel_id, text):
    chat_data = all_chat_data_in_channel(channel_id)
    chat_data['text'] = chat_data['text'].apply(lambda x: x.replace('\xa0', ' '))
    ts = chat_data.loc[chat_data['text'] == text, 'ts'].to_list()[0]
    return ts