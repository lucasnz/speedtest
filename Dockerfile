FROM python:3-slim

#COPY requirements.txt ./
#RUN pip install --no-cache-dir -r requirements.txt

#WORKDIR /var/log/speedtest
WORKDIR /usr/src/speedtest

#ADD ookla-speedtest-1.0.0-x86_64-linux.tgz .
RUN apt-get update && apt-get -y install cron wget \
 && mkdir /var/log/speedtest \
 && wget -O ookla-speedtest-1.0.0-x86_64-linux.tgz https://bintray.com/ookla/download/download_file?file_path=ookla-speedtest-1.0.0-x86_64-linux.tgz \
 && tar -xzf ookla-speedtest-1.0.0-x86_64-linux.tgz \
 && rm ookla-speedtest-1.0.0-x86_64-linux.tgz

COPY speedtest.py ./

ENV ST_CRON_SCH="10 * * * *"
#ENV ST_CRON_SCH="*/1 * * * *"
#CMD (env | grep ^ST_[^C]; echo MAILTO=\"\") | crontab - && (crontab -l ; echo "${ST_CRON_SCH} cd /usr/src/speedtest/; python speedtest.py -V > /proc/\$(cat /var/run/crond.pid)/fd/1 2>&1") | crontab - && crontab -l && (crontab -l ; echo "*/1 * * * * echo \`date\` hello world > /proc/\$(cat /var/run/crond.pid)/fd/1") | crontab - && crontab -l && cron -f
# CMD if [ ! -e /tmp/stdout ]; then mkfifo /tmp/stdout && chmod 777 /tmp/stdout; fi \
 # && (env | grep ^ST_[^C]; echo MAILTO=\"\") | crontab - \
 # && (crontab -l ; echo "${ST_CRON_SCH} cd /usr/src/speedtest/; python speedtest.py -V > /tmp/stdout 2>&1") | crontab - \
 # && crontab -l && (crontab -l ; echo "*/1 * * * * echo \`date\` hello world > /tmp/stdout") | crontab - \
 # && crontab -l && cron -f | tail -f --pid=$(cat /var/run/crond.pid) /tmp/stdout
CMD (env ; echo MAILTO=\"\") | crontab - \
 && (crontab -l ; echo "${ST_CRON_SCH} cd /usr/src/speedtest/; python speedtest.py -V > /proc/1/fd/1 2>&1") | crontab - \
 && crontab -l && cron -f
#CMD (env | grep ^ST_[^C]; echo MAILTO=\"\") | crontab - && (crontab -l ; echo "${ST_CRON_SCH} source $HOME/.profile; python /usr/src/speedtest/speedtest.py -V -e/etc/speedtest/speedtest > /proc/1/fd/1 2>/proc/1/fd/2") | crontab - && crontab -l && (crontab -l ; echo "*/1 * * * * echo `date` hello world > /proc/1/fd/1 2>/ proc/1/fd/2") | crontab - && crontab -l && cron -f
#CMD (env | grep ^ST_[^C]; echo MAILTO=\"\") | crontab - && (crontab -l ; echo "${ST_CRON_SCH} source $HOME/.profile; python /usr/src/speedtest/speedtest.py -V -e/usr/src/speedtest/speedtest > /proc/1/fd/1 2> /proc/1/fd/2") | crontab - && crontab -l && cron -f
#ENTRYPOINT [ "python", "./speedtest.py", ["-V"] ]
