FROM python:3.10

RUN apt update; yes | apt install python3-lxml

RUN mkdir src
WORKDIR src
RUN adduser user
USER user
ENV PATH="$PATH:/home/user/.local/bin"


ADD ./requirements.txt .
RUN pip3 install -r requirements.txt

ADD . .

CMD ["python3", "-u", "./collect-games.py"]
