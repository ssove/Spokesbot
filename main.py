import json
import requests
from pandas import json_normalize

if __name__ == '__main__':
    json_slack_path = "./token.json"
    with open(json_slack_path, 'r') as json_file:
        slack_dict = json.load(json_file)

    slack_token = slack_dict['token']

    channel_name = 'test'
    url = 'https://slack.com/api/conversations.list'
    params = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'token': slack_token
    }

    res = requests.get(url, params=params)

    channel_list = json_normalize(res.json()['channels'])
    channel_id = list(channel_list.loc[channel_list['name'] == channel_name, 'id'])[0]

    print(f'''
    Channel name: {channel_name}
    Channel id: {channel_id}
    ''')

    text = 'api test'
    url = 'https://slack.com/api/conversations.history'

    params = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'token': slack_token,
        'channel': channel_id
    }

    res = requests.get(url, params=params)
    chat_data = json_normalize(res.json()['messages'])
    chat_data['text'] = chat_data['text'].apply(lambda x: x.replace('\xa0',' '))
    ts = chat_data.loc[chat_data['text'] == text, 'ts'].to_list()[0]

    print(f'''
    Contents: {text}
    ts: {ts}
    ''')

    message = f'''
    TEST MESSAGE
    '''

    data = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'token': slack_token,
        'channel': channel_id,
        'text': message,
        'reply_broadcast': 'True',
        'thread_ts': ts
    }
    url = 'https://slack.com/api/chat.postMessage'
    res = requests.post(url, data=data)
