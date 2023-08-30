FROM python:3.11.3
FROM mcr.microsoft.com/windows/servercore:ltsc2019

COPY . /.

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y python3
RUN pip install -y socket

CMD [ "python3",  "./FileServer.py"]