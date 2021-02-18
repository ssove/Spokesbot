from Papago.api import *

if __name__ == '__main__':
    papago_api = PapagoAPI()
    text = '번역해봐'
    translated_text = papago_api.translate(text)
    print(translated_text['message']['result'])