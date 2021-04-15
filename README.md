# konachan_downloader

### 다운로드 시

github에서 exe 실행파일만 내려받을 경우, 어쨰서인지 실행이 안됨.
아래와 같이 [압축파일](https://github.com/happylee789/konachan_downloader/archive/refs/heads/main.zip)로 받은 후, dist 폴더 안의 실행파일만 따로 빼서 사용 가능

![캡처4](https://user-images.githubusercontent.com/21221633/114849500-c700f880-9e1a-11eb-9eea-74c1fd7960f8.PNG)

애플리케이션 스크린샷

![캡처](https://user-images.githubusercontent.com/21221633/114842139-881b7480-9e13-11eb-9926-710f91e3bbda.PNG)

![캡처2](https://user-images.githubusercontent.com/21221633/114843028-5d7deb80-9e14-11eb-956a-d7baf926d680.PNG)



## 사용방법

애플리케이션 실행 후 (dist 폴더의 konachan.exe)
- 태그
- 이미지 갯수  

를 입력하여 [코나짱](https://konachan.com/)으로부터 이미지를 다운받는다.

해당 어플리케이션이 실행된 위치에 새로운 폴더를 만들어 최신 순으로 1번부터 번호를 매겨 저장한다.

#

## 주의사항
- 다운로드 버튼을 누를 시, 독립적인 새 스레드로 실행되기 때문에, 실수로 두 번 이상 누를 시 각각의 폴더에 해당 이미지를 다운받게 된다.
- 두 개 이상의 태그 입력 시, +를 넣어 구분한다.
- "long hair"과 같은 띄어쓰기가 필요한 경우, 띄어쓰기 대신 "_"를 사용한다. 태그 규칙은 [코나짱](https://konachan.com/)의 [태그](https://konachan.com/tag?order=date) 페이지 등을 참고.


#
## 실행파일 생성에 관하여

파이썬 소스가 위치한 경로에서 다음 커맨드를 사용  
```
pyinstaller.exe -F -w --onefile --icon=icon.ico konachan.py
```
이 방법으로 실행파일 생성 시, 독립적인 실행파일을 얻을 수 있으나, 파이썬 코드 내에 tkinter.call()을 사용하여 상단 아이콘 이미지를 지정했을 경우, 실행파일과 해당 이미지(여기서는 icon.png)가 같은 경로에 위치하지 않으면 애플리케이션을 실행할 수 없다.

파이썬 코드 내에서 tkinter.call()함수를 사용하지 않고 실행파일을 만들면, 독립적인 실행파일로 사용이 가능해진다. 단, 아래 이미지와 같이 상단 이미지는 tkinter 기본 이미지로 표시된다.  
![캡처3](https://user-images.githubusercontent.com/21221633/114847686-ec8d0280-9e18-11eb-93b6-0c8e44e6623c.PNG)