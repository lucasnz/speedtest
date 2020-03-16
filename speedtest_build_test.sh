#/bin/sh
FILE=/usr/src/speedtest
if [ -d $FILE ]; then
	echo "directory '$FILE' exists"
else
	echo "directory '$FILE' does not exists"
	exit 1
fi
FILE=/usr/src/speedtest/speedtest1
if [ -f $FILE ]; then
	echo "file '$FILE' exists"
else
	echo "file '$FILE' does not exists"
	exit 1
fi
FILE=/usr/src/speedtest/speedtest.py
if [ -f $FILE ]; then
	echo "file '$FILE' exists"
else
	echo "file '$FILE' does not exists"
	exit 1
fi
cd /usr/src/speedtest/
python speedtest.py --accept-st-eula --url https://httpbin.org/post
ret=$?
echo "speedtest.py exit code $ret"
if [ $ret -ne 0 ]; then
	echo "script error"
	exit $ret
fi
