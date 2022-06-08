FROM python:3-slim-bullseye

WORKDIR /usr/src/speedtest

RUN apt-get update \
 && apt-get -y install curl \
 && curl -s https://install.speedtest.net/app/cli/install.deb.sh | bash \
 && apt-get -y install speedtest cron \
 && rm -rf /var/lib/apt/lists/* \
 && mkdir /var/log/speedtest
 
COPY speedtest.py ./

ENV ST_CRON_SCH="10 * * * *"
CMD (env ; echo MAILTO=\"\") | crontab - \
 && (crontab -l ; echo "${ST_CRON_SCH} cd /usr/src/speedtest/; python speedtest.py -V > /proc/1/fd/1 2>&1") | crontab - \
 && crontab -l && cron -f
