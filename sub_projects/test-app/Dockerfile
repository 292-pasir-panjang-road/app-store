# Dockerfile

FROM python:3.7-slim

COPY . /usr/src/app
WORKDIR /usr/src/app
RUN pip install -r requirements.txt
RUN ln -s /usr/src/app/start.sh /usr/local/bin/start.sh

EXPOSE 8000
CMD /usr/local/bin/start.sh
