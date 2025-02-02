FROM ubuntu:latest
WORKDIR /usr/bot
COPY . .
RUN apt-get update
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
RUN apt-get install libpq-dev -y
RUN apt install python3.12-venv -y
RUN python3 -m venv botenv
RUN /usr/bot/botenv/bin/pip install requests
RUN /usr/bot/botenv/bin/pip install urllib3==1.26.15
RUN /usr/bot/botenv/bin/pip install requests-toolbelt==0.10.1
RUN /usr/bot/botenv/bin/pip install paramiko==3.4.0
RUN /usr/bot/botenv/bin/pip install python-telegram-bot==13.7
RUN /usr/bot/botenv/bin/pip install psycopg2==2.9.9
RUN /usr/bot/botenv/bin/pip install python-dotenv==1.0.1
CMD ["/usr/bot/botenv/bin/python3", "bot.py"]
