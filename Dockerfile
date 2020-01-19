FROM python:3.8.1-alpine

LABEL Name=birthday_bot Version=0.0.2
LABEL maintainer=biohazardvos@gmail.com

ENV DATABASE_URL app.db

WORKDIR /opt/birthday_bot
ADD . /opt/birthday_bot

RUN python3 -m pip install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "birthdaybot:app"]
