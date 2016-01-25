import sys, subprocess
from urllib import parse
 
def getSpeech(phrase):
    googleAPIurl = "http://translate.google.com/translate_tts?tl=en&"
    param = {'q': phrase}
    data = parse.urlencode(param)
    googleAPIurl += data # Append the parameters
    return googleAPIurl
 
def raspberryTalk(text): # This will call mplayer and will play the sound
    subprocess.call(["mplayer",getSpeech(text)], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
 
if __name__ == "__main__":
    raspberryTalk("I love anning, but she hate me. so i am so sadly")
