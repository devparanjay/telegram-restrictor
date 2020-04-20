FROM python:3.7

RUN pip install python-telegram-bot

RUN mkdir /tr
ADD . /tr
WORKDIR /tr

CMD python /tr/bot.py