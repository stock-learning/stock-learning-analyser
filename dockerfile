FROM python:alpine3.7
COPY . /service-analyser
WORKDIR /service-analyser
RUN pip install -r requirements.txt
EXPOSE 5000