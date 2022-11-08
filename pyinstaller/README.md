- 필수적으로 알아야 할 것 : window에서 빌드한 것은 window에서만 사용 가능하고, 다른 운영체제도 이와 같다. 또한 32비트 환경에서 만든 바이너리를 64비트에서 실행할 수 없다.

## pyinstaller 사용법
pyinstaller [option] [filename.py]

#### options
1. -F, --onefile : 1개의 exe 파일로 변환(시간이 좀 더 걸리는 단점 존재)
2. -D, --onedir : 1개의 폴더로 변환
3. -n, --name : 변환될 이름 지정, 별도의 지정이 없을 경우 스크립트 이름을 따라감
4. -w, --noconsole, --windowed : 콘솔 윈도우 표시 안함
5. -c, --console, --nowindowed : 콘솔 윈도우 표시(기본값)
6. -i, --icon : 아이콘 설정
7. --add-data <src;dst or src:dst> : 파일 추가(윈도우는 세미콜론(;), 유닉스는 콜론(:)으로 구분)
<br>

#### 참고
- exe 파일 용량 줄이기
간단한 프로그램인데 파일 용량이 커지는 현상을 마주할 수도 있다. <br>
원인은 <b>conda 명령어로 library를 설치</b>했기 때문이다. conda와 pyinstaller가 잘 맞지 않는다고 한다.<br>
해결방법은 대표적으로 <b>새로운 가상환경을 만들어서 pip로 library를 설치</b>하는 것이다.
<br>

#### 생길 수 있는 문제 해결방법
1. main.spec 파일로 계속 빌드를 했지만, 옵션이 적용되지 않는 문제
    <div>
    pyinstaller -D 옵션은 하나의 Directory 안에 넣고 그 안에 여러 개의 필요한 파일들이 들어있게 된다.<br>
    pyinstaller -F 옵션은 하나의 exe 파일만 떨어지므로 굉장히 간편하게 보이지만 어떤 특정 파일을 참조하는 코드가 있다면 골치 아파진다.<br><br>

    그런데 이 옵션은 <b>main.py에 우선적으로 적용되고, main.spec은 옵션을 무시</b>한다.(정확하게 말하면 spec안에 있는 값만 참조함)<br><br>

    "pyinstaller -F main.py"를 사용해서 빌드한 exe 파일이 존재하고 이에 맞는 main.spec이 생성되어 spec파일을 수정한 뒤,<br>
    "pyinstaller -D main.spec"을 해봐야 -D 옵션은 적용되지도 않고 무시된다.<br>

    <b>따라서 다시 -D 옵션으로 생성하고 싶다면 "pyinstaller -D main.py"를 다시 써주어 적용해야 한다.</b>
    </div>

2. python lib가 제대로 import 되지 않는 문제(no module name 'lib')
    <div>
    main.spec 파일 내부에 hiddenimports = [] 이 공간에 uvicorn 관련 모듈을 다 넣어주면 된다.
    </div>

3. python 코드 내에서 특정 data를 참조해야 하는데 찾지 못하는 경우
    <div>
    pyinstaller는 python 코드 내부에서 참조하는 데이터들을 전혀 고려해주지 않는다.<br>
    예를 들면, icon파일이나 이미지가 적용이 안되는 경우 혹은 file 입출력, directoy 참조 등이 있다.<br><br>

    해결방법은 우선 ./dist/main 폴더를 기본 경로로 잡아줘야 한다.<br><br>

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))<br>
    KEYWORD_DIC = f'{BASE_DIR}/{환경설정 변수들이 들어있는 파일}'<br><br>

    위처럼 BASE_DIR을 지정해주고 main.spec 파일에서 datas = [] 부분을 수정해주면 빌드 후에도 파일을 참조할 수 있다.<br><br>

    ** 주의<br>
    빌드 시 -F 옵션으로 빌드하게 되면 하나의 .exe파일만 떨어지게 되는데 ubuntu 환경에서는 BASE_DIR가 /tmp/_MEIxxxxxx/로 지정되고 사용되기 때문에 파일을 정상적으로 읽어오지 못한다.
    </div>

4. 실행이 안될 때 권한 설정
    <div>
    unix 환경에서는 빌드 후 main 실행파일이 생성되는데, 이 파일의 형식은 application/x-executable이다.<br>
    바로 실행이 안되기 때문에 권한 설정이 필요하다.<br><br>

    sudo chmod 777 ./main
    </div>
