FROM ubuntu:latest
LABEL description="GIT"

RUN apt update -y
RUN apt install git -y
RUN apt install openssh-client -y
