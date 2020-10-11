FROM python:3-slim-buster

WORKDIR /usr/src/speedtest

RUN apt-get update \
 && apt-get -y install gnupg1 apt-transport-https dirmngr \
 && export INSTALL_KEY=379CE192D401AB61 \
 && export DEB_DISTRO=buster \
 && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys $INSTALL_KEY \
 && echo "deb https://ookla.bintray.com/debian ${DEB_DISTRO} main" | tee /etc/apt/sources.list.d/speedtest.list \
 && apt-get update \
 && apt-get -y install speedtest cron \
 && rm -rf /var/lib/apt/lists/* \
 && mkdir /var/log/speedtest

COPY speedtest.py ./

ENV ST_CRON_SCH="10 * * * *"
CMD (env ; echo MAILTO=\"\") | crontab - \
 && (crontab -l ; echo "${ST_CRON_SCH} cd /usr/src/speedtest/; python speedtest.py -V > /proc/1/fd/1 2>&1") | crontab - \
 && crontab -l && cron -f
