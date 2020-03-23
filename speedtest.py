# Copyright (c) 2020 Luke Broadbent

# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in the
# Software without restriction, including without limitation the rights to use, copy,
# modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the
# following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import subprocess,json
from datetime import datetime
from base64 import b64encode
import sys
import socket
import getopt

try:
    from urllib.request import Request, urlopen  # Python 3
except ImportError:
    from urllib2 import Request, urlopen  # Python 2

import logging
import logging.handlers
import os

def main(argv):

    server_ids = None #'18474'
    log_file = "speedtest.log"
    if sys.platform == "win32":
        executable = 'speedtest.exe'
    else:
        executable = './speedtest'
        if os.path.isdir("/var/log/speedtest"):
            log_file = '/var/log/speedtest/speedtest.log'

    #url_base = 'https://httpbin.org/post'
    #url_base = 'http://influxdb.lan:8086/write'
    url_base = 'http://172.0.0.1:8086/write'
    database_name = 'speedtest'
    username = None
    password = None
    accept_license = ''
    
    # Set up a specific logger with our desired output level
    logger = logging.getLogger('speedtest')
    #logger.info(logger.handlers)
    #if logger.handlers == []:
    logger.setLevel(logging.DEBUG)
    c_handler = logging.StreamHandler(sys.stdout)
    f_handler = logging.handlers.RotatingFileHandler(
                  log_file, maxBytes=512000, backupCount=1)
    c_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    f_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)
    #logger.info(logger.handlers)
    logger.info("Script begin")

    try:
        opts, args = getopt.getopt(argv,"hd:e:U:P:u:s:V",["help", "database=", "executable=","username=","password=","url=","test-server-id=","env-variables","accept-st-eula"])
    except getopt.GetoptError:
        print('Error: Incorrect parameters. use -h for help.')
        sys.exit(2)
    for opt, arg in opts:
        #print("opt: %s" % opt)
        #print("arg: %s" % arg)
        if opt in ('-h', '--help'):
            print(usage_options())
            sys.exit()
        elif opt in ('-d', '--database'):
            database_name = arg
        elif opt in ('-e', '--executable'):
            executable = arg
        elif opt in ('-P', '--password'):
            password = arg
        elif opt in ('-U', '--username'):
            username = arg
        elif opt in ('-u', '--url'):
            url_base = arg
        elif opt in ('-s', '--test-server-id'):
            server_ids = arg
        elif opt in ('--accept-st-eula'):
            accept_license = '--accept-license '
        elif opt in ('-V', '--env-variables'):
            database_name = os.getenv('ST_DATABASE', database_name)
            executable = os.getenv('ST_EXECUTABLE', executable)
            password = os.getenv('ST_PASSWORD', password)
            username = os.getenv('ST_USERNAME', username)
            url_base = os.getenv('ST_URL', url_base)
            server_ids = os.getenv('ST_TEST_SERVER_ID', server_ids)
            if 'ACCEPT_ST_EULA' in os.environ:
                accept_license = '--accept-license '
    logger.info('database_name: %s' % database_name)
    logger.info('executable: %s' % executable)
    logger.info('username: %s' % username)
    if password != None:
        logger.info('password: %s' % (len(password)*'*'))
    else:
        logger.info('password: %s' % password)
    logger.info('accept-st-eula: %s' % accept_license)
    logger.info('url: %s' % url_base)
    logger.info('server-id: %s' % server_ids)
    
    if server_ids != None and "," in server_ids:
       server_ids = server_ids.split(",")
    else:
        server_ids = [server_ids]

    for server_id in server_ids:
        if server_id == None:
            branch_cmd = "%s %s--format=json-pretty" % (executable, accept_license)
        else:
            branch_cmd = "%s %s--server-id=%s --format=json-pretty" % (executable, accept_license, server_id)
        logger.info("command line: %s" % branch_cmd)

        proc = subprocess.Popen(branch_cmd.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (output, error) = proc.communicate()
        output = output.decode('utf-8')
        logger.info("speedtest output: %s" % output.replace('\r', '').replace('\n', '\\n'))
        if error:
            logger.error("speedtest error: %s" % error.decode('utf-8'))

        try:
            output_json = json.loads(output)

            timestamp = datetime.strptime(output_json['timestamp']+'UTC', '%Y-%m-%dT%H:%M:%SZ%Z')
            timestamp_unix = int((timestamp - datetime(1970, 1, 1)).total_seconds())
            #timestamp_unix_nano = timestamp_unix * 1000 * 1000

            #fields - floats do not need to be escaped
            jitter = float(output_json['ping']['jitter'])
            latency = float(output_json['ping']['latency'])
            download_Mbps = round((output_json['download']['bandwidth'])*8/1000/1000, 2)
            upload_Mbps = round((output_json['upload']['bandwidth'])*8/1000/1000, 2)
            result_url = quote(output_json['result']['url'], 3)
            external_IP = quote(output_json['interface']['externalIp'], 3)
            
            #tags
            server_id = quote(output_json['server']['id'])
            server_name = quote(output_json['server']['name'])
            server_location = quote(output_json['server']['location'])
            server_country = quote(output_json['server']['country'])
            hostname = quote(socket.gethostname())
        except Exception as e:
            logger.error("Error loading JSON: %s" % repr(e))
            exit(1)

        #data = 'cpu_load_short,host=server01,region=us-west value=0.64 1434055562000000000'
        measurement = "speedtest-results"
        tags =   "hostname=%s," % hostname + \
                 "server-country=%s," % server_country + \
                 "server-id=%s," % server_id + \
                 "server-location=%s," % server_location + \
                 "server-name=%s" % server_name
        fields = "download-bandwidth=%s," % download_Mbps + \
                 "external-IP=%s," % external_IP + \
                 "jitter=%s," % jitter + \
                 "latency=%s," % latency + \
                 "result-url=%s," % result_url + \
                 "upload-bandwidth=%s" % upload_Mbps

        data = "%s,%s %s %s" % (measurement, tags, fields, timestamp_unix)
        logger.info("data to send: %s" % data)

        url = '%s?db=%s&precision=s' % (url_base, database_name)
        #url = '%s?db=%s&u=%s&p=%s&precision=s' % (url_base, database_name, username, password)
        req = Request(url, data.encode('utf-8'))
        if username != None and password != None:
            base64string = b64encode(("%s:%s" % (username, password)).encode())
            req.add_header("Authorization", "Basic %s" % base64string.decode())
        req.add_header("Content-Type", "text")
        try:
            resp = urlopen(req).read().decode('utf-8')
            logger.info("response: %s" % resp)
        except Exception as e:
            logger.error("Error writing data: %s" % repr(e))

def usage_options():
    return   "Usage: speedtest.py [<options>]\n" + \
             "  -h, --help                        Print usage information\n" + \
             "  -d, --database=<database_name>    Influx database name\n" + \
             "                                     * if not specified, assumes speedtest\n" + \
             "  -e, --executable=<executable>     Speedtest executable filename and path\n" + \
             "                                     * assumes speedtest.exe for Windows and\n" + \
             "                                       speedtest for *nix in current working directory\n" + \
             "  -U, --username=<username>         InfluxDB username\n" + \
             "                                     * if InfluxDB requires authentication a\n" + \
             "                                     * username and password must be specified\n" + \
             "  -P, --password=<password>         InfluxDB password\n" + \
             "  -u, --url=<influxDB_URL>          The InfluxDB url\n" + \
             "                                     * if not specified, assumes; http://127.0.0.1:8086/write\n" + \
             "  -s, --test-server-id=<server_id>  The speed test server ID\n" + \
             "                                     * if not specified, allows speedtest to auto select\n" + \
             "  -V, --env-variables               Script to read environment variables. Environment variables should be all caps,\n" + \
             "                                      have the same name as the long options, and '-' are replaced with '_'\n" + \
             "                                      E.g. ST_TEST_SERVER_ID. ACCEPT_ST_EULA is a special case (no ST prefix).\n" + \
             "  --accept-st-eula                  Required to accept the speedtest EULA."

# Quoting
# field value strings;
    # back slash
    # double quotes
    # commas
    # equal signs
    # spaces
# tag values:
    # commas
    # equal signs
    # spaces
# keys (both tags and fields):
    # commas
    # equal signs
    # spaces
# measurement:
    # commas
    # spaces
# FIELD = 3   #field values
# TAG = 2     #tag values
# KEY = 2     #field and tag keys
# MEASURE = 1 #measurements
def quote(to_quote, quote_type=2):
    try:
        if quote_type > 2: #field values
            to_quote = to_quote.replace('\\', '\\\\')
            to_quote = to_quote.replace('"', '\"')
            if to_quote[0] != '"' and to_quote[-1] != '"':
                to_quote = '"%s"' % to_quote

        if quote_type > 1: #tag values
            to_quote = to_quote.replace('=', '\=')
        
        to_quote = to_quote.replace(',', '\,')
        to_quote = to_quote.replace(' ', '\ ')
    except:
        pass
    return to_quote

if __name__ == "__main__":
   main(sys.argv[1:])