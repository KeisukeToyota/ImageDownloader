from urllib import request
import sys
from tweepy import *
import webbrowser
import os
import signal
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

signal.signal(signal.SIGPIPE, signal.SIG_DFL)
signal.signal(signal.SIGINT, signal.SIG_DFL)

path = os.path.abspath(os.path.dirname(__file__))

def getOauth():
    consumer_key = '***********************'
    consumer_secret = '****************************'
    auth = OAuthHandler(consumer_key, consumer_secret)
    if os.path.isfile((path) + "/../data/access_token.txt"):
        with open((path) + '/../data/access_token.txt','r') as f:
            token = f.read()
        token = token.split('\n')
        access_token = token[0]
        access_token_secret = token[1]
        auth.set_access_token(access_token, access_token_secret)
        return auth
    else:
        if not os.path.exists((path) + '/../data'):
            os.system('mkdir ' + (path) + '/../data')
        f = open((path) + '/../data/access_token.txt','w+')
        url = auth.get_authorization_url()
        webbrowser.open(url)
        pin = input('Enter PIN code : ')
        auth.get_access_token(pin)
        auth.set_access_token(auth.access_token, auth.access_token_secret)
        f.write(auth.access_token + '\n' + auth.access_token_secret)
        f.close()
        return auth


def getImage(name):
    api = API(getOauth())
    if not os.path.exists(name):
        os.system('mkdir '+name)
    print('START\n')
    count = 0
    for status in Cursor(api.user_timeline, screen_name=name, count=200).items():
        try:
            if 'extended_entities' in status._json:
                for i in range(len(status.extended_entities['media'])):
                    with open(name+'/'+status._json['extended_entities']['media'][i]['id_str']+'.jpg', "wb") as image:
                        image.write(request.urlopen(status._json['extended_entities']['media'][i]['media_url']).read())
                    draw(name,status._json['extended_entities']['media'][i]['id_str']+'.jpg',status.text)
                    count += 1
            elif 'media' in status._json['entities']:
                with open(name+'/'+status._json['entities']['media'][0]['id_str']+'.jpg', "wb") as image:
                    image.write(request.urlopen(status._json['entities']['media'][0]['media_url']).read())
                draw(name,status._json['entities']['media'][0]['id_str']+'.jpg',status.text)
                count += 1
        except:
            continue
    print('Get count : '+str(count)+'\n')
    print('END')

def draw(image_path,name,text):
    tweet = text.replace('。','\n').replace('、','\n').replace('：','\n').replace('http','\nhttp')
    if not os.path.exists(image_path+'/text_image'):
        os.system('mkdir '+image_path+'/text_image')
    _bg = Image.open(image_path+'/'+name)
    _draw = ImageDraw.Draw(_bg,mode='RGB')
    canvas = Image.new('RGB', (_bg.size[0],_bg.size[1]+80), (255, 255, 255))
    _font = ImageFont.truetype('/Library/Fonts/Arial Unicode.ttf',12, encoding='utf-8')
    ImageDraw.Draw(canvas).text((0,0), tweet, font=_font,fill=(255,0,0))
    canvas.paste(_bg,(0,80))
    canvas.save(image_path+'/text_image/'+name)

def main():
    param = sys.argv
    getImage(param[1])

if __name__ == '__main__':
    main()
