from Slack.api import *

if __name__ == '__main__':
    slack_api = SlackAPI()
    print(slack_api.channel_list_json())