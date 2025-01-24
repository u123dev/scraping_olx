FROM python:3.12
LABEL maintainer="u123@ua.fm"

ENV PYTHONUNBUFFERED 1

WORKDIR app/

COPY requirements.txt ./
RUN pip install  -r requirements.txt
COPY . .

#ENTRYPOINT ["scrapy"]
#
#CMD ["crawl", "olx"]

CMD ["tail", "-f", "/dev/null"]
