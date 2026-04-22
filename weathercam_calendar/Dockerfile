FROM ghcr.io/home-assistant/base:latest

RUN apk add --no-cache python3 py3-pip py3-flask

COPY run.sh /run.sh
COPY app.py /app.py

RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
