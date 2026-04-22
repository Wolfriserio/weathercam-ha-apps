FROM ghcr.io/home-assistant/base:latest

RUN apk add --no-cache ffmpeg bash coreutils findutils

COPY run.sh /run.sh
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
