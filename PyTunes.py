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
from text2speech import t2s
from time import sleep
from next_keyword import next_keyword

def select_by_speech():
    t2i_en = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine':9, 'ten':10 }
    t2i_en2 = {'number one': 1, 'number two': 2, 'number three': 3, 'number four': 4, 'number five': 5, 'number six': 6, 'number seven': 7, 'number eight': 8, 'number nine':9, 'number ten':10 }
    t2i_vn = {'một': 1, 'hai': 2, 'ba': 3, 'bốn': 4, 'năm': 5, 'sáu': 6, 'bẩy': 7, 'tám': 8, 'chín':9, 'mười':10 }
    t2i_vn2 = {'số 1': 1, 'số 2': 2, 'số 3': 3, 'số 4': 4, 'số 5': 5, 'số 6': 6, 'số 7': 7, 'số 8': 8, 'số 9':9, 'số 10':10 }
    t2i = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9':9, '10':10 }
    match = False
    while match != True:
        t2s('select song')
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

    t2i_en = {'play':0, 'next':1, 'stop':2, 'search':3, 'select song':4, 'next random':6, 'exit':5}
    t2i_vn = {'phát':0, 'tiếp tục':0, 'tiếp theo':1, 'kế tiếp':1, 'dừng lại':2, 'tìm kiếm':3, 'chọn bài hát':4, 'chọn bài':4, "gợi ý bài mới":6, "gợi ý":6, 'thoát':5, 'thoát chương trình':5}
    
    match = False
    while match != True:
        t2s('speech command')
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
        sleep(1)
        key = recognize('keyword')
        #t2s('you are want to find: {}'.format(key))
        if key != "error":
            t2s("search for")
            t2s(key)
            cf = recognize('YES or OK to confirm and NO to try again')
        else:
            continue

        if cf in ['yes','ok','oke','đúng','phải','đồng ý']:
            t2s('ok')
            #match = True
            break
        #else:
            #t2s('oh sorry! please speech keyword again')
    return key
        
def getLinkAudio(link):
    print('start get audio')
    video = pafy.new(link)
    best = video.getbestaudio()
    url = best.url
    print('done get audio')
    return url

class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.instance = vlc.Instance()
        self.mediaplayer = self.instance.media_player_new()
        
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
        # self.show()
        self.showFullScreen()
        #self.Wellcome()

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
        self.searchInput.setFixedHeight(30)
        #self.searchInput.setText("ok binz")
        self.searchBtn = QPushButton('Tìm kiếm')
        self.searchBtn.setFixedHeight(50)
        self.searchBtn.clicked.connect(self.Search)

        self.voicesearchBtn = QPushButton('Tìm bằng giọng nói')
        self.voicesearchBtn.setFixedHeight(50)
        self.voicesearchBtn.clicked.connect(self.VoiceSearch)

        self.listAudio = QListWidget()
        
        self.volumeslider = QSlider(Qt.Horizontal, self)
        self.volumeslider.setMaximum(100)
        self.volumeslider.setMinimum(0)
        # self.volumeslider.setValue(self.mediaplayer.audio_get_volume())
        self.volumeslider.setValue(100)
        self.volumeslider.setToolTip("Âm lượng")
        
        self.playbutton = QPushButton('Phát/Tạm dừng')  # play button
        self.playbutton.setFixedHeight(50)
        self.stopbutton = QPushButton('Dừng')  # Stop button
        self.stopbutton.setFixedHeight(50)
        self.nextbutton = QPushButton('Tiếp theo')  # Next button
        self.nextbutton.setFixedHeight(50)
        self.nextbutton2 = QPushButton('Tiếp theo')  # Next button
        self.nextbutton2.setFixedHeight(50)
        self.command = QPushButton('Ra lệnh bằng giọng nói')  # Next button
        self.command.setFixedHeight(50)

        self.shortcut = QShortcut(QKeySequence("Space"), self)
        self.shortcut.activated.connect(self.excCommand)

        self.exit = QPushButton('Thoát')  # Next button
        # Add button layouts
        mainLayout = QVBoxLayout()
        # search = QHBoxLayout()
        controls = QHBoxLayout()
        # Add search
        controls.addWidget(self.playbutton)
        #controls.addWidget(self.nextbutton)
        controls.addWidget(self.nextbutton2)
        controls.addWidget(self.stopbutton)
        # Add to vertical layout
        mainLayout.addWidget(self.status)
        mainLayout.addWidget(self.searchInput)
        mainLayout.addWidget(self.result_label)
        mainLayout.addWidget(self.listAudio)
        mainLayout.addWidget(self.searchBtn)
        mainLayout.addWidget(self.voicesearchBtn)
        mainLayout.addLayout(controls)
        mainLayout.addWidget(self.command)
        mainLayout.addWidget(self.volumeslider)
        mainLayout.addWidget(self.exit)
        wid.setLayout(mainLayout)
        # Connect each signal to their appropriate function
        self.playbutton.clicked.connect(self.PlayPause)
        self.stopbutton.clicked.connect(self.Stop)
        #self.nextbutton.clicked.connect(self.Next)
        self.nextbutton2.clicked.connect(self.Next)
        self.command.clicked.connect(self.excCommand)
        self.volumeslider.valueChanged.connect(self.setVolume)
        # self.volumeslider.valueChanged.connect(self.volumeslabel.setNum)
        self.exit.clicked.connect(self.exitApp)
        self.statusBar()

    def exitApp(self):
        exit()

    def setVolume(self, Volume):
        self.mediaplayer.audio_set_volume(Volume)

    def PlayPause(self):
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
            self.playbutton.setText("Phát")
            #self.status.setText("Đang tạm dừng")
        else:
            self.mediaplayer.play()
            self.playbutton.setText("Tạm dừng")
            #self.status.setText("Đang phát")
            
    def Pause(self):
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
            self.playbutton.setText("Phát")

    def Stop(self):
        self.mediaplayer.stop()
        self.playbutton.setText("Phát")
        #self.status.setText("Đã dừng")
    
    def setMediaPlayerUrl(self, url):
        self.media = self.instance.media_new(url)
        self.mediaplayer.set_media(self.media)

    def generateRandomList(self):
        list_title = ["nhạc hay", "nhạc mới", "nhạc trẻ hot", "nhac viet", "top hit", "best song"]
        next_key = next_keyword(list_title)
        self.status.setText('Tìm kiếm cho: "{}"'.format(next_key))
        self.searchInput.setText(next_key)
        self.Search(get_idx_by_user=False)

    def getListSearch(self):
        self.status.setText('Đang tìm')
        if self.searchInput.text() == '':
            self.status.setText('Nhập từ khóa hoặc tìm bằng giọng nói')
            t2s('enter keyword or voice search')
        else:
            print('keyword:', self.searchInput.text())
            print('searching...')
            results = YoutubeSearch(self.searchInput.text(), max_results=5).to_json()
            results = json.loads(results)
            results = results["videos"]
            
            if len(results) == 0:
                if self.fornext:
                    #self.idx_audio = 0
                    pass
                else:
                    self.status.setText('Không có kết quả hoặc lỗi')
                    t2s('try again')
                    #self.searchInput.setText('')
            else:
                #tìm kiếm mới
                self.listAudio_text = {}
                self.listAudio.clear()
                self.list_title = [e["title"] for e in results]
                
                for i, item in enumerate(results):
                    itemlink = 'https://www.youtube.com' + item['link']
                    self.listAudio_text[self.list_title[i]] = itemlink
                    self.status.setText('Kết quả cho: "{}"'.format(self.searchInput.text()))
                
                for i, item in enumerate(results):
                    #nếu search gợi ý cho next thì chỉ hiển thị 1 bài tiếp theo
                    if self.fornext:
                        self.listAudio.insertItem(i+1, 'Tiếp theo: ' + self.list_title[i])
                        self.idx_audio = 0
                        break
                    else:
                        self.listAudio.insertItem(i+1, str(i+1) + ': ' + self.list_title[i])

                self.listAudio.repaint()
        self.listAudio.repaint()

    def Search(self):
        self.Pause()
        self.fornext = False
        self.getListSearch()
        try:
            _ = len(self.listAudio_text)
            self.idx_audio = select_by_speech()
            self.fornext = True
            self.selectAndPlaySongByIndex()
        except:
            self.status.setText('Không có kết quả hoặc lỗi')
            #t2s('try again')

    def VoiceSearch(self):
        self.Pause()
        t2s('Start Voice Search')
        self.status.setText('Tìm kiếm giọng nói')
        keyword = getVoiceKeyWord() # có xác nhận key
        # keyword = recognize('keyword')# không cần xác nhận
        t2s('search for {}'.format(keyword))
        self.status.setText('Tìm kiếm cho: "{}"'.format(keyword))
        self.searchInput.setText(keyword)
        self.Search()
        #self.selectAndPlaySongByIndex()
        
    def selectAndPlaySongByIndex(self):
        title_audio = list(self.listAudio_text.keys())[self.idx_audio]
        link_audio = list(self.listAudio_text.values())[self.idx_audio]
        link_audio = getLinkAudio(link_audio)
        t2s('Start play: {}'.format(title_audio))
        self.setMediaPlayerUrl(link_audio)

        next_key = next_keyword(self.list_title)
        self.searchInput.setText(next_key)
        self.getListSearch()

        self.PlayPause()
        self.status.setText('Đang phát: {}'.format(title_audio))
  
    def Next(self):
        self.status.setText("Tiếp theo")
        t2s("next")
        self.Pause()
        self.selectAndPlaySongByIndex()
    
    def nextRecommend(self):
        self.status.setText("Tiếp theo gợi ý")
        self.Pause()
        next_key = next_keyword(self.list_title)
        self.status.setText('Tìm kiếm cho: "{}"'.format(next_key))
        self.searchInput.setText(next_key)
        # self.Search(get_idx_by_user=False)
        self.SearchPlay()
    
    def voiceNext(self):
        print('Next song')
        self.Next()

    def voiceSelect(self):
        self.status.setText("Chọn bài hát")
        self.idx_audio = select_by_speech()
        self.selectAndPlaySongByIndex()

    def excCommand(self):
        self.Stop()
        #t2s('OK. Im here')
        t2s('Please speech a command')
        command = listen_command()
        if command == 0:
            self.PlayPause()
        elif command == 1:
            self.Next()
        elif command == 2:
            self.Stop()
        elif command == 3:
            self.VoiceSearch()
        elif command == 5:
            t2s('You are sure to exit!')
            t2s('Speech Yes or OK to comfirm!')
            cf_exit = recognize('')
            if cf_exit == 'yes' or cf_exit == 'ok' or cf_exit =='oke':
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
    with open('/home/pi/Desktop/music-player-voice-control-master/style.css', "r") as fh:
        app.setStyleSheet(fh.read())
    ex = App()
    sys.exit(app.exec_())
