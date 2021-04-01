FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
RUN mkdir /code/staticfiles
RUN mkdir /code/mediafiles
WORKDIR /code

COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
#COPY ./entrypoint.sh /
#ENTRYPOINT ["sh", "/entrypoint.sh"]


