#/bin/sh
if [ ! -f "/usr/src/speedtest/speedtest" ]; then
	echo "speedtest binary does not exist"
	exit 1
fi
cd /usr/src/speedtest/
python speedtest.py --accept-st-eula --url https://httpbin.org/post
ret=$?
if [ $ret -ne 0 ]; then
	echo "python script error"
	exit $ret
fi
