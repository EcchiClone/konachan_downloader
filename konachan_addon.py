import urllib.request
import requests
import os
from datetime import datetime
from bs4 import BeautifulSoup

class classKona():
    def __init__(self, __tag, __num):
        self.logText = "클래스를 시작합니다"
        self.tag_url = ''# INPUT(태그, 이미지 갯수)
        # self.tag = input("태그(tag)를 입력해주세요.(없으면 그대로 엔터) : ") #princess_connect
        self.tag = __tag
        if(self.tag!=''):
            self.tag_url = '&tags='+self.tag

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
            self.logText = ["페이지를 탐색중입니다."]


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

        print(str(len(self.img_info_url))+"개의 이미지가 검색되었습니다.")

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


        # 뷰어URL에서 이미지 크롤
        print("크롤링을 시작합니다.")
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
            urllib.request.urlretrieve(img_src, '.\\'+self.folder_name+'\\'+str(i+1).zfill(3)+'.png')
        print("다운로드가 완료되었습니다.")
    



# 썸네일 표시의 a 태그는 class='thumb'
#url = 'https://files.yande.re/sample/3de6b336c21feba3f1a0a796ac3d9dcc/yande.re%20488783%20sample%20anus%20doremy_sweet%20dress%20gekidoku_shoujo%20ke-ta%20nopan%20photoshop%20pussy%20skirt_lift%20tail%20touhou%20uncensored.jpg'
#urllib.request.urlretrieve(url, '.\\'+folder_name+'\\test.png')