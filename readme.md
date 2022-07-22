# Speedtest
Runs a speedtest on a schedule using the speedtest.net Linux binary then sends the logs to InfluxDB. You must read and accept the speedtest.net EULA before deploying this container.

## Setup Guide
Download and extract the required files from my github, here: https://github.com/lucasnz/speedtest/archive/refs/heads/master.zip

#### Set the setup.sh as executable:
chmod 755 setup.sh

#### Run the command:
./setup.sh

#### Configure passwords in docker-compose.yml and datasources/all.yml
vi docker-compose.yml  
vi datasources/all.yml

#### Start the programme:
docker-compose up

#### Configure Grafana
Access grafana by navigating to: http://docker-host:3000/  
Log in with the grafana admin credential specified in the docker-compose file.  
Click Configuration, then preferences to set the "Speed Test" Dashboard as the Home Dashboard.

## Speedtest Server ID
The following two speedtest websites will list the nearest speedtest servers and their IDs:
* https://www.speedtest.net/speedtest-servers-static.php
* https://www.speedtest.net/api/js/servers?limit=10

Alternatively, you can use the speedtest.net website to obtain server IDs using the instructions here: https://www.dcmembers.com/skwire/how-to-find-a-speedtest-net-server-id/

## Parameters

Container images are configured using parameters passed at runtime.

| Parameter | Function |
| :----: | --- |
| `-h <hostname>` | Appears in InfluxDB logs. If not specified, the container ID will be used. |
| `-e TZ=Europe/London` | Specify a time zone to use e.g. Europe/London. |
| `-e ACCEPT_ST_EULA=1` | Once you've reviewed the speedtest.net EULA and accepted enable this environment variable. |
| `-e ST_URL=http://<influxDB_hostname_or_IP>:8086/write` | Required URL for InfluxDB. |
| `-e ST_TEST_SERVER_ID=123,345` | Specify the speedtest server IDs. Multiple IDs can be listed via comma separated list. If not specified, the binary will auto select a server. For best results, specify server IDs you know to work well. |
| `-e ST_USERNAME=<InfluxDB_username>` | InfluxDB username (required if authentication is enabled in InfluxDB). |
| `-e ST_PASSWORD=<InfluxDB_paasword>` | InfluxDB password (required if authentication is enabled in InfluxDB). |
| `-e ST_DATABASE=<InfluxDB_database>` | InfluxDB database. Defaults to `speedtest` if not specified. |
| `-e ST_CRON_SCH=<cron_time>` | cron schedule for test. Defaults to `10 * * * *` if not specified. |
| `-v ./logs/:/var/log/speedtest/` | Log files reside here and can optionally be retained by mapping the volume. |

## docker-compose

Example docker-compose file.

```
---
version: '3.6'

services:
  grafana:
    image: grafana/grafana:latest
    container_name: speedtest_grafana
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=adminpassword
    volumes:
      - ./grafana_config:/var/lib/grafana
      - ./dashboards:/etc/grafana/provisioning/dashboards
      - ./datasources:/etc/grafana/provisioning/datasources
    ports:
      - 3000:3000
    restart: always

  influxdb:
    image: influxdb:alpine
    container_name: speedtest_influxdb
    environment:
      - TZ=Europe/London
    #you may need to initialize influxdb on first run
      - DOCKER_INFLUXDB_INIT_MODE=setup
      - DOCKER_INFLUXDB_INIT_USERNAME=influxuser
      - DOCKER_INFLUXDB_INIT_PASSWORD=influxpassword
      - DOCKER_INFLUXDB_INIT_ORG=my-org
      - DOCKER_INFLUXDB_INIT_BUCKET=mybucket
      - V1_DB_NAME=speedtest
      - V1_RP_NAME=v1-rp
      - V1_AUTH_USERNAME=speedtest
      - V1_AUTH_PASSWORD=mypassword
      - DOCKER_INFLUXDB_INIT_RETENTION=52w
    volumes:
      - ./data:/var/lib/influxdb2
      - ./config:/etc/influxdb2
      - ./db_scripts:/docker-entrypoint-initdb.d
    #ports only needed if you want to expose influxdb outside the stack
    #ports:
    #  - 8086:8086
    restart: always

  speedtest:
    image: lucasnz/speedtest
    container_name: speedtest
    hostname: docker_speedtest
    environment:
      - TZ=Europe/London
      - ACCEPT_ST_EULA=1
      - ST_DATABASE=speedtest
      - ST_URL=http://influxdb:8086/write
      - ST_TEST_SERVER_ID=28314,16805,7317
      - ST_USERNAME=speedtest
      - ST_PASSWORD=mypassword
      #- ST_CRON_SCH=27 * * * *
      #- ST_CRON_SCH=10 1-23/4 * * *
      - ST_CRON_SCH=45 22,2-6/4 * * *
    volumes:
      - ./speedtest_logs/:/var/log/speedtest/
    restart: always

```

## License

This script is dependent on the speedtest.net binary. The speedtest.net binary license states:
```
You may only use this Speedtest software and information generated
from it for personal, non-commercial use, through a command line
interface on a personal computer. Your use of this software is subject
to the End User License Agreement, Terms of Use and Privacy Policy at
these URLs:

        https://www.speedtest.net/about/eula
        https://www.speedtest.net/about/terms
        https://www.speedtest.net/about/privacy
```
To show you have read and agreed to the speedtest.net terms, you must specify the "ACCEPT_ST_EULA" environment variable.

The MIT License applies to all other components.

Copyright (c) 2020 Luke Broadbent

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
