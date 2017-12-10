#!/bin/sh

PYTHONS="
python
/usr/bin/python
/usr/local/bin/python
python2.7
/usr/bin/python2.7
/usr/local/bin/python2.7
/Library/Frameworks/Python.framework/Versions/2.6/bin/python2.7
python2.6
/usr/bin/python2.6
/usr/local/bin/python2.6
/Library/Frameworks/Python.framework/Versions/2.6/bin/python2.6
python2.5
/usr/bin/python2.5
/usr/local/bin/python2.5
/Library/Frameworks/Python.framework/Versions/2.5/bin/python2.5
python2.4
/usr/bin/python2.4
/usr/local/bin/python2.4
/Library/Frameworks/Python.framework/Versions/2.4/bin/python2.4
"

testPython() {
	"${1}" << EOF
import sys
if sys.version < '2.4':
	sys.exit(1)
EOF
}

MY_DIR=$(dirname "${0}")

if testPython "${PYTHON}" > /dev/null 2> /dev/null
then
	"${PYTHON}" "${MY_DIR}/Forgery.py"
	exit "${?}"
fi
for PYTHON in ${PYTHONS}
do
	if testPython "${PYTHON}" > /dev/null 2> /dev/null
	then
		"${PYTHON}" "${MY_DIR}/Forgery.py"
		exit "${?}"
	fi
done
echo "Python 2.4 or higher was not found.  Please set \$PYTHON to the"
echo "location of your Python interpreter, and then try again."
