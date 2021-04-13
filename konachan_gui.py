import tkinter as tk
from tkinter import messagebox
import time
import urllib.request
import requests
import os
from datetime import datetime
from bs4 import BeautifulSoup
import threading
import sys
import webbrowser

LOGTEXT = "태그 및 화상의 수를 입력합니다."
BTNTEXT = "Download"
SAFETY = "rating:safe+"

# 웹페이지 링크 열 때 씀
def callback(url):
    webbrowser.open_new(url)

class classKona():
    def __init__(self, __tag, __num):
        global LOGTEXT
        global BTNTEXT
        BTNTEXT = "Wait..."
        self.logText = "클래스를 시작합니다"
        self.tag_url = ''# INPUT(태그, 이미지 갯수)
        # self.tag = input("태그(tag)를 입력해주세요.(없으면 그대로 엔터) : ") #princess_connect
        self.tag = __tag
        self.tag_url = '&tags='+SAFETY+self.tag

        self.MAX_COUNT=-1
        while(True):
            # self.input_num = input("몇 개의 이미지를 크롤링할까요?(자연수로 입력) : ")
            self.input_num = __num
            if(self.input_num.isdecimal()):
                if(int(self.input_num)>0):
                    self.MAX_COUNT = int(self.input_num)
                    break

        # r18 = input("1 : 모든 이미지\n2 : R-18등급 이미지\n3 : R-18등급이 아닌 이미지\n : ")
        # r18 = int(r18)
        self.r18 = 1

        # 갤러리에서 뷰어URL 크롤

        self.url_root = "https://konachan.com/post?page=1" # 이후 추가주소 붙여서 url선정
        self.page = 1
        self.url_get = "https://konachan.com/post?page="+str(self.page)+self.tag_url

        self.res = urllib.request.urlopen(self.url_get).read()
        self.soup = BeautifulSoup(self.res,'html.parser')

        self.img_info_url = []
        self.counter = 0
        while((self.soup.find('a',class_='thumb') != None ) and self.counter < self.MAX_COUNT):

            print(str(self.page)+"페이지를 탐색중입니다.")
            LOGTEXT = str(self.page)+"페이지를 탐색중입니다."


            for tmp_url in self.soup.find_all('a',class_='thumb'):
                # 모든 이미지
                if (self.r18==1):
                    self.img_info_url.append('https://konachan.com'+tmp_url.get('href'))
                    self.counter += 1
                    if(self.counter >= self.MAX_COUNT):
                        break

            self.page += 1
            self.url_get = "https://konachan.com/post?page="+str(self.page)+self.tag_url

            self.res = urllib.request.urlopen(self.url_get).read()
            self.soup = BeautifulSoup(self.res,'html.parser')

        print(str(len(self.img_info_url))+"개의 이미지가 검색되었습니다.")
        LOGTEXT = str(len(self.img_info_url))+"개의 이미지가 검색되었습니다."
        
        self.keta = 1
        if(len(self.img_info_url)>9) : self.keta = 2
        if(len(self.img_info_url)>99) : self.keta = 3
        if(len(self.img_info_url)>999) : self.keta = 4
        if(len(self.img_info_url)>9999) : self.keta = 5
        if(len(self.img_info_url)>99999) : self.keta = 6

        # 폴더 생성
        self.now = datetime.now()
        self.folder_name = self.tag +"("+str(len(self.img_info_url))+")_"+ str(self.now)[:10] + "_" + str(self.now)[11:13] + str(self.now)[14:16] + str(self.now)[17:19]

        try:
            if not(os.path.isdir(self.folder_name)):
                os.makedirs(os.path.join(self.folder_name))
        except OSError as e:
            if e.errno != errno.EEXIST:
                print("Failed to create directory!!")
                raise

        print("저장폴더를 생성했습니다. <"+self.folder_name+">")
        LOGTEXT = "저장폴더를 생성했습니다. <"+self.folder_name+">"


        # 뷰어URL에서 이미지 크롤
        print("다운로드를 시작합니다.")
        LOGTEXT = "다운로드를 시작합니다."
        for i in range(self.counter):

            self.res = urllib.request.urlopen(self.img_info_url[i]).read()
            self.soup = BeautifulSoup(self.res,'html.parser')

            #print(img_info_url[i])
            img_src = ""
            try:
                img_src = self.soup.find('a',class_='highres-show')['href']
                #print("더 큰 사이즈의 원본을 받습니다")
            except:
                try:
                    img_src = self.soup.find('img',class_='image')['src']
                    #print("표시된 원본을 그대로 받습니다")
                except:
                    print("뭔가가 잘못되었습니다.")
            print('Downloading [ '+str(i+1)+' / '+str(self.counter) + ' ]')
            LOGTEXT = 'Downloading [ '+str(i+1)+' / '+str(self.counter) + ' ]'
            urllib.request.urlretrieve(img_src, '.\\'+self.folder_name+'\\'+str(i+1).zfill(self.keta)+'.png')
        print("다운로드가 완료되었습니다.")
        LOGTEXT = "다운로드가 완료되었습니다."
        BTNTEXT = "Download"
        webbrowser.open_new('.\\'+self.folder_name)

# 썸네일 표시의 a 태그는 class='thumb'
#url = 'https://files.yande.re/sample/3de6b336c21feba3f1a0a796ac3d9dcc/yande.re%20488783%20sample%20anus%20doremy_sweet%20dress%20gekidoku_shoujo%20ke-ta%20nopan%20photoshop%20pussy%20skirt_lift%20tail%20touhou%20uncensored.jpg'
#urllib.request.urlretrieve(url, '.\\'+folder_name+'\\test.png')

class LabelUpdate(threading.Thread):

    def __init__(self, _window):
        threading.Thread.__init__(self)
        self.win = _window

    def run(self):
        while True:
            time.sleep(0.1)
            self.win.log.set(LOGTEXT)
            self.win.btnStr.set(BTNTEXT)


class NewThread(threading.Thread):

    def __init__(self, _window):
        threading.Thread.__init__(self)
        self.win = _window

    def run(self):
        print(type(self.win))
        instance = classKona(self.win.str1.get(), self.win.str2.get())


class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):

        # 일반라벨
        self.lb1 = tk.Label(window, text="TAG : ").grid(row=0,column=0)
        self.lb2 = tk.Label(window, text="NUM : ").grid(row=1,column=0)

        # 업데이트용 문자열변수와 라벨
        self.log = tk.StringVar()
        self.log.set(":3")
        self.lb3 = tk.Label(window, textvariable=self.log).grid(row=3,column=0,columnspan=3)

        # 링크주소 라벨과 기능
        self.link1 = tk.Label(window, text="https://konachan.com/post", fg="blue", cursor="hand2")
        self.link1.grid(row=4,column=0,columnspan=3)        
        self.link1.bind("<Button-1>", lambda e: callback("https://konachan.com/post"))

        # 텍스트 필드 읽어올 문자열변수
        self.str1=tk.StringVar()
        self.str2=tk.StringVar()

        self.input_tag_field = tk.Entry(window, textvariable=self.str1).grid(row=0,column=1,columnspan=2)
        self.input_num_field = tk.Entry(window, textvariable=self.str2).grid(row=1,column=1,columnspan=2)
        
        # 다운로드 버튼에 표시할 문자열 변수, 버튼변수, 클릭 시 실행할 함수
        self.btnStr = tk.StringVar()
        self.btnStr.set("tmp button text")
        self.btn_dl = tk.Button(window, textvariable=self.btnStr, width=10, height=4)

        self.btn_dl["command"] = self.downloadStart
        self.btn_dl.grid(row=0,column=3,rowspan=3)

        # 체크확인용 변수, 체크박스
        self.v1=tk.IntVar()
        self.check1 = tk.Checkbutton(window, text="Safe", variable = self.v1, command = self.saftySetting)
        self.check1.select()

        self.v2=tk.IntVar()
        self.check2 = tk.Checkbutton(window, text="+R18", variable = self.v2, command = self.saftySetting)

        self.check1.grid(row=2,column=1)
        self.check2.grid(row=2,column=2)

        # 버튼(종료용도)
        self.quit = tk.Button(window, text="QUIT", fg="red", command=self.quitApp, width=10, height=2)
        self.quit.grid(row=3,column=3,rowspan=2)

        # 이후 0.1초 간격으로 라벨 계속 업데이트. 이렇게 해도 되기는 되서 함... 좋은 방법일 것 같진 않음.
        LabelUpdate(self).start()

    # 체크박스 변동 시 변수조작
    def saftySetting(self):
        global SAFETY
        if(self.v1.get()==0 and self.v2.get()==0):
            SAFETY = ""
        if(self.v1.get()==1 and self.v2.get()==0):
            SAFETY = "rating:safe+"
        if(self.v1.get()==0 and self.v2.get()==1):
            SAFETY = "-rating:safe+"
        if(self.v1.get()==1 and self.v2.get()==1):
            SAFETY = ""
        print("1 : "+str(self.v1.get()))
        print("2 : "+str(self.v2.get()))

    # 체크박스 체크 확인 후, 다운로드용 스레드 시작
    def downloadStart(self):

        global LOGTEXT
        print("PUSH DL BUTTON")

        if(self.v1.get()==0 and self.v2.get()==0):
            LOGTEXT = "체크박스가 선택되지 않았습니다."
            return

        NewThread(self).start()
        
    # 종료 버튼 클릭
    def quitApp(self):
        sys.exit()


window = tk.Tk()

# 닫기 버튼 시 함수
def on_closing():
    if tk.messagebox.askokcancel("Quit", "Do you want to quit?"): # 이거 안하면 왠진 모르겠는데 안꺼짐;; 타임슬립 등 넣어도 마찬가지
        sys.exit()
window.protocol("WM_DELETE_WINDOW", on_closing)

# 타이틀, 파일아이콘, 윈도우상단아이콘, 윈도우크기, 크기재설정여부
window.title("KONA_DL ver=0.1")
window.iconbitmap(default='icon.ico')
window.tk.call('wm', 'iconphoto', window._w, tk.PhotoImage(file='./icon.png'))
window.geometry("272x120+1200+200")
window.resizable(False,False)

# 앱 시작
app = Application(master=window)
app.mainloop()