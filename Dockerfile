FROM python:3.8-slim-buster

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

ADD filter_page.py /
RUN mkdir -p /templates
COPY ./templates/filter_page.html /templates/filter_page.html

CMD [ "python3", "./filter_page.py"]