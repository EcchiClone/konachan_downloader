import urllib.request
import requests
import os
from datetime import datetime
from bs4 import BeautifulSoup

# INPUT(태그, 이미지 갯수)

tag_url = ''
tag = input("태그(tag)를 입력해주세요.(없으면 그대로 엔터) : ") #princess_connect

if(tag!=''):
    tag_url = '&tags='+tag

MAX_COUNT=-1
while(True):
    input_num = input("몇 개의 이미지를 크롤링할까요?(자연수로 입력) : ")
    if(input_num.isdecimal()):
        if(int(input_num)>0):
            MAX_COUNT = int(input_num)
            break

# r18 = input("1 : 모든 이미지\n2 : R-18등급 이미지\n3 : R-18등급이 아닌 이미지\n : ")
# r18 = int(r18)
r18 = 1

# 갤러리에서 뷰어URL 크롤

url_root = "https://konachan.com/post?page=1" # 이후 추가주소 붙여서 url선정
page = 1
url_get = "https://konachan.com/post?page="+str(page)+tag_url

res = urllib.request.urlopen(url_get).read()
soup = BeautifulSoup(res,'html.parser')

img_info_url = []
counter = 0
while((soup.find('a',class_='thumb') != None ) and counter < MAX_COUNT):

    print(str(page)+"페이지를 탐색중입니다.")

    for tmp_url in soup.find_all('a',class_='thumb'):
        # 모든 이미지
        if (r18==1):
            img_info_url.append('https://konachan.com'+tmp_url.get('href'))
            counter += 1
            if(counter >= MAX_COUNT):
                break
        # R-18 이미지만
        if (r18==2):
            print(tmp_url.parent.parent.get('class',[]))
            if(tmp_url.parent.parent.get('class',[])[0]!='javascript-hide'):
                print('hide 가 아니다')
                continue
            print('hide 이다')
            print(tmp_url.get('href'))
            img_info_url.append('https://konachan.com'+tmp_url.get('href'))
            counter += 1
            if(counter >= MAX_COUNT):
                break
        # R-18이 아닌 이미지만
        if (r18==3):
            if(tmp_url.parent.parent.get('class',[])[0]=='javascript-hide'):
                continue
            img_info_url.append('https://konachan.com'+tmp_url.get('href'))
            counter += 1
            if(counter >= MAX_COUNT):
                break

    page += 1
    url_get = "https://konachan.com/post?page="+str(page)+tag_url

    res = urllib.request.urlopen(url_get).read()
    soup = BeautifulSoup(res,'html.parser')

print(str(len(img_info_url))+"개의 이미지가 검색되었습니다.")

# 폴더 생성
now = datetime.now()
folder_name = tag +"("+str(len(img_info_url))+")_"+ str(now)[:10] + "_" + str(now)[11:13] + str(now)[14:16] + str(now)[17:19]

try:
    if not(os.path.isdir(folder_name)):
        os.makedirs(os.path.join(folder_name))
except OSError as e:
    if e.errno != errno.EEXIST:
        print("Failed to create directory!!")
        raise

print("저장폴더를 생성했습니다. <"+folder_name+">")


# 뷰어URL에서 이미지 크롤
print("크롤링을 시작합니다.")
for i in range(counter):

    res = urllib.request.urlopen(img_info_url[i]).read()
    soup = BeautifulSoup(res,'html.parser')

    #print(img_info_url[i])
    img_src = ""
    try:
        img_src = soup.find('a',class_='highres-show')['href']
        print("더 큰 사이즈의 원본을 받습니다")
    except:
        try:
            img_src = soup.find('img',class_='image')['src']
            print("표시된 원본을 그대로 받습니다")
        except:
            print("뭔가가 잘못되었습니다.")
    print('Downloading [ '+str(i+1)+' / '+str(counter) + ' ]')
    urllib.request.urlretrieve(img_src, '.\\'+folder_name+'\\'+str(i+1).zfill(3)+'.png')
    



# 썸네일 표시의 a 태그는 class='thumb'
#url = 'https://files.yande.re/sample/3de6b336c21feba3f1a0a796ac3d9dcc/yande.re%20488783%20sample%20anus%20doremy_sweet%20dress%20gekidoku_shoujo%20ke-ta%20nopan%20photoshop%20pussy%20skirt_lift%20tail%20touhou%20uncensored.jpg'
#urllib.request.urlretrieve(url, '.\\'+folder_name+'\\test.png')