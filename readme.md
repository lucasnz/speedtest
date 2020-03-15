# Speedtest
Runs a speedtest on a schedule using the speedtest.net Linux binary then sends the logs to InfluxDB. You must read and accept the speedtest.net EULA before deploying this container.

## Parameters

Container images are configured using parameters passed at runtime.

| Parameter | Function |
| :----: | --- |
| `-h <hostname>` | Appears in InfluxDB logs. If not specified the container ID will be used. |
| `-e TZ=Europe/London` | Specify a time zone to use e.g. Europe/London. |
| `-e ACCEPT_ST_EULA=1` | Once you've reviewed the speedtest.net EULA and accepted enable this environment variable. |
| `-e ST_URL=http://<influxDB_hostname_or_IP>:8086/write` | Required URL for InfluxDB. |
| `-e ST_TEST_SERVER_ID=123,` | Specify they speedtest server by ID. If not specified, the binary will auto-select a server. For best results, select a server from: https://telcodb.net/explore/speedtest-servers/ |
| `-e ST_USERNAME=<InfluxDB_username>` | InfluxDB username (required if authentication is enabled in InfluxDB). |
| `-e ST_PASSWORD=<InfluxDB_paasword>` | InfluxDB password (required if authentication is enabled in InfluxDB). |
| `-e ST_DATABASE=<InfluxDB_database>` | InfluxDB database. Defaults to `speedtest` if not specified. |
| `-e ST_CRON_SCH=<cron_time>` | cron schedule for test. Defaults to `10 * * * *` if not specified. |
| `-v ./logs/:/var/log/speedtest/` | Log files reside here and can optionally be retained by mapping the volume. |

### docker-compose

Example docker-compose file.

```
---
---
version: '2'
services:
  speedtest:
    image: lucasnz/speedtest:latest
    container_name: speedtest
    hostname: docker_speedtest
    environment:
      TZ: Pacific/Auckland
      ACCEPT_ST_EULA: 1
      ST_URL: http://192.168.1.10:8086/write
      ST_TEST_SERVER_ID: 123
      ST_USERNAME: speedtest
      ST_PASSWORD: speedtest
      ST_DATABASE: speedtest
      ST_CRON_SCH: 50 * * * *
    volumes:
      - ./logs/:/var/log/speedtest/
    restart: unless-stopped
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
