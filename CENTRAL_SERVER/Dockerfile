FROM python:3.11.3
FROM mcr.microsoft.com/windows/servercore:ltsc2019

COPY . /.

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y python3
RUN pip install -y opencv-python
RUN pip install -y numpy
RUN pip install -y socket
RUN pip install -y pillow
RUN pip install -y httpx
RUN pip install -y attrs
RUN pip install -y requests
RUN pip install -y typing-extensions
RUN pip install -y urllib3

#! simpleslideinterface install and run before start of server

CMD [ "python3", "./CentralServer.py" ]