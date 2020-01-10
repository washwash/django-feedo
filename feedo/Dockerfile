FROM python:3.6

RUN mkdir /opt/app
WORKDIR /opt/app/

COPY pyproject.toml poetry.lock /opt/app/
COPY . /opt/app/

RUN apt-get update && apt-get -y install \
    build-essential \
    python-dev \
    vim

RUN pip install uwsgi
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN cd /opt/app/
RUN poetry install

COPY install_resources /install_resources/
