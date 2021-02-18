import json
import requests

import Papago.constant


def get_auth_keys_from_file(auth_file_name):
    with open(auth_file_name, 'r') as json_file:
        auth_dict = json.load(json_file)

    return auth_dict['client_id'], auth_dict['client_secret']


class PapagoAPI:
    def __init__(self):
        self.client_id, self.client_secret = get_auth_keys_from_file(Papago.constant.AUTH_FILE_NAME)
        self._headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Naver-Client-Id': self.client_id,
            'X-Naver-Client-Secret': self.client_secret
        }

    def translate(self, text, source='ko', target='en'):
        headers = self._headers
        data = {
            'source': source,
            'target': target,
            'text': text
        }
        res = requests.post(Papago.constant.PAPAGO_API_URL, headers=headers, data=data)
        return res.json()
