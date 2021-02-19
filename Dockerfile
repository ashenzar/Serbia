# We're using Ubuntu 20.10
FROM sahyam/docker:groovy

#
# Clone repo and prepare working directory
#
RUN git clone -b dev https://github.com/ashenzar/Serbia /root/userbot
RUN mkdir /root/userbot/.bin
WORKDIR /root/userbot

#Install python requirements
RUN pip3 install -r https://raw.githubusercontent.com/ashenzar/Serbia/dev/requirements.txt

CMD ["python3","-m","userbot"]
