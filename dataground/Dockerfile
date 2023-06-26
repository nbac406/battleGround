FROM ubuntu:22.04

WORKDIR /dataground

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE config.settings.prod

# apt 업그레이트 및 업데이트
RUN apt-get -y update && apt-get -y dist-upgrade
# apt-utils dialog : 우분투 초기 설정 / libpq-dev : PostgreSQL 의존성
RUN apt-get install -y apt-utils dialog libpq-dev
# pip dev 설치
RUN apt-get install -y python3-pip python3-dev

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]