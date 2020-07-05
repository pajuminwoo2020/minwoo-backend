# Bigstep backend

* 역할: DJango REST API server
* 환경: python 3.7.3 (파이썬 virtualenv 구성은[link](https://beomi.github.io/2016/12/28/HowToSetup-Virtualenv-VirtualenvWrapper/) 참고)
---

## Django server 띄우는 방법

### 패키지 설치

1. postgresql를 설치한다. pycopg2 python패키지 설치를 위해 필요한 과정이다.
```bash
$ sudo apt-get install postgresql postgresql-contrib
```
2. python 패키지를 설치한다.
```bash
$ cd bitstep-backend
$ pip install -r requirements.txt
```
3. 환경변수 설정을 한다. 아래와 같이 .env 파일 생성 후 임의로 만든 SECRET KEY를 설정해준다. local에서는 .env-example에 셋팅된 값을 그대로 사용해도
```bash
$ cd bigstep-backend/bigstep_backend/app/settings
$ cp .env-example .env
```
```vim
```

### 서버 띄우기
```bash
$ cd bigstep-backend/bigstep_backend
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```

### Windows
1. postgresql-contirb 설치
postgresql login후,
```bash
create extenstion pgcrypto;
```
2. python 패키지 설치
Microsoft Visual C++ 14.0 is required 에러 발생하면(psycopg2),
아래 링크에서 MS Build Tools 다운로드
https://visualstudio.microsoft.com/ko/visual-cpp-build-tools/
