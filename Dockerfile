FROM python:3
ENV PATH=/usr/local/bin:$PATH ENV=prod
VOLUME /data
RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN pip install -r requirements.txt --index https://pypi.mirrors.ustc.edu.cn/simple/
CMD ["scrapy", "crawl", "qichacha"]
