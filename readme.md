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

