from Slack.api import *
from Papago.api import *

if __name__ == '__main__':
    slack_api = SlackAPI()
    channel_list = slack_api.get_channel_list_json()
    channel_name = 'test'
    channel_id = slack_api.get_channel_id(channel_name)
    msg = 'From Slack API'
    slack_api.post_message(channel_id, msg)
    papago_api = PapagoAPI()
    text = '번역해봐'
    translated_text = papago_api.translate(text)
    print(translated_text['message']['result'])