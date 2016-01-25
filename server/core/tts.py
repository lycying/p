#!/bin/python
import sys, subprocess
from urllib import parse
from urllib import request
 
def getSpeech(phrase):
    googleAPIurl = "http://fanyi.baidu.com/gettts?lan=zh&spd=2&source=web&"
    param = {'text': phrase}
    #googleAPIurl = "http://translate.google.com/translate_tts?tl=en&"
    #param = {'q': phrase}
    data = parse.urlencode(param)
    googleAPIurl += data 
    return googleAPIurl
 
def netTalk(text): # This will call mplayer and will play the sound
    subprocess.call(["mplayer",getSpeech(text)], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

if __name__ == "__main__":
    netTalk("他把她打倒在地上，然后吻了它。啊，这不科学！")
