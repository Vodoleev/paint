FROM ubuntu:latest

RUN apt-get update && apt-get -y install nano python3.11 python3.11-distutils python3-pip screen

RUN pip install pyTelegramBotAPI
RUN pip install asyncio
RUN pip install aiohttp
RUN pip install pillow