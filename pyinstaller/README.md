- 필수적으로 알아야 할 것 : window에서 빌드한 것은 linux에서 사용할 수 없고, linux에서 빌드한 것은 window에서 사용할 수 없다. 또한 32비트 환경에서 만든 바이너리를 64비트에서 실행할 수 없다.

## pyinstaller 사용법
pyinstaller [option] [filename.py]

#### options
1. -F, --onefile
1개의 exe 파일로 변환(시간이 좀 더 걸리는 단점 존재)
2. -D, --onedir
1개의 폴더로 변환
3. -n, --name
변환될 이름 지정, 별도의 지정이 없을 경우 스크립트 이름을 따라감
4. -w, --windowed, --noconsole
콘솔 윈도우 표시 안함
5. -c, --console, --nowindowed
콘솔 윈도우 표시(기본값)
6. -i, --icon
아이콘 설정
7. --add-data <src;dst or src:dst>
파일 추가(윈도우는 세미콜론(;), 유닉스는 콜론(:)으로 구분)

#### 참고
- exe 파일 용량 줄이기
간단한 프로그램인데 파일 용량이 커지는 현상을 마주할 수도 있다. 원인은 <b>conda 명령어로 numpy와 pandas</b>를 설치했기 때문이다. conda와 pyinstaller가 잘 맞지 않는다고 한다.
해결방법은 대표적으로 <b>새로운 가상환경을 만들어서 pip로 numpy와 pandas</b>를 설치하는 것이다.

- pyinstaller의 바이너리 생성과정
pyinstaller는 입력받은 파이썬 스크립트를 읽어서 'import' 구문을 모두 읽어 들인다. 바이너리로 만들 파이썬 스크립트가 사용하고 있는 의존성 패키지들과 다른 스크립트들을 recursive하게 따라가면서 필요한 리스트를 조사한다. 이 때, 런타임에 결정되는 일부 패키지들은 포함되지 않을 수 있다. 예를 들어 __import__() 구문을 이용하여 변수 값에 따른 동적 로딩을 할 때, imp.find_module(), sys.path 등을 이용할 때는 파이썬 스크립트를 정적으로 분석하여 의존성 라이브러리를 찾기 힘들다.
이런 경우 pyinstaller 실행 시 import에 대한 부가적인 정보를 넣어주면 된다. pyinstaller를 실행하면 디렉토리에 test.spec 파일이 생성되는데 이 파일에 정적 분석으로 알 수 없는 정보들을 넣어주면 된다. 예를 들어 실행파일을 만들 때 같이 배포되어야 하는 README 파일이나 런타임 정보들을 이 spec 파일에 적어주면 pyinstaller가 바이너리 생성시 참조한다.
바이너리가 실행될 서버에 기본적으로 설치되어 있는 패키지들은 실행파일에 포함되지 않을 수 있다. 이런 패키지들은 '/lib', 혹은 '/usr/lib' 등에 위치시키면 된다.

#### 생길 수 있는 문제 해결방법
1. main.spec 파일로 계속 빌드를 했지만, 옵션이 적용되지 않는 문제
pyinstaller -D 옵션은 하나의 Directory 안에 넣고 그 안에 여러 개의 필요한 파일들이 들어있게 된다.
pyinstaller -F 옵션은 하나의 exe 파일만ㄷ떨어지므로 굉장히 간편하게 보이지만 어떤 특정 파일을 참조하는 코드가 있다면 골치 아파진다.

그런데 이 옵션은 <b> main.py에 우선적으로 적용되고, main.spec은 옵션을 무시</b>한다.(정확하게 말하면 spec안에 있는 값만 참조함)

"pyinstaller -F main.py"를 사용해서 빌드한 exe 파일이 존재하고 이에 맞는 main.spec이 생성되어 spec파일을 수정한 뒤
"pyinstaller -D main.spec"을 해봐야 -D 옵션은 적용되지도 않고 무시된다.
<b>따라서 다시 -D 옵션으로 생성하고 싶다면
"pyinstaller -D main.py"를 다시 써주어 적용해야 한다.</b>

2. python lib가 제대로 import 되지 않는 문제(no module name 'lib')
main.spec 파일 내부에 hiddenimports = [] 이 공간에 uvicorn 관련 모듈을 다 넣어주면 된다.

3. python 코드 내에서 특정 data를 참조해야 하는데 찾지 못하는 경우
pyinstaller는 python 코드 내부에서 참조하는 데이터들을 전혀 고려해주지 않는다.
예를 들면, icon파일이나 이미지가 적용이 안되는 경우 혹은 file 입출력, directoy 참조 등이 있다.

해결방법은 우선 ./dist/main 폴더를 기본 경로로 잡아줘야 한다.

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEYWORD_DIC = f'{BASE_DIR}/{환경설정 변수들이 들어있는 파일}'

위 소스코드처럼 BASE_DIR을 지정해주고 main.spec 파일에서 datas = [] 부분을 수정해주면 빌드 후에도 파일을 참조할 수 있다.

** 주의
빌드 시 -F 옵션으로 빌드하게 되면 하나의 .exe파일만 떨어지게 되는데 ubuntu 환경에서는 BASE_DIR가 /tmp/_MEIxxxxxx/로 지정되고 사용되기 때문에 파일을 정상적으로 읽어오지 못한다.

4. 실행이 안될 때 권한 설정
unix 환경에서는 빌드 후 main 실행파일이 생성되는데, 이 파일의 형식은 application/x-executable이다.
바로 실행이 안되기 때문에 권한 설정이 필요하다.

sudo chmod 777 ./main