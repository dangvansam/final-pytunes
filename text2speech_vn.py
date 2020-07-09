from gtts import gTTS
#from playsound import playsound
import os
#os.system("afplay file.mp3")
import re
import string
from mpyg321.mpyg321 import MPyg321Player

player = MPyg321Player()

patterns = {
    '[àáảãạăắằẵặẳâầấậẫẩ]': 'a',
    '[đ]': 'd',
    '[èéẻẽẹêềếểễệ]': 'e',
    '[ìíỉĩị]': 'i',
    '[òóỏõọôồốổỗộơờớởỡợ]': 'o',
    '[ùúủũụưừứửữự]': 'u',
    '[ỳýỷỹỵ]': 'y'
}
#hàm này để chuyển text có dấu thành k dấu
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
#đưa vào 1 đoạn text nó tạo file mp3
def t2s(text, clear_file=False):
    text  = text.translate(string.punctuation)
    #text = re.findall("(\w+)", text)
    print(text)
    filename = convert(text) + ".mp3"
    filename = filename.replace("|","").replace("#","").replace("?","").replace("」","").replace("「","").replace('\\','')
    #print("#############:"+filename)
    if filename in os.listdir('mp3'): #nếu tên file đã có rồi thì chỉ cần phát
        #print("đã có file mp3")
        #playsound('mp3/'+filename)
        player.play_song('mp3/'+filename)
        #os.system("mpg321 mp3/{} &".format(filename))
    else:
        #print("chưa có file mp3")
        tts = gTTS(text=text, lang='vi') #đoạn này là api của google
        tts.save('mp3/'+filename)
        #playsound('mp3/'+filename)
        player.play_song('mp3/'+filename)
        #os.system("mpg321 mp3/{} &".format(filename))
        if clear_file:
            os.remove('mp3/'+filename)
