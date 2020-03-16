FROM python:3-slim

WORKDIR /usr/src/speedtest

RUN apt-get update && apt-get -y install cron wget \
 && mkdir /var/log/speedtest \
 && wget -O ookla-speedtest-1.0.0-x86_64-linux.tgz https://bintray.com/ookla/download/download_file?file_path=ookla-speedtest-1.0.0-x86_64-linux.tgz \
 && tar -xzf ookla-speedtest-1.0.0-x86_64-linux.tgz \
 && rm ookla-speedtest-1.0.0-x86_64-linux.tgz

COPY speedtest.py ./

ENV ST_CRON_SCH="10 * * * *"
CMD (env ; echo MAILTO=\"\") | crontab - \
 && (crontab -l ; echo "${ST_CRON_SCH} cd /usr/src/speedtest/; python speedtest.py -V > /proc/1/fd/1 2>&1") | crontab - \
 && crontab -l && cron -f
