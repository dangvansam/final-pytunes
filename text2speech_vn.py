from gtts import gTTS
from playsound import playsound
import os
#os.system("afplay file.mp3")
import re
import string

patterns = {
    '[àáảãạăắằẵặẳâầấậẫẩ]': 'a',
    '[đ]': 'd',
    '[èéẻẽẹêềếểễệ]': 'e',
    '[ìíỉĩị]': 'i',
    '[òóỏõọôồốổỗộơờớởỡợ]': 'o',
    '[ùúủũụưừứửữự]': 'u',
    '[ỳýỷỹỵ]': 'y'
}

def convert(text):
    """
    Convert from 'Tieng Viet co dau' thanh 'Tieng Viet khong dau'
    text: input string to be converted
    Return: string converted
    """
    output = text
    for regex, replace in patterns.items():
        output = re.sub(regex, replace, output)
        # deal with upper case
        output = re.sub(regex.upper(), replace.upper(), output)
    return output

def t2s(text, clear_file=False):
    text  = text.translate(string.punctuation)
    #text = re.findall("(\w+)", text)
    print(text)
    filename = convert(text) + ".mp3"
    filename = filename.replace("|",'').replace("#",'').replace("?",'')
    #print(filename)
    if filename in os.listdir('mp3'):
        #print("đã có file mp3")
        playsound('mp3/'+filename)
    else:
        #print("chưa có file mp3")
        tts = gTTS(text=text, lang='vi')
        tts.save('mp3/'+filename)
        playsound('mp3/'+filename)
        if clear_file:
            os.remove('mp3/'+filename)