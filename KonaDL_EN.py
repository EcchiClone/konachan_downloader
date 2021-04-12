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
LOGTEXT = "Input Tag and Number of Image."
BTNTEXT = "Download"
SAFETY = "rating:safe+"
class classKona():
    def __init__(self, __tag, __num):
        global LOGTEXT
        global BTNTEXT
        BTNTEXT = "Wait..."
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

            print(str(self.page)+"page.....is searching.")
            LOGTEXT = str(self.page)+"page.....is searching."


            for tmp_url in self.soup.find_all('a',class_='thumb'):
                # 모든 이미지
                if (self.r18==1):
                    self.img_info_url.append('https://konachan.com'+tmp_url.get('href'))
                    self.counter += 1
                    if(self.counter >= self.MAX_COUNT):
                        break
                # R-18 이미지만
                if (self.r18==2):
                    print(tmp_url.parent.parent.get('class',[]))
                    if(tmp_url.parent.parent.get('class',[])[0]!='javascript-hide'):
                        print('hide 가 아니다')
                        continue
                    print('hide 이다')
                    print(tmp_url.get('href'))
                    self.img_info_url.append('https://konachan.com'+tmp_url.get('href'))
                    self.counter += 1
                    if(self.counter >= self.MAX_COUNT):
                        break
                # R-18이 아닌 이미지만
                if (self.r18==3):
                    if(tmp_url.parent.parent.get('class',[])[0]=='javascript-hide'):
                        continue
                    self.img_info_url.append('https://konachan.com'+tmp_url.get('href'))
                    self.counter += 1
                    if(self.counter >= self.MAX_COUNT):
                        break

            self.page += 1
            self.url_get = "https://konachan.com/post?page="+str(self.page)+self.tag_url

            self.res = urllib.request.urlopen(self.url_get).read()
            self.soup = BeautifulSoup(self.res,'html.parser')

        print(str(len(self.img_info_url))+" images is already.")
        LOGTEXT = str(len(self.img_info_url))+" images is already."

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

        print("Complete to create save folder. <"+self.folder_name+">")
        LOGTEXT = "Complete to create save folder. <"+self.folder_name+">"


        # 뷰어URL에서 이미지 크롤
        print("Complete Download..")
        LOGTEXT = "Starting Download."
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
                    print("Error....!!")
            print('Downloading [ '+str(i+1)+' / '+str(self.counter) + ' ]')
            LOGTEXT = 'Downloading [ '+str(i+1)+' / '+str(self.counter) + ' ]'
            urllib.request.urlretrieve(img_src, '.\\'+self.folder_name+'\\'+str(i+1).zfill(3)+'.png')
        print("Complete Download.")
        LOGTEXT = "Complete Download."
        BTNTEXT = "Download"

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
            self.win.btn.set(BTNTEXT)

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
        #self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.lb1 = tk.Label(window, text="TAG : ").grid(row=0,column=0)
        self.lb2 = tk.Label(window, text="NUM : ").grid(row=1,column=0)
        self.log = tk.StringVar()
        self.log.set(":3")
        self.lb3 = tk.Label(window, textvariable=self.log).grid(row=3,column=0,columnspan=3)
        self.str1=tk.StringVar()
        self.str2=tk.StringVar()
        # self.lb1.pack(side="left")
        self.input_tag_field = tk.Entry(window, textvariable=self.str1).grid(row=0,column=1,columnspan=2)
        # self.input_tag_field.pack(side="right")
        # self.lb2.pack(side="left")
        self.input_num_field = tk.Entry(window, textvariable=self.str2).grid(row=1,column=1,columnspan=2)
        # self.input_num_field.pack(side="right")
        self.btn = tk.StringVar()
        self.btn.set("btn")
        self.hi_there = tk.Button(window, textvariable=self.btn, width=10, height=4)
        #self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.grid(row=0,column=3,rowspan=3)
        #self.hi_there.pack(side="top")
        self.v1=tk.IntVar()
        self.check1 = tk.Checkbutton(window, text="Safe", variable = self.v1, command = self.saftySetting)
        self.check1.select()
        self.v2=tk.IntVar()
        self.check2 = tk.Checkbutton(window, text="+R18", variable = self.v2, command = self.saftySetting)
        self.check1.grid(row=2,column=1)
        self.check2.grid(row=2,column=2)

        self.quit = tk.Button(window, text="QUIT", fg="red",
                              command=self.quitApp,width=10)
        self.quit.grid(row=3,column=3)
        LabelUpdate(self).start()

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

    def say_hi(self):
        global LOGTEXT
        print("PUSH DL BUTTON")
        if(self.v1.get()==0 and self.v2.get()==0):
            LOGTEXT = "select checkbox."
            return
        NewThread(self).start()
    def quitApp(self):
        sys.exit()


window = tk.Tk()
def on_closing():
    if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
        sys.exit()
window.protocol("WM_DELETE_WINDOW", on_closing)
window.title("KONA_DL ver=0.1")
window.iconbitmap('./icon.ico')
window.tk.call('wm', 'iconphoto', window._w, tk.PhotoImage(file='./icon.png'))
window.geometry("272x100+1200+200")
window.resizable(False,False)
app = Application(master=window)
app.mainloop()