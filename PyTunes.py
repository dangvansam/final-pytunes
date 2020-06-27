import sys
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtGui import QKeySequence
from PyQt5 import QtCore
from PyQt5.QtCore import QUrl, QDirIterator, Qt
from PyQt5.QtWidgets import QApplication, QListWidget, QWidget, QMainWindow, QPushButton, QFileDialog, QAction, QHBoxLayout, QVBoxLayout, QSlider, QLineEdit ,QLabel, QListView, QFrame, QShortcut
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaPlayer, QMediaContent
import vlc
import pafy
from youtube_search import YoutubeSearch 
import json
from recognition import recognize
from text2speech_vn import t2s
from time import sleep
from next_keyword import next_keyword
import random

def select_by_speech():
    t2i_en = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine':9, 'ten':10 }
    t2i_en2 = {'number one': 1, 'number two': 2, 'number three': 3, 'number four': 4, 'number five': 5, 'number six': 6, 'number seven': 7, 'number eight': 8, 'number nine':9, 'number ten':10 }
    t2i_vn = {'một': 1, 'hai': 2, 'ba': 3, 'bốn': 4, 'năm': 5, 'sáu': 6, 'bẩy': 7, 'tám': 8, 'chín':9, 'mười':10 }
    t2i_vn2 = {'số 1': 1, 'số 2': 2, 'số 3': 3, 'số 4': 4, 'số 5': 5, 'số 6': 6, 'số 7': 7, 'số 8': 8, 'số 9':9, 'số 10':10 }
    t2i = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9':9, '10':10 }
    match = False
    firttime = True
    while match != True:
        if firttime:
            t2s('Mời bạn chọn bài hát bằng cách nói số thứ tự bài')
            firttime = False
        else:
            t2s("Tôi chưa hiểu hãy thử lại")
        text = recognize()
        if text in t2i_en.keys() or text in t2i_en2.keys() or text in t2i_vn.keys() or t2i_vn2.keys() or text in t2i.keys():
            if text in t2i_en.keys():
                number = t2i_en[text]
                match = True
                break
            elif text in t2i_en2.keys():
                number = t2i_en2[text]
                match = True
                break
            elif text in t2i_vn.keys():
                number = t2i_vn[text]
                match = True
                break
            elif text in t2i_vn2.keys():
                number = t2i_vn2[text]
                match = True
                break
            elif text in t2i.keys():
                number = t2i[text]
                match = True
                break
            # mặc định trả về 0 nếu không nhận dạng được, nếu không mặc định
            # thì hỏi đến lúc nhận dạng đúng
            #else:
                #match = True
                #number = 1
                #break
    return int(number) - 1

def waitForSpeech():
    t2s('I am listing')
    #print('I am listing')


def listen_command():
    t2s('Bạn muốn tôi làm gì hãy ra lệnh cho tôi')
    #t2s('Ví dụ tìm kiếm, kế tiếp, tiếp tục')
    t2i_en = {'play':0, 'next':1, 'stop':2, 'search':3, 'volume up':4, 'volume down':6, 'exit':5}
    t2i_vn = {'phát':0, 'tiếp tục':0, 'tiếp theo':1, 'kế tiếp':1, 'dừng lại':2, 'tìm kiếm':3, 'tăng âm lượng':4, 'tăng âm':4, "giảm âm lượng":6, "giảm âm":6, 'thoát':5, 'thoát chương trình':5}
    
    match = False
    while match != True:
        t2s('Đọc lệnh bạn muốn')
        text = recognize()
        if text in t2i_en.keys() or text in t2i_vn.keys():
            if text in t2i_en.keys():
                command = t2i_en[text]
                match = True
            elif text in t2i_vn.keys():
                command = t2i_vn[text]
                match = True
    return int(command)

def getVoiceKeyWord():
    match = False
    while True:
        #sleep(1)
        key = recognize('keyword')
        #t2s('you are want to find: {}'.format(key))
        if key != "error":
            t2s("Có phải bạn muốn tìm kiếm {}".format(key))
            cf = recognize('Nói OK hoặc Đồng ý để xác nhận')
        else:
            continue

        if cf in ['yes','ok','oke','đúng','phải','đồng ý']:
            t2s('Ok tìm kiếm cho {}'.format(key))
            #match = True
            break
        #else:
            #t2s('oh sorry! please speech keyword again')
    return key
        
def getLinkAudio(link):
    #print('start get audio')
    video = pafy.new(link)
    best = video.getbestaudio()
    url = best.url
    #print('done get audio')
    return url

class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.instance = vlc.Instance('--novideo')
        #self.mediaplayer = self.instance.media_player_new()
        self.medialist = self.instance.media_list_new()
        self.mediaplayer = self.instance.media_list_player_new()
        
        self.title = 'Player'
        self.left = 500
        self.top = 200
        self.width = 600
        self.height = 400
        self.color = 0  # 0- toggle to dark 1- toggle to light
        self.initUI()

    def initUI(self):
        self.addControls()
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.toggleColors()
        self.show()
        #self.showFullScreen()
        self.Wellcome()

    def addControls(self):
        wid = QWidget(self)
        self.setCentralWidget(wid)
        # Status
        self.status = QLabel()
        self.status.setAlignment(QtCore.Qt.AlignCenter)
        self.status.setStyleSheet('color: #1DB954')
        self.status.setText('Xin chào')
        # List
        self.result_label = QLabel()
        self.result_label.setAlignment(QtCore.Qt.AlignCenter)
        self.result_label.setStyleSheet('color: #1DB954')
        self.result_label.setText('Danh sách phát')
        # Search
        self.searchInput = QLineEdit()
        self.searchInput.setFixedHeight(22)
        self.searchInput.setText("am tham ben em")
        self.searchBtn = QPushButton('Tìm kiếm')
        self.searchBtn.setFixedHeight(40)
        self.searchBtn.clicked.connect(self.Search)

        self.voicesearchBtn = QPushButton('Tìm bằng giọng nói')
        self.voicesearchBtn.setFixedHeight(40)
        self.voicesearchBtn.clicked.connect(self.VoiceSearch)

        self.listAudio = QListWidget()
        self.listAudio.setFixedHeight(125)
        
        self.current_vol = 60
        self.mediaplayer.get_media_player().audio_set_volume(self.current_vol)

        self.voldown = QPushButton('-')
        self.volup = QPushButton('+')
        self.volup.setFixedHeight(50)
        self.volup.setFixedWidth(50)
        self.voldown.setFixedHeight(50)
        self.voldown.setFixedWidth(50)

        
        self.playbutton = QPushButton('Phát/Tạm dừng')  # play button
        self.playbutton.setFixedHeight(50)
        self.stopbutton = QPushButton('Dừng')  # Stop button
        self.stopbutton.setFixedHeight(50)
        self.nextbutton = QPushButton('Tiếp theo')  # Next button
        self.nextbutton.setFixedHeight(50)
        self.nextbutton2 = QPushButton('Tiếp theo')  # Next button
        self.nextbutton2.setFixedHeight(50)
        self.command = QPushButton('Ra lệnh bằng giọng nói')  # Next button
        self.command.setFixedHeight(40)

        self.shortcut = QShortcut(QKeySequence("Space"), self)
        self.shortcut.activated.connect(self.excCommand)

        self.exit = QPushButton('Thoát')  # Next button
        self.exit.setFixedHeight(40)
        # Add button layouts
        mainLayout = QVBoxLayout()

        controls = QHBoxLayout()
        controls.addWidget(self.voldown)
        controls.addWidget(self.playbutton)
        controls.addWidget(self.nextbutton2)
        controls.addWidget(self.stopbutton)
        controls.addWidget(self.volup)

        # Add to vertical layout
        mainLayout.addWidget(self.status)
        mainLayout.addWidget(self.searchInput)
        mainLayout.addWidget(self.result_label)
        mainLayout.addWidget(self.listAudio)
        mainLayout.addWidget(self.searchBtn)
        mainLayout.addWidget(self.voicesearchBtn)
        mainLayout.addLayout(controls)
        mainLayout.addWidget(self.command)
        mainLayout.addWidget(self.exit)
        wid.setLayout(mainLayout)

        self.playbutton.clicked.connect(self.PlayPause)
        self.stopbutton.clicked.connect(self.Stop)
        self.nextbutton2.clicked.connect(self.Next)
        self.volup.clicked.connect(self.volUp)
        self.voldown.clicked.connect(self.volDown)

        self.command.clicked.connect(self.excCommand)
        self.exit.clicked.connect(self.exitApp)
        self.statusBar()
        
    def Wellcome(self):
        t2s("Xin chào tôi là Pi")

    def exitApp(self):
        exit()

    def setVolume(self, Volume):
        self.mediaplayer.get_media_player().audio_set_volume(Volume)

    def volUp(self):
        if self.current_vol < 100:
            self.current_vol = self.current_vol + 20
            self.mediaplayer.get_media_player().audio_set_volume(self.current_vol)
        
    def volDown(self):
        if self.current_vol > 20:
            self.current_vol = self.current_vol - 20
            self.mediaplayer.get_media_player().audio_set_volume(self.current_vol)
        

    def PlayPause(self):
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
            self.playbutton.setText("Phát")
            #self.status.setText("Đang tạm dừng")
        else:
            self.mediaplayer.play()
            self.playbutton.setText("Tạm dừng")
            
    def Pause(self):
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
            self.playbutton.setText("Phát")

    def Stop(self):
        self.mediaplayer.stop()
        self.playbutton.setText("Phát")
    
    def setMediaPlayerUrl(self, url):
        #self.media = self.instance.media_new(url)
        #self.mediaplayer.set_media(self.media)
        for u in url:
            self.medialist.add_media(self.instance.media_new(u))
        self.mediaplayer.set_media_list(self.medialist)

    def addMediaPlayerUrl(self, url):
        #self.media = self.instance.media_new(url)
        #self.mediaplayer.set_media(self.media)
        if self.medialist.count() == 0:
            self.medialist.add_media(self.instance.media_new(url))
        else:
            self.medialist.insert_media(self.instance.media_new(url),1)

        self.mediaplayer.set_media_list(self.medialist)

    def getListSearch(self):
        self.status.setText('Đang tìm')
        if self.searchInput.text() == '':
            self.status.setText('Nhập từ khóa hoặc tìm bằng giọng nói')
            t2s('Vui lòng nhập từ khóa hoặc tìm kiếm bằng giọng nói')
        else:
            print('keyword:', self.searchInput.text())
            print('searching...')
            results = []
            try:
                results = YoutubeSearch(self.searchInput.text(), max_results=5).to_json()
            except:
                #sleep(1)
                results = YoutubeSearch(self.searchInput.text(), max_results=5).to_json()
            results = json.loads(results)
            results = results["videos"]

            if len(results) == 0:
                if self.fornext:
                    self.listAudio.clear()
                    self.medialist.remove_index(0)
                    self.idx_audio = self.idx_audio + 1
                    self.listAudio.insertItem(0, 'Tiếp theo: ' + self.list_title[self.idx_audio])
                    self.listAudio.repaint()
                else:
                    self.status.setText('Không có kết quả hoặc lỗi')
                    t2s('Tôi không thể tìm kiếm Hãy thử lại')
            else:
                #tìm kiếm mới
                self.listAudio_text = {}
                self.listAudio.clear()
                self.list_title = [e["title"] for e in results]
                print("list_title:",self.list_title)

                for i, item in enumerate(results):
                    itemlink = 'https://www.youtube.com' + item['link']
                    self.listAudio_text[self.list_title[i]] = itemlink
                    self.status.setText('Kết quả cho: "{}"'.format(self.searchInput.text()))
                
                for i, item in enumerate(results):
                    #nếu search gợi ý cho next thì chỉ hiển thị 1 bài tiếp theo
                    if self.fornext:
                        self.listAudio.insertItem(i+1, 'Tiếp theo: ' + self.list_title[i])
                        self.idx_audio = 0
                        self.listAudio.repaint()
                        break
                    else:
                        self.listAudio.insertItem(i+1, str(i+1) + ': ' + self.list_title[i])

                self.listAudio.repaint()
        self.listAudio.repaint()
        print("end search")

    def Search(self):
        self.Stop()
        self.medialist.remove_index(0)
        self.medialist.remove_index(1)
        self.fornext = False
        t2s("đang tìm kiếm")
        self.getListSearch()
        try:
            _ = len(self.listAudio_text)
            t2s("Đây là những kết quả tôi tìm được. Vui lòng chọn một bài")
            self.idx_audio = 0#select_by_speech()
            self.fornext = True
            self.selectAndPlaySongByIndex()
        except:
            self.status.setText('Không có kết quả hoặc lỗi')
            #t2s('try again')

    def VoiceSearch(self):
        self.Stop()
        t2s('Chức năng tìm kiếm bằng giọng nói sẵn sàng')
        self.status.setText('Tìm kiếm giọng nói')
        keyword = getVoiceKeyWord() # có xác nhận key
        # keyword = recognize('keyword')# không cần xác nhận
        #t2s('search for {}'.format(keyword))
        self.status.setText('Tìm kiếm cho: "{}"'.format(keyword))
        self.searchInput.setText(keyword)
        self.Search()
        
    def selectAndPlaySongByIndex(self):
        title_audio = list(self.listAudio_text.keys())[self.idx_audio]
        link_audio = list(self.listAudio_text.values())[self.idx_audio]
        link_audio = getLinkAudio(link_audio)
        t2s('Bắt đầu phát')
        t2s(title_audio)
        print(self.medialist.count())
        self.addMediaPlayerUrl(link_audio)
        print(self.medialist.count())

        next_key = next_keyword(self.list_title)
        self.searchInput.setText(next_key)
        self.getListSearch()

        title_audio2 = list(self.listAudio_text.keys())[self.idx_audio]
        link_audio2 = list(self.listAudio_text.values())[self.idx_audio]
        link_audio2 = getLinkAudio(link_audio2)
        self.addMediaPlayerUrl(link_audio2)
        print(self.medialist.count())
        #print(self.medialist)

        self.PlayPause()
        self.status.setText('Đang phát: {}'.format(title_audio))
  
    def Next(self):
        self.Stop()
        self.status.setText("Tiếp theo")
        t2s("Tiếp theo")
        self.medialist.remove_index(0)
        self.medialist.remove_index(1)
        print(self.medialist.count())
        self.selectAndPlaySongByIndex()

    def excCommand(self):
        self.Pause()
        command = listen_command()
        if command == 0:
            self.PlayPause()
        elif command == 1:
            self.Next()
        elif command == 2:
            self.Stop()
            t2s("đã dừng phát")
        elif command == 3:
            self.VoiceSearch()
        elif command == 4:
            self.volUp()
            t2s("đã tăng")
            self.PlayPause()
        elif command == 6:
            self.volDown()
            t2s("đã giảm")
            self.PlayPause()

        elif command == 5:
            t2s('Bạn chắc chắn muốn thoát không')
            t2s('Xác nhận bằng cách nói ok')
            cf_exit = recognize('')
            if cf_exit == 'yes' or cf_exit == 'ok' or cf_exit =='oke':
                t2s("Chào bạn hẹn gặp lại bạn hihi")
                exit()
            else:
                print('no exit')
            
    def toggleColors(self):
        app.setStyle("Fusion")
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(41, 41, 41))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(41, 41, 41))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(29, 185, 84))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(235, 101, 54))
        palette.setColor(QPalette.Highlight, Qt.white)
        palette.setColor(QPalette.HighlightedText,  QColor(29, 185, 84))
        app.setPalette(palette)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # load and set stylesheet
    #with open('/home/pi/Desktop/music-player-voice-control-master/style.css', "r") as fh:
    with open('style.css', "r") as fh:
        app.setStyleSheet(fh.read())
    ex = App()
    sys.exit(app.exec_())
