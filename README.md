# Bigstep backend

## 기본 환경
* python 3.7.3 (파이썬 virtualenv 구성은[link](https://beomi.github.io/2016/12/28/HowToSetup-Virtualenv-VirtualenvWrapper/) 참고)

## Django server 띄우는 방법

### 패키지 설치

postgresql를 설치한다. pycopg2 python패키지 설치를 위해 필요한 과정이다.
```bash
$ sudo apt-get install postgresql postgresql-contrib
```
python 패키지를 설치한다.
```bash
$ cd bitstep-backend
$ pip install -r requirements.txt
```
환경변수 설정을 한다. 아래와 같이 .env 파일 생성 후 임의로 만든 SECRET KEY를 설정해준다
```bash
$ cd bigstep-backend/bigstep_backend/app/settings
$ cp .env-example .env
```

### 서버 띄우기
```bash
$ cd bigstep-backend/bigstep_backend
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```
