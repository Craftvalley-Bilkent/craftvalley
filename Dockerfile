FROM python:3.12
ENV PYTHONUNBUFFERED 1
RUN mkdir /craftvalley
WORKDIR /craftvalley
ADD . /craftvalley/
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .